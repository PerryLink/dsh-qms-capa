# Changelog

## [0.1.0-alpha.13] — 2026-11-01

### Security / Fixes

- Release configuration hardening: wider host peer range and a build step before publish.


### Added

- `qms.capa_effectiveness`: close-readiness review for a CAPA — state gate, overdue flag and a recurrence blocker when the NCR is a repeat, per ISO 9001:2015 10.2's effectiveness expectation. Verified by `node --test test/*.test.mjs` (13/13).

## [Unreleased]

### Added

- `qms.8d_check`: read-only completeness check for an 8D record — missing or too-thin D1-D8 disciplines and a `ready_to_close` verdict, aligned with the ISO 9001:2015 10.2 corrective-action expectation. Verified by `node --test test/*.test.mjs` (9/9).

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
