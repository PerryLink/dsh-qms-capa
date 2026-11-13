# Changelog

## [0.2.0] — 2026-11-13

### Breaking

- **Tool names now use underscores (`qms_*`) instead of dots.** The provider
  validates every `tools[].name` against `^[a-zA-Z0-9_-]+$`; a single dot makes
  it reject the entire `tools` array, so the 0.1.x dotted surface could register
  locally but never reach a model. All seven registered names now use `qms_`
  plus the same suffix as before: `ncr`, `batch_alias`, `impact`, `capa`, `8d`,
  `8d_check`, `capa_effectiveness` — that is, `qms_ncr`, `qms_batch_alias`,
  `qms_impact`, `qms_capa`, `qms_8d`, `qms_8d_check`, `qms_capa_effectiveness`.
  No dotted aliases or shims are kept.
- Update prompts, scripts, saved tool references and integrations to the
  underscore names. This is a breaking change to the tool surface, shipped as a
  minor bump under the 0.1.0 compatibility promise.

### Added

- `test/tool-name-wire.test.mjs`: regression test asserting every registered
  tool name matches `^[a-zA-Z0-9_-]+$`, contains no dot, and is unique.

### Changed

- Five-language READMEs, troubleshooting, docs diagrams, the quickstart sample
  and earlier release notes now use the underscore names.
- The README compatibility tables document the provider wire-name constraint and
  the 0.2.0 rename.

## [0.1.0] — 2026-11-03

### Stable

- First non-alpha release: tool names and the CLI surface are covered by a
  compatibility promise (breaking changes require a minor bump).
- Ships a quickstart sample, a one-line prompt, a permission block and real captures.

## [0.1.0] — 2026-11-01

### Security / Fixes

- Release configuration hardening: wider host peer range and a build step before publish.


### Added

- `qms_capa_effectiveness`: close-readiness review for a CAPA — state gate, overdue flag and a recurrence blocker when the NCR is a repeat, per ISO 9001:2015 10.2's effectiveness expectation. Verified by `node --test test/*.test.mjs` (13/13).

## [Unreleased]

### Added

- `qms_8d_check`: read-only completeness check for an 8D record — missing or too-thin D1-D8 disciplines and a `ready_to_close` verdict, aligned with the ISO 9001:2015 10.2 corrective-action expectation. Verified by `node --test test/*.test.mjs` (9/9).

## [0.1.0-alpha.8] — 2026-11-01

### Changed

- Documentation: five-language fixture/acceptance links now resolve on npm; added specific related-checker/tool links.
- Marketplace metadata: taxonomy category, archetype, domains and status; docs page now shows the same.

All notable changes to `dsh-qms-capa` are documented here. The format follows Keep a Changelog; this project uses alpha versions.

## [0.1.0-alpha.7] — 2026-11-01

### Added

- Five-language READMEs: English, 简体中文, Español, Português, हिन्दी.
- Local workflow SVG at `docs/assets/dsh-qms-capa-flow.svg`.
- Family cross-links (domain index, checker family, `dsh-kit`), compatibility, permissions, and related-work sections.
- Standard repository files: `SECURITY.md`, `PRIVACY.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, and `icon.svg`.

### Changed

- README aligned with the PerryLink DSH checker/plugin family style; package remains public/synthetic, alpha, not GA.

### Maintenance

- 2026-11-01: active again — feature work, hardening and fresh evidence resumed.

## [Earlier]

Earlier alpha builds are available from npm and GitHub Releases; this file starts at the family-standard documentation wave.
