# dsh-qms-capa

> 🧊 **FROZEN — 2026-10-31. No new features.** This public/synthetic S1 demo is not GA; it stays installable and only genuine breakage is fixed.

## Maintenance status: 🧊 FROZEN

Frozen on 2026-10-31. This repository is a public/synthetic S1 demo, not a validated product. The npm package stays installable; no new features are planned.


QMS NCR ingest, batch alias resolution, impact evaluation, CAPA and 8D state for DeepSeek Harness.

> **Status: alpha / public-synthetic / partial / not counted / not GA.** No customer evidence, customer data, or production-readiness claim. All acceptance rows are `counted=false`.

## Install

```sh
dsh plugin --profile <profile> add dsh-qms-capa
dsh --profile <profile> --dump-config | grep dsh-qms-capa
```

Requires DSH `>=0.2.1-rc.3 <0.3.0` and Node `>=24.9 <25`.

<details>
<summary>中文摘要</summary>

QMS NCR 入库、批次别名、影响评估、CAPA 与 8D。 安装：`dsh plugin --profile <profile> add dsh-qms-capa`。公开/合成、alpha、非 GA。

</details>

## Tools

| Tool | What it does | Risk |
|---|---|---|
| `qms.ncr` | Ingest and dedupe NCR rows | R1 local write |
| `qms.batch_alias` | Resolve batch aliases | R0 |
| `qms.impact` | Evaluate affected batches/orders | R0 |
| `qms.capa` | Open/classify/advance a CAPA | R1 local write |
| `qms.8d` | Track D1–D8 evidence and state | R1 local write |

## Input / output

**Input:** NCR rows and batch aliases. **Output:** an impact report, CAPA state, and D1–D8 8D evidence/state. The package records local state; it does not operate a full QMS.

## Limits / non-claims

- No full CAPA/8D ledger, approval workflow, e-signature, or Client surface.
- No ERP/MES integration and no automatic disposition.
- One MIT redacted NCR sample only; no customer plant data.
- No customer evidence, customer data, or production-readiness claim; all fixtures are public/synthetic.

## Public sample

MIT redacted NCR sample; `ACCEPTANCE.csv` lists 6 public checks.

## Development

```sh
pnpm install --frozen-lockfile
pnpm build && pnpm lint && pnpm typecheck && pnpm test && pnpm gate:sku08
```

## License

Apache-2.0. See `LICENSE`, `NOTICE`, `THIRD-PARTY-NOTICES`.
