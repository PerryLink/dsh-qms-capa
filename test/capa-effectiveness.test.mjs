import test from 'node:test'
import assert from 'node:assert/strict'
import { createTools } from '../lib/plugin/tools.js'

class T { map = new Map(); get(k){return this.map.get(k)}; entries(){return this.map.entries()}; get size(){return this.map.size}; async put(k,v){this.map.set(k,v)} }

async function setup({ recurrence = false, dueDate = '2026-12-31', state = 'opened' } = {}) {
  const ncrs = new T(); const capas = new T(); const eightd = new T()
  await ncrs.put('N1', { ncr_id: 'N1', plant: 'P1', material: 'M1', lot: 'L1', defect_code: 'D1', found_date: '2026-01-01', quantity: 1, source: 'audit', ...(recurrence ? { recurrence_of: 'N0' } : {}) })
  await capas.put('C1', { capa_id: 'C1', ncr_id: 'N1', grade: 'A', owner: 'qa', due_date: dueDate, state, created_at: '2026-01-01T00:00:00Z', updated_at: '2026-01-01T00:00:00Z' })
  const tools = createTools({ ncrs, aliases: new T(), capas, eightd })
  return Object.fromEntries(tools.map((t) => [t.name, t]))
}

test('an opened CAPA is not closeable', async () => {
  const by = await setup()
  const r = await by['qms.capa_effectiveness'].execute({ capa_id: 'C1' }, { callId: 'c' })
  assert.equal(r.ready_to_close, false)
  assert.ok(r.blockers.includes('state_not_verified'))
  assert.equal(r.overdue, false)
})

test('a verified CAPA is closeable and a past due date is overdue', async () => {
  const ok = await setup({ state: 'verified' })
  const r = await ok['qms.capa_effectiveness'].execute({ capa_id: 'C1' }, { callId: 'c' })
  assert.equal(r.ready_to_close, true)
  assert.deepEqual(r.blockers, [])
  const late = await setup({ state: 'corrective', dueDate: '2020-01-01' })
  const lateRes = await late['qms.capa_effectiveness'].execute({ capa_id: 'C1' }, { callId: 'c' })
  assert.equal(lateRes.overdue, true)
  assert.ok(lateRes.blockers.includes('overdue'))
})

test('a recurring NCR blocks closure until effectiveness is verified', async () => {
  const by = await setup({ recurrence: true, state: 'corrective' })
  const r = await by['qms.capa_effectiveness'].execute({ capa_id: 'C1' }, { callId: 'c' })
  assert.ok(r.blockers.includes('recurrence_needs_effectiveness'))
  assert.equal(r.ready_to_close, false)
})

test('unknown CAPA is rejected', async () => {
  const by = await setup()
  await assert.rejects(() => by['qms.capa_effectiveness'].execute({ capa_id: 'nope' }, { callId: 'c' }), (error) => error.code === 'E_QMS_RECORD_NOT_FOUND' && /｜下一步：/.test(error.message))
})
