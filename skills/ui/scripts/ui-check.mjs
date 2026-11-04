#!/usr/bin/env node
// ui-check.mjs — 웹 화면을 헤드리스 브라우저로 폭마다 찍고, 화면을 재서 결함을 이름으로 낸다(dev:ui). 실패가 있으면 종료 코드 1.
// 쓰는 법: node ui-check.mjs <URL|HTML 파일> [--widths 1440,390] [--select <css>] [--ignore <css>] [--out shots] [--wait 1000]
// 종료 코드: 0 통과(경고는 있을 수 있음) · 1 실패 있음 · 2 쓰는 법 틀림 · Playwright·브라우저 없음 · 페이지 못 엶.
// 일부러 넘긴 곳은 그 요소에 data-ui-check-ignore 를 붙이거나 --ignore 로 뺀다.
// 검사 아이디어와 일부 기준값은 benjitaylor/skills 의 stageshow scripts/film-checks.mjs
// (MIT, Copyright (c) 2026 Benji Taylor)에서 빌렸다. 코드는 업무 화면용으로 새로 썼다.
import { createRequire } from 'node:module'
import { existsSync, mkdirSync, readdirSync, statSync } from 'node:fs'
import { join, resolve, basename, delimiter } from 'node:path'
import { pathToFileURL } from 'node:url'
import { execSync } from 'node:child_process'
import os from 'node:os'

function parseArgs(argv) {
  const o = { widths: [1440, 390], select: '', ignore: '', out: 'shots', wait: 1000, url: '' }
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i], v = () => argv[++i] ?? ''
    if (a === '--widths') o.widths = v().split(',').map(Number).filter((n) => n > 0)
    else if (a === '--select') o.select = v()
    else if (a === '--ignore') o.ignore = v()
    else if (a === '--out') o.out = v()
    else if (a === '--wait') o.wait = Number(v()) || 0
    else if (!a.startsWith('--')) o.url = a
  }
  return o
}

// Playwright 찾기: 프로젝트 → `npx -p playwright` 가 PATH 에 넣은 폴더 → 전역 → npx 임시 폴더(최근 것부터).
function findPlaywright() {
  const bases = [process.cwd()]
  for (const p of (process.env.PATH || '').split(delimiter)) if (/node_modules[\\/]\.bin$/.test(p)) bases.push(resolve(p, '..', '..'))
  try { bases.push(resolve(execSync('npm root -g', { stdio: ['ignore', 'pipe', 'ignore'] }).toString().trim(), '..')) } catch {}
  for (const cache of [join(os.homedir(), 'AppData', 'Local', 'npm-cache', '_npx'), join(os.homedir(), '.npm', '_npx')]) {
    if (!existsSync(cache)) continue
    const dirs = readdirSync(cache).map((d) => join(cache, d)).sort((a, b) => statSync(b).mtimeMs - statSync(a).mtimeMs)
    bases.push(...dirs)
  }
  for (const base of bases) for (const name of ['playwright', 'playwright-core']) {
    try { return createRequire(join(base, 'noop.js'))(name) } catch {}
  }
  return null
}

async function launch(pw) {
  const errs = []
  for (const o of [{}, { channel: 'chrome' }, { channel: 'msedge' }]) {
    try { return await pw.chromium.launch({ headless: true, ...o }) } catch (e) { errs.push(String(e.message).split('\n')[0]) }
  }
  throw new Error(errs.join(' / '))
}

// 페이지가 열리기 전에 심는다: 화면이 그려진 뒤 밀린 기록(layout-shift)을 모은다.
function shiftRecorder() {
  window.__uiShifts = []
  try {
    new PerformanceObserver((list) => {
      for (const e of list.getEntries()) if (!e.hadRecentInput) window.__uiShifts.push({ value: e.value, nodes: (e.sources || []).map((s) => s.node).filter(Boolean) })
    }).observe({ type: 'layout-shift', buffered: true })
  } catch {}
}

