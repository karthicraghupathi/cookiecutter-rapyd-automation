# Changelog

All notable changes to this project will be documented in this file. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- Pre-generation hook (`hooks/pre_gen_project.py`) that fails fast on invalid `project_slug` (non-identifier or Python keyword), TOML-unsafe characters in `author_name` / `project_description`, and malformed `author_email`.
- Ruff `S` (bandit) security rules enabled with targeted ignores in both root and generated configs.
- Test coverage expanded from 15 to 26 tests: invalid slug rejection, Python-keyword slug rejection, quote/newline-in-author rejection, malformed email rejection, quote-in-email rejection, quote-in-project_name rejection, non-ASCII author rendering, `requirements.txt` / `requirements-dev.txt` content assertions, unknown-license failure, `.licenses/` staging cleanup verification.
- `LOG_LEVEL` validation in generated `settings.py` — invalid values fall back to INFO with a warning printed to stderr.
- AGENTS.md at repo root and inside generated projects.
- CONTRIBUTING.md and CHANGELOG.md.
- Generated `.env.example` documenting `LOG_LEVEL`.
- Generated `Makefile` with `lint` / `format` / `test` / `run` targets.
- Generated `tests/` directory with smoke test.
- License choice prompt (MIT, Apache-2.0, BSD-3-Clause, Proprietary). License templates ship inside the rendered tree at `.licenses/` (with `_copy_without_render`) and the post-gen hook substitutes `{author_name}` and `{current_year}` into the chosen template.
- Cookiecutter prompts: `author_name`, `author_email`.
- `python_version` is now a choice list (3.10, 3.11, 3.12, 3.13; default 3.12).
- Comprehensive test suite (15 tests) that bakes the template and runs ruff + pytest on the result, parametrized over Python versions and license choices.
- Test that the post-gen hook fails gracefully when `uv` is unavailable.

### Changed
- **Replaced pipenv with uv** in both the template repo and generated projects.
- **Replaced black + isort + flake8 with ruff** in both repos.
- Generated `src/` is now a proper package layout: `src/<slug>/` with `__init__.py` and `__main__.py`. Run via `uv run python -m <slug>` or `make run`.
- Generated `pyproject.toml` is now uv-native (proper `[project]` table, `[dependency-groups].dev`, `[tool.ruff]`, `[tool.pytest.ini_options]`).
- Post-generation hook ported from bash to Python (cross-platform — works on Windows without WSL).
- Generated `.gitignore` slimmed from 200+ lines (toptal-generated) to ~20 focused lines.
- Generated `.pre-commit-config.yaml` is now an independent file (no longer a symlink to the root config). Ruff hooks replace black/isort/flake8.
- `readme.md` renamed to `README.md` (uppercase).
- Generated logger no longer prefixes with `PROJECT_SLUG` — the package layout already namespaces names via `__name__`.

### Removed
- `Pipfile`, `Pipfile.lock`, `requirements.txt`, `requirements-dev.txt`, `.flake8` at root.
- Generated `Pipfile`, `setup_env.sh`, `.flake8`.
- The custom `pipenv-requirements-pre-commit` hook (replaced by `astral-sh/uv-pre-commit`'s `uv-export`).
- The symlink at `{{ cookiecutter.project_slug }}/.pre-commit-config.yaml` (replaced with an independent file).
- Static generated `LICENSE` (now rendered by the post-gen hook from the chosen license template, with current year and author auto-filled).

### Fixed
- Templated values in hook scripts and generated `pyproject.toml`/`settings.py`/`test_smoke.py` are now rendered via Jinja's `|tojson` filter. This makes the hook itself robust to weird input (quotes, newlines, control chars) even before validation runs, so quote-containing values can no longer break Python parsing of the hook script before the validator can reject them.
- Tightened `author_email` validation: practical email regex (no quotes, backslashes, or whitespace anywhere). The previous loose regex permitted `b"d@example.com`-style values.
- Extended pre-gen validation to cover `project_name` (flows into `settings.py`, `__init__.py` docstring, smoke tests) and `author_email` (flows into TOML).
- Extended `UNSAFE_CHARS` set to also catch tab and null byte, with friendly per-character labels in the error message.
- Scoped `ruff S603` ignore from global to per-line (`# noqa: S603` on the hook's `subprocess.run` helper) and per-file (`test_*.py`). Future genuinely-risky subprocess calls won't be masked by a blanket ignore.
- Post-gen hook now uses `try/finally` to clean up `.licenses/` staging dir on all paths (was leaked on failure).
- Post-gen hook distinguishes pre-commit auto-fix from real hook failure via a second pass; only emits the "auto-fixed" message when the second pass is clean.
- Doc/code mismatch: `AGENTS.md` and `CONTRIBUTING.md` previously referenced `hooks/licenses/`; now correctly point to the rendered-tree `.licenses/` location.
- Pre-commit hook revisions bumped: `pre-commit-hooks` v5.0.0→v6.0.0, `ruff-pre-commit` v0.7.4→v0.15.12. New ruff hook IDs (`ruff-check` instead of legacy `ruff` alias).
- Generated projects no longer silently inherit maintainer-side pre-commit state via the now-removed symlink.
- `LOG_LEVEL` is now read via `environs.env.str` for consistency with the rest of the settings module (was `os.environ.get`).
- `setup_env.sh` (which was never invoked by the post-gen hook) is gone; `.env.example` ships in its place and is copied to `.env` automatically by the post-gen hook.
- `PROJECT_DIR` resolution updated to `Path(__file__).resolve().parents[2]` to account for the new package depth (`src/<slug>/settings.py` instead of `src/settings.py`).
