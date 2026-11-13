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

test('CAPA open/classify/advance', async () => {
  const tools = createTools({ ncrs: new T(), aliases: new T(), capas: new T() })
  const by = Object.fromEntries(tools.map((tool) => [tool.name, tool]))
  const ncr = await by['qms_ncr'].execute({ ncrs: [{ plant: 'P1', material: 'M1', lot: 'L1', defect_code: 'D1', found_date: '2026-01-01', quantity: 1 }] }, { callId: 'c' })
  const capa = await by['qms_capa'].execute({ action: 'open', ncr_id: ncr.ncrs[0], grade: 'A' }, { callId: 'c' })
  assert.equal(capa.state, 'opened')
  const classified = await by['qms_capa'].execute({ action: 'classify', capa_id: capa.capa_id, grade: 'C' }, { callId: 'c' })
  assert.equal(classified.grade, 'C')
  const advanced = await by['qms_capa'].execute({ action: 'advance', capa_id: capa.capa_id }, { callId: 'c' })
  assert.equal(advanced.state, 'contained')
})

test('CAPA unknown NCR rejected', async () => {
  const tools = createTools({ ncrs: new T(), aliases: new T(), capas: new T() })
  const capa = tools.find((tool) => tool.name === 'qms_capa')
  await assert.rejects(() => capa.execute({ action: 'open', ncr_id: 'missing' }, { callId: 'c' }))
})
