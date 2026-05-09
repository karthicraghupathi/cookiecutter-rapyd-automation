# Changelog

All notable changes to this project will be documented in this file. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
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
- Generated projects no longer silently inherit maintainer-side pre-commit state via the now-removed symlink.
- `LOG_LEVEL` is now read via `environs.env.str` for consistency with the rest of the settings module (was `os.environ.get`).
- `setup_env.sh` (which was never invoked by the post-gen hook) is gone; `.env.example` ships in its place and is copied to `.env` automatically by the post-gen hook.
- `PROJECT_DIR` resolution updated to `Path(__file__).resolve().parents[2]` to account for the new package depth (`src/<slug>/settings.py` instead of `src/settings.py`).
