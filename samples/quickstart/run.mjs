#!/usr/bin/env node
/**
 * dsh-qms-capa quickstart — runs the built plugin tools over the bundled
 * synthetic NCR batch. The golden file `expected/result.json` is the stdout of
 * `node samples/quickstart/run.mjs --json`, so it is a real run, not hand-written.
 *
 *   node samples/quickstart/run.mjs            # human-readable summary
 *   node samples/quickstart/run.mjs --json     # the golden result on stdout
 *   node samples/quickstart/run.mjs --check    # recompute and diff against the golden file
 */
import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { createTools } from '../../lib/plugin/tools.js'

const here = path.dirname(fileURLToPath(import.meta.url))
const inputDir = path.join(here, 'input')
const expectedPath = path.join(here, 'expected', 'result.json')
const mode = process.argv.includes('--check') ? 'check' : process.argv.includes('--json') ? 'json' : 'summary'

class Table {
  map = new Map()
  get(key) { return this.map.get(key) }
  entries() { return this.map.entries() }
  get size() { return this.map.size }
  async put(key, value) { this.map.set(key, value) }
}

function parseCsv(text) {
  const [header, ...lines] = text.trim().split(/\r?\n/)
  const columns = header.split(',')
  return lines.filter((line) => line.trim()).map((line) => {
    const row = Object.fromEntries(line.split(',').map((value, index) => [columns[index], value]))
    return row
  })
}

async function run() {
  const ncrRows = parseCsv(await readFile(path.join(inputDir, 'ncrs.csv'), 'utf8')).map((row) => ({
    plant: row.plant,
    material: row.material,
    lot: row.lot,
    defect_code: row.defect_code,
    found_date: row.found_date,
    quantity: Number(row.quantity),
    ...(row.source ? { source: row.source } : {}),
    ...(row.recurrence_of ? { recurrence_of: row.recurrence_of } : {}),
  }))
  const aliasRows = parseCsv(await readFile(path.join(inputDir, 'aliases.csv'), 'utf8'))
  const snapshots = JSON.parse(await readFile(path.join(inputDir, 'snapshots.json'), 'utf8'))

  const tools = createTools({ ncrs: new Table(), aliases: new Table(), capas: new Table(), eightd: new Table() })
  const byName = Object.fromEntries(tools.map((tool) => [tool.name, tool]))
  const call = { callId: 'quickstart' }

  const ingest = await byName['qms_ncr'].execute({ ncrs: ncrRows }, call)
  const firstNcr = ingest.ncrs[0]
  const alias = await byName['qms_batch_alias'].execute(
    { action: 'set', alias: aliasRows[0].alias, canonical: aliasRows[0].canonical }, call,
  )
  const impact = await byName['qms_impact'].execute({ ncr_id: firstNcr, snapshots }, call)
  const capa = await byName['qms_capa'].execute({ action: 'open', ncr_id: firstNcr, grade: 'A' }, call)
  const effectiveness = await byName['qms_capa_effectiveness'].execute({ capa_id: capa.capa_id }, call)
  const eightd = await byName['qms_8d'].execute({ action: 'open', ncr_id: firstNcr }, call)
  const eightdCheck = await byName['qms_8d_check'].execute({ eightd_id: eightd.eightd_id }, call)

  return {
    sample: 'samples/quickstart/input/ncrs.csv',
    rows_read: ncrRows.length,
    ncrs_created: ingest.ncrs.length,
    duplicates: ingest.duplicates.length,
    alias: { alias: alias.alias, canonical: alias.canonical },
    impact: {
      canonical_lot: impact.canonical_lot,
      affected_count: impact.affected.length,
      affected_lots: [...new Set(impact.affected)],
      recall_hint: impact.recall_hint,
    },
    capa: { grade: capa.grade, state: capa.state },
    capa_effectiveness: { ready_to_close: effectiveness.ready_to_close, blockers: effectiveness.blockers },
    eightd: {
      state: eightdCheck.state,
      missing: eightdCheck.missing.length,
      thin: eightdCheck.thin.length,
      ready_to_close: eightdCheck.ready_to_close,
    },
  }
}

const result = await run()

if (mode === 'json') {
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`)
} else if (mode === 'check') {
  const expected = JSON.parse(await readFile(expectedPath, 'utf8'))
  assert.deepEqual(result, expected)
  console.log('dsh-qms-capa quickstart - synthetic NCR batch (not real plant data)')
  console.log(`read ${result.rows_read} rows: ${result.ncrs_created} new NCR, ${result.duplicates} duplicates`)
  console.log(`alias ${result.alias.alias} -> ${result.alias.canonical}`)
  console.log(`impact: ${result.impact.affected_count} batch rows hit ${result.impact.canonical_lot} (recall hint: ${result.impact.recall_hint})`)
  console.log(`CAPA grade ${result.capa.grade} ${result.capa.state}; effectiveness blockers: ${result.capa_effectiveness.blockers.join(', ')}`)
  console.log(`8D at ${result.eightd.state}: ${result.eightd.missing} disciplines missing`)
  console.log('golden samples/quickstart/expected/result.json matches')
  console.log('quickstart ok')
} else {
  console.log('dsh-qms-capa quickstart - synthetic NCR batch (not real plant data)')
  console.log(`read ${result.rows_read} rows: ${result.ncrs_created} new NCR, ${result.duplicates} duplicates`)
  console.log(`alias ${result.alias.alias} -> ${result.alias.canonical}`)
  console.log(`impact: ${result.impact.affected_count} batch rows hit ${result.impact.canonical_lot} (recall hint: ${result.impact.recall_hint})`)
  console.log(`CAPA grade ${result.capa.grade} ${result.capa.state}; effectiveness blockers: ${result.capa_effectiveness.blockers.join(', ')}`)
  console.log(`8D at ${result.eightd.state}: ${result.eightd.missing} disciplines missing`)
  console.log('run with --check to compare against expected/result.json')
}
