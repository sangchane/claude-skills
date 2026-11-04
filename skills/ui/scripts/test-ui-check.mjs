#!/usr/bin/env node
// ui-check.mjs 자체 시험 — 나쁜 견본은 검사 이름이 다 나오고 실패(1), 좋은 견본은 실패·경고 없이 통과(0).  node scripts/test-ui-check.mjs
import { spawnSync } from 'node:child_process'
import { mkdtempSync, rmSync, existsSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'
import os from 'node:os'

const here = dirname(fileURLToPath(import.meta.url))
const out = mkdtempSync(join(os.tmpdir(), 'ui-check-'))
const run = (name) => spawnSync(process.execPath, [join(here, 'ui-check.mjs'), join(here, 'ui-check-fixtures', name), '--out', out], { encoding: 'utf8' })
let ok = 0, total = 0
const check = (what, cond, detail = '') => { total++; if (cond) ok++; else console.log(`실패: ${what}${detail ? `\n${detail}` : ''}`) }

const bad = run('bad.html')
if (bad.status === 2) { console.log(bad.stderr); process.exit(2) }
check('나쁜 견본은 종료 1', bad.status === 1, bad.stdout + bad.stderr)
for (const name of ['h-scroll', 'overlap', 'clipped', 'near-aligned', 'unit-wrapped', 'font-sizes', 'layout-shift']) check(`실패 ${name}`, bad.stdout.includes(`실패 ${name}:`))
for (const name of ['uneven-inset', 'mixed-icons', 'start-lines']) check(`경고 ${name}`, bad.stdout.includes(`경고 ${name}:`))
check('폭마다 스크린샷', existsSync(join(out, 'bad-1440.png')) && existsSync(join(out, 'bad-390.png')))
check('h-scroll 은 390 에서만', !bad.stdout.split('== 390')[0].includes('h-scroll'))

const good = run('good.html')
check('좋은 견본은 종료 0', good.status === 0, good.stdout + good.stderr)
check('좋은 견본은 실패·경고 없음', !/^(실패|경고) /m.test(good.stdout), good.stdout)

rmSync(out, { recursive: true, force: true })
console.log(`ok ${ok}/${total}`)
process.exit(ok === total ? 0 : 1)