// 페이지 안에서 돈다. 이 함수 밖의 것을 쓰지 않는다(page.evaluate 로 넘어간다).
function audit({ select, ignore }) {
  const root = (select && document.querySelector(select)) || (select ? null : document.body)
  if (!root) return { fails: [`select: ${select} 를 찾지 못했다`], warns: [] }
  const fails = [], warns = [], counts = {}
  const push = (fail, key, msg) => { counts[key] = (counts[key] || 0) + 1; if (counts[key] <= 5) (fail ? fails : warns).push(`${key}: ${msg}`) }
  const ignSel = '[data-ui-check-ignore]' + (ignore ? `, ${ignore}` : '')
  const ignored = (el) => !!el.closest(ignSel)
  const css = (el) => getComputedStyle(el)
  const label = (n) => {
    const el = n.nodeType === 1 ? n : n.parentElement
    if (!el) return '?'
    const id = el.id ? `#${el.id}` : ''
    const cls = typeof el.className === 'string' && el.className.trim() ? '.' + el.className.trim().split(/\s+/)[0] : ''
    const txt = (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 20)
    return `${el.localName}${id}${cls}${txt ? ` "${txt}"` : ''}`
  }
  const alpha = (c) => {
    const m = c && c.match(/rgba?\(([^)]+)\)|color\(srgb\s+([^)]+)\)/)
    if (!m) return 0
    const p = (m[1] ?? m[2]).split(/[ ,/]+/).filter(Boolean)
    return p.length > 3 ? parseFloat(p[3]) : 1
  }
  const shown = (el) => {
    const r = el.getBoundingClientRect()
    return r.width >= 1 && r.height >= 1 && (!el.checkVisibility || el.checkVisibility({ opacityProperty: true, visibilityProperty: true }))
  }
  const union = (rs) => rs.reduce((u, r) => ({ l: Math.min(u.l, r.l), t: Math.min(u.t, r.t), r: Math.max(u.r, r.r), b: Math.max(u.b, r.b) }), { l: Infinity, t: Infinity, r: -Infinity, b: -Infinity })
  const sx = scrollX, sy = scrollY
  const doc = (r) => ({ l: r.left + sx, t: r.top + sy, r: r.right + sx, b: r.bottom + sy })
  const skipTag = /^(script|style|noscript|template|title|option)$/

  // 화면 읽기 전용 숨김(sr-only): 1~2px 절대 위치, clip rect, clip-path inset(50%). 조상까지 본다.
  const srCache = new Map()
  const srOnly = (el) => {
    if (!el || el === document.body || el === document.documentElement) return false
    if (srCache.has(el)) return srCache.get(el)
    const cs = css(el), r = el.getBoundingClientRect()
    const v = (cs.position === 'absolute' && r.width <= 2 && r.height <= 2) || cs.clip.startsWith('rect') || /inset\(50%/.test(cs.clipPath) || srOnly(el.parentElement)
    srCache.set(el, v); return v
  }
  // 이 요소 글자를 자르는 상자들(overflow ≠ visible). hard = hidden·clip(스크롤로도 못 봄), soft = 말줄임·줄 수 제한.
  // shortcut: 절대·고정 위치로 조상 밖에 나간 요소도 조상이 자른다고 본다, 헛경보가 나오면 containing block 을 따라간다.
  const clipCache = new Map()
  const clipOf = (el) => {
    if (!el || el === document.body || el === document.documentElement) return []
    if (clipCache.has(el)) return clipCache.get(el)
    const list = [...clipOf(el.parentElement)]
    const cs = css(el)
    if (cs.overflowX !== 'visible' || cs.overflowY !== 'visible') {
      const r = el.getBoundingClientRect(), l = r.left + sx + el.clientLeft, t = r.top + sy + el.clientTop
      list.push({ el, box: { l, t, r: l + el.clientWidth, b: t + el.clientHeight }, hard: /hidden|clip/.test(cs.overflowX + cs.overflowY), soft: cs.textOverflow === 'ellipsis' || cs.webkitLineClamp !== 'none' })
    }
    clipCache.set(el, list); return list
  }

  // 글자 잎: 직접 글자 노드를 가진 보이는 요소. 장식(aria-hidden)·sr-only 는 뺀다.
  // rects 는 자르는 상자 안에 실제로 보이는 부분만 남긴다. 통째로 가려진 글자(넘기는 판·접힌 칸)는 화면에 없는 것으로 본다.
  const leaves = []
  for (const el of [root, ...root.querySelectorAll('*')]) {
    if (skipTag.test(el.localName) || ignored(el) || !shown(el) || el.closest('[aria-hidden="true"]') || srOnly(el)) continue
    const nodes = [...el.childNodes].filter((n) => n.nodeType === 3 && n.textContent.trim())
    if (!nodes.length) continue
    const rects = []
    for (const n of nodes) {
      const rg = document.createRange(); rg.selectNodeContents(n)
      for (const r of rg.getClientRects()) if (r.width >= 1 && r.height >= 1) rects.push(doc(r))
    }
    const clips = clipOf(el), vis = []
    let cut = null
    for (const r of rects) {
      let v = r
      for (const c of clips) v = { l: Math.max(v.l, c.box.l), t: Math.max(v.t, c.box.t), r: Math.min(v.r, c.box.r), b: Math.min(v.b, c.box.b) }
      if (v.r - v.l < 1 || v.b - v.t < 1) continue
      vis.push(v)
      // 보이다 만 글자: hidden·clip 칸에 말줄임 없이 잘림. 여러 줄 글의 아랫줄만 잘린 것은 일부러 접은 것으로 본다.
      for (const c of clips) {
        if (cut || !c.hard || c.soft) continue
        const side = Math.max(c.box.l - r.l, r.r - c.box.r), vert = rects.length === 1 ? Math.max(c.box.t - r.t, r.b - c.box.b) : 0
        if (Math.max(side, vert) > 1) cut = { by: c.el, over: Math.max(side, vert) }
      }
    }
    if (vis.length) leaves.push({ el, rects: vis, box: union(vis), text: nodes.map((n) => n.textContent).join('').trim(), cut, fs: parseFloat(css(el).fontSize) })
  }

  // 1. 가로 스크롤 — 폰 폭에서 가장 흔한 고장.
  const vw = document.documentElement.clientWidth
  if (document.documentElement.scrollWidth > vw + 1) {
    const culprits = []
    for (const el of document.body.querySelectorAll('*')) {
      if (culprits.length >= 3) break
      if (skipTag.test(el.localName) || ignored(el) || !shown(el)) continue
      if (el.getBoundingClientRect().right + sx <= vw + 1) continue
      let clippedBy = false
      for (let a = el.parentElement; a && a !== document.body; a = a.parentElement) if (css(a).overflowX !== 'visible') { clippedBy = true; break }
      if (clippedBy || [...el.children].some((c) => c.getBoundingClientRect().right + sx > vw + 1)) continue
      culprits.push(`${label(el)} 오른쪽 끝 ${Math.round(el.getBoundingClientRect().right + sx)}px`)
    }
    push(true, 'h-scroll', `페이지 폭 ${document.documentElement.scrollWidth}px 가 화면 ${vw}px 보다 넓어 가로 스크롤이 생긴다. 넘친 것: ${culprits.join(', ') || '찾지 못함'} — min-width: 0, overflow-wrap: anywhere, 고정 폭 대신 max-width`)
  }

  // 2. 글자 잘림 — hidden·clip 칸에 말줄임 없이 보이다 만 글자.
  for (const { el, cut } of leaves) if (cut) push(true, 'clipped', `${label(el)} 글자가 ${label(cut.by).split(' "')[0]} 에 ${Math.round(cut.over)}px 잘린다 — 칸을 넓히거나 줄바꿈하거나, 일부러 줄이면 text-overflow: ellipsis`)

  // 3·4. 시작선 — 패널(테두리·배경·그림자가 있는 상자, 구역 태그)마다 줄 첫머리 x 를 모은다.
  const panelTag = /^(section|article|aside|nav|header|footer|main|form|fieldset|dialog)$/
  const isPanel = (el) => {
    if (el === root || panelTag.test(el.localName)) return true
    const cs = css(el)
    const border = ['Top', 'Right', 'Bottom', 'Left'].some((s) => parseFloat(cs[`border${s}Width`]) > 0 && cs[`border${s}Style`] !== 'none')
    return border || alpha(cs.backgroundColor) > 0 || cs.boxShadow !== 'none'
  }
  const panelOf = (el) => { for (let a = el.parentElement; a; a = a.parentElement) { if (isPanel(a)) return a; if (a === root) return root } return root }
  const centered = (el) => {
    const cs = css(el)
    if (/center|right|end/.test(cs.textAlign) && cs.textAlign !== 'start') return true
    const p = el.parentElement && css(el.parentElement)
    if (!p) return false
    if (p.display.includes('flex')) {
      const col = p.flexDirection.startsWith('column')
      return col ? /center|end/.test(p.alignItems) : /center|end|space/.test(p.justifyContent)
    }
    return p.display.includes('grid') && /center|end/.test(p.justifyItems)
  }
  const starters = []
  for (const lf of leaves) if (!centered(lf.el)) starters.push({ el: lf.el, x: lf.rects[0].l, t: lf.rects[0].t, b: lf.rects[0].b, fs: lf.fs })
  for (const el of root.querySelectorAll('svg, img, input, select, textarea')) {
    if (ignored(el) || !shown(el) || el.parentElement?.closest('svg')) continue
    const r = doc(el.getBoundingClientRect()); starters.push({ el, x: r.l, t: r.t, b: r.b, mark: true })
  }
  const panels = new Map()
  for (const s of starters) { const p = panelOf(s.el); if (!panels.has(p)) panels.set(p, []); panels.get(p).push(s) }
  for (const [p, items] of panels) {
    const list = items.slice(0, 300)
    // 줄 첫머리: 같은 줄(세로로 겹침)에 더 왼쪽 것이 없다.
    const firsts = list.filter((a) => !a.mark && !list.some((b) => b !== a && b.x < a.x - 1 && Math.min(a.b, b.b) - Math.max(a.t, b.t) > 2))
    const xs = [...new Set(firsts.map((f) => Math.round(f.x * 2) / 2))].sort((a, b) => a - b)
    // 크기가 1.4배 넘게 다른 글자(큰 제목 대 본문)는 일부러 광학 보정하기도 해서 비교하지 않는다.
    near: for (let i = 0; i < firsts.length; i++) for (let j = i + 1; j < firsts.length; j++) {
      const a = firsts[i], b = firsts[j], d = Math.abs(a.x - b.x)
      if (d > 1 && d <= 4 && Math.max(a.fs, b.fs) / Math.min(a.fs, b.fs) < 1.4) {
        push(true, 'near-aligned', `${label(a.el)} 와 ${label(b.el)} 의 시작선이 ${d.toFixed(1)}px 어긋난다(${label(p).split(' "')[0]} 안) — 같은 선에 맞추거나, 들여쓰기면 뚜렷하게(아이콘 폭 + 간격)`)
        break near
      }
    }
    if (p === root || p.closest('table, [role="table"], [role="grid"], pre, code')) continue
    const groups = []
    for (const x of xs) if (!groups.length || x - groups[groups.length - 1] > 2) groups.push(x)
    if (groups.length > 3) push(false, 'start-lines', `${label(p).split(' "')[0]} 안 글자 시작선이 ${groups.length}개다(${groups.map((x) => Math.round(x - p.getBoundingClientRect().left - sx)).join('·')}px) — 패널당 3개 이하가 정상`)
  }

  // 5. 단위 줄바꿈 — 숫자와 단위가 두 줄로 갈라짐.
  const NUMUNIT = /^[-+−]?[\d,.]+\s*(%|[A-Za-z가-힣㎡㎥℃°/]{1,6})$/, NUM = /^[-+−]?[\d,]+(\.\d+)?$/, UNIT = /^(%|[A-Za-z가-힣㎡㎥℃°/]{1,6})$/
  for (const { el, rects, box, text } of leaves) {
    const tops = [...new Set(rects.map((r) => Math.round(r.t)))]
    const lineH = rects[0].b - rects[0].t
    if (NUMUNIT.test(text) && tops.length > 1 && Math.max(...tops) - Math.min(...tops) > lineH / 2) push(true, 'unit-wrapped', `${label(el)} 숫자와 단위가 두 줄로 갈렸다 — white-space: nowrap 으로 묶거나 칸을 넓힌다`)
    else if (NUM.test(text)) {
      const nx = el.nextElementSibling
      if (nx && shown(nx) && UNIT.test((nx.textContent || '').trim()) && nx.getBoundingClientRect().top + sy >= box.b - 2) push(true, 'unit-wrapped', `${label(el)} 다음 단위 ${label(nx)} 가 아랫줄로 떨어졌다 — 두 요소를 nowrap 으로 묶는다`)
    }
  }

  // 6. 글자 크기 종류 — 한 화면(창 높이 한 판)에 크기가 많으면 전부 중간 크기라 위계가 사라진다.
  // 규칙은 5종 이하. 잘 만든 화면(shadcn 대시보드·GitHub·Linear, 2026-11-04 측정)도 6~7종이라 6~7은 경고, 8 이상만 실패.
  const bands = new Map()
  for (const { box, fs } of leaves) { const k = Math.floor(box.t / innerHeight); if (!bands.has(k)) bands.set(k, new Set()); bands.get(k).add(Math.round(fs * 2) / 2) }
  let worst = null
  for (const [k, set] of bands) if (!worst || set.size > worst.set.size) worst = { k, set }
  if (worst && worst.set.size > 5) push(worst.set.size >= 8, 'font-sizes', `${worst.k + 1}번째 화면(위에서 ${worst.k * innerHeight}px부터)에 글자 크기가 ${worst.set.size}종이다(${[...worst.set].sort((a, b) => b - a).join('·')}px) — 한 화면 5종 이하로 줄인다`)

  // 7. 그려진 뒤 밀림 — 늦게 온 데이터가 아래를 민다. 기준은 Web Vitals CLS 「좋음」 0.1.
  const shifts = window.__uiShifts || []
  const cls = shifts.reduce((s, e) => s + e.value, 0)
  if (cls > 0.1) {
    const big = shifts.slice().sort((a, b) => b.value - a.value)[0]
    push(true, 'layout-shift', `화면이 그려진 뒤 밀렸다(CLS ${cls.toFixed(3)}, 기준 0.1). 밀린 것: ${big.nodes.slice(0, 3).map(label).join(', ') || '모름'} — 늦게 오는 자리의 높이를 미리 잡는다`)
  }

  // 8. 좌우 여백 불균형(경고) — 내용에 맞춰 줄어든 버튼의 왼쪽·오른쪽 안쪽 여백이 다름.
  for (const el of root.querySelectorAll('button, [role="button"]')) {
    if (ignored(el) || !shown(el)) continue
    const cs = css(el)
    if (alpha(cs.backgroundColor) === 0 && !(parseFloat(cs.borderLeftWidth) > 0 && cs.borderLeftStyle !== 'none')) continue
    // CSS 로 그린 점·아이콘(::before·::after)은 상자를 잴 수 없어 넘긴다.
    if (['::before', '::after'].some((p) => { const ps = getComputedStyle(el, p); return ps.content !== 'none' && ps.content !== 'normal' && ps.display !== 'none' })) continue
    // 내용 = 보이는 글자 + 아이콘·그림 + 자기 배경·테두리가 있는 안쪽 상자(단축키 칩 등). sr-only 는 leaves 에서 이미 빠졌다.
    const parts = leaves.filter((lf) => el.contains(lf.el)).flatMap((lf) => lf.rects)
    for (const d of el.querySelectorAll('*')) {
      if (!shown(d) || d.parentElement.closest('svg') || srOnly(d) || d.closest('[aria-hidden="true"]') && d.localName !== 'svg') continue
      const ds = css(d)
      if (/^(svg|img)$/.test(d.localName) || alpha(ds.backgroundColor) > 0 || (parseFloat(ds.borderLeftWidth) > 0 && ds.borderLeftStyle !== 'none')) parts.push(doc(d.getBoundingClientRect()))
    }
    if (!parts.length) continue
    const ud = union(parts), u = { l: ud.l - sx, r: ud.r - sx }, r = el.getBoundingClientRect()
    const pad = parseFloat(cs.paddingLeft) + parseFloat(cs.paddingRight) + parseFloat(cs.borderLeftWidth) + parseFloat(cs.borderRightWidth)
    const slack = r.width - (u.r - u.l) - pad
    const centeredInside = cs.display.includes('flex') || cs.display.includes('grid') ? /center/.test(cs.justifyContent) : cs.textAlign === 'center'
    if (slack > 2 && !centeredInside) continue // 늘어난 왼쪽 정렬 버튼은 일부러 그렇다
    const l = u.l - r.left, rr = r.right - u.r, hi = Math.max(l, rr), lo = Math.min(l, rr)
    if (u.r - u.l > r.width) continue // 넘친 글자는 clipped 가 잡는다
    if (hi >= 8 && hi - lo >= 4 && lo >= 0 && hi > lo * 1.5) push(false, 'uneven-inset', `${label(el)} 안쪽 여백이 왼쪽 ${Math.round(l)}px · 오른쪽 ${Math.round(rr)}px 로 다르다 — 버튼·배지는 양쪽을 같게`)
  }

  // 9. 섞인 아이콘(경고) — 한 묶음에 속이 찬 아이콘과 선 아이콘이 함께 있음.
  const small = [...root.querySelectorAll('svg')].filter((s) => {
    if (ignored(s) || !shown(s) || s.parentElement.closest('svg')) return false
    const r = s.getBoundingClientRect(); return r.width <= 40 && r.height <= 40
  })
  const kind = (s) => {
    let f = 0, o = 0
    for (const p of s.querySelectorAll('path, circle, rect, ellipse, polygon, polyline, line')) {
      const c = css(p)
      const filled = c.fill !== 'none' && alpha(c.fill) > 0 && !/^(line|polyline)$/.test(p.localName)
      const stroked = c.stroke !== 'none' && alpha(c.stroke) > 0 && parseFloat(c.strokeWidth) > 0
      if (filled) f++; else if (stroked) o++
    }
    return f + o === 0 ? null : f >= o ? 'filled' : 'outline'
  }
  const smallSet = new Set(small), groupsOf = new Map()
  for (const s of small) {
    let g = null
    for (let a = s.parentElement, d = 0; a && d < 4; a = a.parentElement, d++) if ([...a.querySelectorAll('svg')].filter((x) => smallSet.has(x)).length >= 3) { g = a; break }
    if (!g) continue
    if (!groupsOf.has(g)) groupsOf.set(g, [])
    groupsOf.get(g).push(kind(s))
  }
  for (const [g, ks] of groupsOf) {
    const f = ks.filter((k) => k === 'filled').length, o = ks.filter((k) => k === 'outline').length
    if (f >= 1 && o >= 1 && f + o >= 3) push(false, 'mixed-icons', `${label(g).split(' "')[0]} 안 아이콘이 속 찬 것 ${f}개 · 선 ${o}개로 섞였다 — 한 묶음은 한 모양으로(선택 표시가 목적이면 그대로 두고 넘긴다)`)
  }

  // 10. 글자 겹침 — 마지막에 한다(가려짐을 보려고 스크롤을 움직인다).
  const L = leaves.slice(0, 1500).sort((a, b) => a.box.t - b.box.t)
  const opaque = (el) => { const cs = css(el); return alpha(cs.backgroundColor) >= 0.75 || cs.backdropFilter !== 'none' || /^(img|video|canvas)$/.test(el.localName) }
  for (let i = 0; i < L.length; i++) {
    for (let j = i + 1; j < L.length && L[j].box.t < L[i].box.b; j++) {
      const a = L[i], b = L[j]
      if (a.el.contains(b.el) || b.el.contains(a.el)) continue
      if (Math.min(a.box.r, b.box.r) - Math.max(a.box.l, b.box.l) <= 2) continue
      // 글자 상자는 행간보다 커서 좁은 행간의 위아래 줄이 몇 px 겹친다 — 위아래 20%씩 깎은 몸통만 비교한다.
      const body = (r) => { const d = (r.b - r.t) * 0.2; return { l: r.l, r: r.r, t: r.t + d, b: r.b - d } }
      let k = null
      for (const ra0 of a.rects) { const ra = body(ra0); for (const rb0 of b.rects) {
        const rb = body(rb0)
        const w = Math.min(ra.r, rb.r) - Math.max(ra.l, rb.l), h = Math.min(ra.b, rb.b) - Math.max(ra.t, rb.t)
        if (w > 3 && h > 3) { k = { w, h, x: (Math.max(ra.l, rb.l) + Math.min(ra.r, rb.r)) / 2, y: (Math.max(ra.t, rb.t) + Math.min(ra.b, rb.b)) / 2 }; break }
      } if (k) break }
      if (!k) continue
      // 그 점에서 두 글자가 실제로 겹쳐 그려지는지 본다: 사이에 불투명(또는 흐림 처리한) 층이 있으면
      // 아래 글자는 가려진 것이다(모달·메뉴·고정 머리띠 밑으로 지나가는 글). 마우스를 안 받는 요소는 판단할 수 없어 넘긴다.
      // shortcut: 배지가 글자를 일부 덮는 결함은 못 잡는다, 필요하면 덮는 층의 크기로 따로 본다.
      window.scrollTo(k.x - innerWidth / 2, k.y - innerHeight / 2)
      const stack = document.elementsFromPoint(k.x - scrollX, k.y - scrollY)
      const ia = stack.indexOf(a.el), ib = stack.indexOf(b.el)
      if (ia < 0 || ib < 0) continue
      const [up, lowIdx, low] = ia < ib ? [ia, ib, b] : [ib, ia, a]
      if (stack.slice(up, lowIdx).some((e) => !e.contains(low.el) && opaque(e))) continue
      push(true, 'overlap', `${label(a.el)} 와 ${label(b.el)} 의 글자가 ${Math.round(k.w)}×${Math.round(k.h)}px 겹친다 — 위치(absolute)·음수 여백을 확인한다`)
    }
  }
  window.scrollTo(sx, sy)

  for (const [key, n] of Object.entries(counts)) if (n > 5) {
    const list = fails.some((f) => f.startsWith(key + ':')) ? fails : warns
    list.push(`${key}: 같은 결함 ${n - 5}건 더`)
  }
  return { fails, warns }
}

