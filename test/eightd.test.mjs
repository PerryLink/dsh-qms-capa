import test from 'node:test'
import assert from 'node:assert/strict'
import { createTools } from '../lib/plugin/tools.js'

class T {
  map = new Map()
  get(key) { return this.map.get(key) }
  entries() { return this.map.entries() }
  get size() { return this.map.size }
  async put(key, value) { this.map.set(key, value) }
}

test('8D open/update/advance D1→D2', async () => {
  const tools = createTools({ ncrs: new T(), aliases: new T(), capas: new T(), eightd: new T() })
  const by = Object.fromEntries(tools.map((tool) => [tool.name, tool]))
  const ncr = await by['qms.ncr'].execute({ ncrs: [{ plant: 'P1', material: 'M1', lot: 'L1', defect_code: 'D1', found_date: '2026-01-01', quantity: 1 }] }, { callId: '8d' })
  const d = await by['qms.8d'].execute({ action: 'open', ncr_id: ncr.ncrs[0] }, { callId: '8d' })
  assert.equal(d.state, 'd1')
  await by['qms.8d'].execute({ action: 'update', eightd_id: d.eightd_id, discipline: 'd1', content: 'team' }, { callId: '8d' })
  const advanced = await by['qms.8d'].execute({ action: 'advance', eightd_id: d.eightd_id }, { callId: '8d' })
  assert.equal(advanced.state, 'd2')
})
