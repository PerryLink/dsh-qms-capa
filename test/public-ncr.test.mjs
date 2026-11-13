import test from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { createTools } from '../lib/plugin/tools.js'

class T {
  map = new Map()
  get(key) { return this.map.get(key) }
  entries() { return this.map.entries() }
  get size() { return this.map.size }
  async put(key, value) { this.map.set(key, value) }
}

test('public MIT redacted NCR ingest', async () => {
  const csv = readFileSync('fixtures/public/mit/ncr_register.redacted.csv', 'utf8').trim().split('\n')
  const header = csv[0].split(',').map((value) => value.trim())
  const ncrs = csv.slice(1).map((line) => {
    const cells = line.match(/(".*?"|[^,]+)(?=,|$)/g)?.map((value) => value.replace(/^"|"$/g, '').trim()) ?? []
    const row = Object.fromEntries(header.map((key, index) => [key, cells[index] ?? '']))
    return { plant: 'PHX-DC-01', material: row['Linked Equipment'] ?? 'UNKNOWN', lot: row['NCR ID'], defect_code: row['Issue'].slice(0, 24), found_date: '2026-01-01', quantity: 1, source: 'public-mit' }
  })
  const tools = createTools({ ncrs: new T(), aliases: new T() })
  const ncr = tools.find((tool) => tool.name === 'qms_ncr')
  const result = await ncr.execute({ ncrs }, { callId: 'public-ncr' })
  assert.ok(result.ncrs.length >= 3)
  assert.equal(result.duplicates.length, 0)
})