const opts = parseArgs(process.argv.slice(2))
if (!opts.url || !opts.widths.length) {
  console.error('쓰는 법: node ui-check.mjs <URL|HTML 파일> [--widths 1440,390] [--select <css>] [--ignore <css>] [--out shots] [--wait 1000]')
  process.exit(2)
}
const url = /^[a-z][a-z0-9+.-]*:\/\//i.test(opts.url) ? opts.url : pathToFileURL(resolve(opts.url)).href
const pw = findPlaywright()
if (!pw) {
  console.error('Playwright 를 찾지 못했다. 프로젝트에서 `npm i -D playwright` 하거나, `npx -y -p playwright node ui-check.mjs <URL>` 로 돌린다.')
  process.exit(2)
}
let browser
try { browser = await launch(pw) } catch (e) {
  console.error(`브라우저를 열지 못했다: ${e.message}\n\`npx playwright install chromium\` 을 한 번 돌린다.`)
  process.exit(2)
}
mkdirSync(opts.out, { recursive: true })
const slug = (basename(new URL(url).pathname).replace(/\.[a-z]+$/i, '') || 'index').replace(/[^\w가-힣-]/g, '_')
let fails = 0, warns = 0
for (const w of opts.widths) {
  const h = w <= 480 ? 844 : 900
  const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 })
  await page.addInitScript(shiftRecorder)
  try {
    await page.goto(url, { waitUntil: 'load', timeout: 30000 })
    await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {})
    await page.evaluate(() => document.fonts && document.fonts.ready)
    await page.waitForTimeout(opts.wait)
  } catch (e) {
    console.error(`페이지를 열지 못했다(${w}px): ${String(e.message).split('\n')[0]}`)
    await browser.close(); process.exit(2)
  }
  const shot = join(opts.out, `${slug}-${w}.png`)
  await page.screenshot({ path: shot, fullPage: true })
  const r = await page.evaluate(audit, { select: opts.select, ignore: opts.ignore })
  console.log(`== ${w}x${h}  ${shot}`)
  for (const f of r.fails) console.log(`실패 ${f}`)
  for (const x of r.warns) console.log(`경고 ${x}`)
  fails += r.fails.length; warns += r.warns.length
  await page.close()
}
await browser.close()
console.log(fails ? `ui-check failed: 실패 ${fails} · 경고 ${warns}` : `ui-check passed: 실패 0 · 경고 ${warns}`)
process.exit(fails ? 1 : 0)
