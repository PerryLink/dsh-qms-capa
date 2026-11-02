import test from 'node:test'
import assert from 'node:assert/strict'
import { createTools } from '../lib/plugin/tools.js'

class T { map = new Map(); get(k){return this.map.get(k)}; entries(){return this.map.entries()}; get size(){return this.map.size}; async put(k,v){this.map.set(k,v)} }

async function setup() {
  const ncrs = new T()
  await ncrs.put('N1', { ncr_id: 'N1', plant: 'P1', material: 'M1', lot: 'L1', defect_code: 'D1', found_date: '2026-01-01' })
  const tools = createTools({ ncrs, aliases: new T(), capas: new T(), eightd: new T() })
  return Object.fromEntries(tools.map((t) => [t.name, t]))
}

test('a fresh 8D reports all eight disciplines missing', async () => {
  const by = await setup()
  const opened = await by['qms.8d'].execute({ action: 'open', ncr_id: 'N1' }, { callId: 'q' })
  const r = await by['qms.8d_check'].execute({ eightd_id: opened.eightd_id }, { callId: 'q' })
  assert.equal(r.missing.length, 8)
  assert.equal(r.ready_to_close, false)
  assert.equal(r.state, 'd1')
})

test('filled disciplines make the report closeable; thin content is flagged', async () => {
  const by = await setup()
  const opened = await by['qms.8d'].execute({ action: 'open', ncr_id: 'N1' }, { callId: 'q' })
  const filled = { d1: 'Team formed with quality and production', d2: 'Lot 12 rejected at incoming inspection', d3: 'Stock blocked and rework started', d4: 'Root cause is a worn die guide pin', d5: 'Replace guide pin and adjust maintenance interval', d6: 'Verified on 3 lots with zero defects', d7: 'Updated the preventive maintenance standard', d8: 'Closed with customer acknowledgement' }
  for (const [discipline, content] of Object.entries(filled)) {
    await by['qms.8d'].execute({ action: 'update', eightd_id: opened.eightd_id, discipline, content }, { callId: 'q' })
  }
  const full = await by['qms.8d_check'].execute({ eightd_id: opened.eightd_id }, { callId: 'q' })
  assert.equal(full.missing.length, 0)
  assert.equal(full.ready_to_close, true)
  await by['qms.8d'].execute({ action: 'update', eightd_id: opened.eightd_id, discipline: 'd4', content: 'pin' }, { callId: 'q' })
  const thin = await by['qms.8d_check'].execute({ eightd_id: opened.eightd_id }, { callId: 'q' })
  assert.deepEqual(thin.thin, ['d4'])
  assert.equal(thin.ready_to_close, false)
})

test('unknown 8D id is rejected', async () => {
  const by = await setup()
  await assert.rejects(() => by['qms.8d_check'].execute({ eightd_id: 'nope' }, { callId: 'q' }), (error) => error.code === 'E_QMS_RECORD_NOT_FOUND' && /｜下一步：/.test(error.message))
})
