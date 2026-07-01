# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-07-01

### Added

- Unified skill name to `lingqi` across all files
- Cross-platform installation guide (Hermes Agent, Claude Code, Codex, OpenCode)
- `CHANGELOG.md` for version tracking
- Enhanced README with badges, feature table, and project structure

### Changed

- Bumped version from 1.1.0 to 1.2.0
- Updated SKILL.md description with Chinese name prefix
- Renamed trigger from `$prompt-optimizer` to `$lingqi`

### Fixed

- Resolved SKILL.md name mismatch between local and GitHub
- Aligned default branch to `master`

## [1.1.0] - 2026-06-30

### Added

- Initial release of prompt-optimizer skill
- Core optimization workflow (classify → choose mode → optimize → self-check)
- Four output modes: explained, simple, engineering, eval
- Validation scripts: `check_prompt_artifact.py`, `score_prompt_shape.py`
- Reference documents: agent-prompts, anti-patterns, eval-design, model-adapters, output-modes, testing-and-qa
- Known pitfalls documentation (vague_verbs, empty_persona, security scan false positives)

### Added

- MIT License
- Platform support: Linux, macOS, Windows
- Related skills: hermes-agent, systematic-debugging
