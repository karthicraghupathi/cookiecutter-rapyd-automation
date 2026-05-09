# Modernization Design — cookiecutter-rapyd-automation

**Date:** 2026-05-09
**Status:** Approved (scope locked with maintainer)
**Author:** Karthic Raghupathi (with AI collaboration)

## Goal

Modernize this Cookiecutter template to give new automation projects a fast, low-friction starter — and make the template repo itself easier for both humans and LLMs to maintain.

Two perspectives drive the work:

1. **End user** (someone who runs `cookiecutter <repo>`): gets a generated project that works on first try, ships sensible defaults, and uses current tooling (uv, ruff).
2. **Maintainer / contributor**: can change the template confidently, knows how to test changes, and has documentation an LLM coding agent can navigate.

## Scope

In scope:

- Replace pipenv with uv (single source of truth: `pyproject.toml`).
- Replace black + isort + flake8 with ruff (lint + format).
- Fix two bugs in the current template (see "Bugs Fixed" below).
- Port the post-generation hook from bash to Python (cross-platform).
- Add proper test coverage for the template itself.
- Add `AGENTS.md` to both the template repo and generated projects.
- Add cookiecutter prompts for `author_name`, `author_email`, `license`.
- Add a focused `.gitignore`, a `Makefile`, and a `tests/` directory in the generated project.
- Convert generated `src/` to a proper package layout (`src/<slug>/`).

Out of scope:

- CI workflows (template repo or generated project) — explicitly excluded by maintainer.
- Docker / devcontainers / mypy / pyright.
- Renaming the "Rapyd" reference in the repo.
- Migrating already-generated downstream projects.

## Bugs Fixed

| # | Bug | Fix |
|---|-----|-----|
| 1 | Generated project's post-gen hook calls `pre-commit install` and `pre-commit run --all-files`, but the template ships no `.pre-commit-config.yaml`. | Template ships `.pre-commit-config.yaml` (with ruff hooks). |
| 2 | `setup_env.sh` is dead — never invoked, leaves users with no `.env`, no `.env.example`. | Replace with `.env.example` documenting `LOG_LEVEL`; post-gen hook copies it to `.env` if missing. |
| 3 | `migrations/` exclusion in pre-commit (Django carryover). | Removed. |
| 4 | Bash-only post-gen hook excludes Windows users. | Ported to Python (cross-platform `subprocess`). |
| 5 | `src/` is not a package; `import settings` is sys.path-fragile. | Switch to `src/<slug>/` package; absolute imports. |
| 6 | Free-text `python_version` in `cookiecutter.json` (typo-prone). | Cookiecutter choice list. |
| 7 | `cookiecutter.json` lacks author/license metadata; generated `LICENSE` keeps template author forever. | Add prompts; generate fresh `LICENSE` per project with current year. |
| 8 | Generated `pyproject.toml` lacks a `[project]` table (incomplete for modern Python packaging and uv). | Full `[project]` table populated from cookiecutter prompts. |
| 9 | `readme.md` lowercase. | Standardize on `README.md`. |
| 10 | `settings.py` mixes `os.environ.get` and `environs.env`. | Use `env.str("LOG_LEVEL", "INFO")` consistently. |

## Two Milestones

These are *logical* phases. They can ship as one or two PRs at the maintainer's discretion. Without CI, the value of phasing is mainly so the test harness exists before the implementation churn.

### M1 — Foundation

No end-user behavior change. Adds maintainer-facing infrastructure.

- `AGENTS.md` at repo root.
- `CONTRIBUTING.md`.
- `CHANGELOG.md` (Keep a Changelog format).
- Expanded `test_cookiecutter.py` against the **current** template (asserts files in the *pre-M2* tree: `Pipfile`, `setup_env.sh`, `src/main.py`, `src/settings.py`, etc.):
  - Existing default-bake test (kept).
  - Assert each currently-expected file exists in the generated project.
  - This test will be rewritten in M2 to match the new tree.
- `README.md` (uppercase) at repo root, rewritten for clarity.

### M2 — Modernization

End-user-visible changes.

- Replace pipenv → uv.
- Replace black/isort/flake8 → ruff.
- Port post-gen hook from bash to Python.
- Generated project: ship `.pre-commit-config.yaml`, `.env.example`, `Makefile`, `AGENTS.md`, `tests/` directory.
- Generated project: convert to `src/<slug>/` package layout.
- Cookiecutter prompts: add `author_name`, `author_email`, `license`; convert `python_version` to a choice list.
- Trim `.gitignore` to focused Python content.
- Update template-level tests to assert generated project passes `ruff check` and `pytest`.

## Cookiecutter Inputs (`cookiecutter.json`)

```json
{
    "python_version": ["3.12", "3.10", "3.11", "3.13"],
    "project_name": "Python Boilerplate",
    "project_slug": "{{ cookiecutter.project_name.lower().replace(' ', '_').replace('-', '_') }}",
    "project_description": "A Python automation project.",
    "author_name": "Your Name",
    "author_email": "you@example.com",
    "license": ["MIT", "Apache-2.0", "BSD-3-Clause", "Proprietary"]
}
```

Cookiecutter renders the first list item as the default. Default Python: **3.12**. Default license: **MIT**.

`current_year` is derived inside the post-gen hook (`datetime.now().year`), not a prompt.

## Generated Project File Tree (after M2)

```
{{ project_slug }}/
├── .gitignore                           # focused ~30-line Python+macOS+vscode
├── .pre-commit-config.yaml              # ruff + ruff-format + standard hooks
├── .env.example                         # documents LOG_LEVEL
├── AGENTS.md                            # conventions doc for AI tools
├── LICENSE                              # rendered from chosen license
├── Makefile                             # lint / format / test / run targets
├── pyproject.toml                       # [project], [tool.ruff], [tool.pytest]
├── README.md
├── src/
│   └── {{ project_slug }}/
│       ├── __init__.py
│       ├── __main__.py                  # `uv run python -m <slug>` entry
│       ├── main.py
│       └── settings.py
└── tests/
    ├── __init__.py
    └── test_smoke.py
```

Files removed compared to current template: `Pipfile`, `setup_env.sh`, root `.flake8`, the toptal-generated `.gitignore`.

## Generated `pyproject.toml`

```toml
[project]
name = "{{ cookiecutter.project_slug }}"
version = "0.1.0"
description = "{{ cookiecutter.project_description }}"
requires-python = ">={{ cookiecutter.python_version }}"
authors = [
    {name = "{{ cookiecutter.author_name }}", email = "{{ cookiecutter.author_email }}"}
]
dependencies = ["environs"]

[dependency-groups]
dev = ["pre-commit", "pytest", "ruff"]

[tool.ruff]
line-length = 88
target-version = "py{{ cookiecutter.python_version.replace('.', '') }}"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "B", "UP"]
ignore = ["E501"]

[tool.ruff.format]
# Black-compatible defaults

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```

## Generated `.pre-commit-config.yaml`

```yaml
default_language_version:
  python: python3
exclude: |
  (?x)(
    .idea/|
    .venv/|
    .git/
  )
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: check-added-large-files
      - id: check-json
      - id: check-merge-conflict
      - id: check-symlinks
      - id: check-yaml
      - id: end-of-file-fixer
      - id: trailing-whitespace
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.7.4
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

## Post-Gen Hook (`hooks/post_gen_project.py`)

Replaces `hooks/post_gen_project.sh`. Behavior:

1. Detect missing `uv` or `git`; print install instructions and exit cleanly with non-zero code.
2. Render `LICENSE`: pick the chosen license template, substitute `{author_name}` and `{current_year}`, write to `LICENSE`. (Cookiecutter alone can't compute current year, hence the hook.)
3. Copy `.env.example` to `.env` if `.env` does not already exist.
4. `git init -b main` (force `main` for predictability).
5. `uv sync --all-groups` (creates `.venv` and `uv.lock`).
6. `git add .`
7. `uv run pre-commit install`.
8. `uv run pre-commit run --all-files` — best-effort. If it fails, print a friendly message ("pre-commit auto-fixed some files; review and re-stage") and exit 0; do not abort the project generation.

License templates live at `hooks/licenses/<choice>.txt`, where `<choice>` matches the value in `cookiecutter.json` exactly (`MIT.txt`, `Apache-2.0.txt`, `BSD-3-Clause.txt`, `Proprietary.txt`).

## Settings & Main Modules

`src/<slug>/settings.py`:

- Switch `os.environ.get("LOG_LEVEL", "INFO")` to `env.str("LOG_LEVEL", "INFO")` for consistency with `environs`.
- `PROJECT_DIR = Path(__file__).resolve().parents[2]` (now two levels up because of the `src/<slug>/` layout).
- Logger naming: `logging.getLogger(__name__)` (changed from current `f"{PROJECT_SLUG}.{__name__}"` — with the new package layout, `__name__` already begins with the slug, so the explicit prefix would duplicate).
- Excepthook: kept as-is.

`src/<slug>/main.py`:

```python
from . import settings
from .settings import logger


def main() -> None:
    logger.info("Running %s", settings.PROJECT_NAME)


if __name__ == "__main__":
    main()
```

`src/<slug>/__main__.py`:

```python
from .main import main

if __name__ == "__main__":
    main()
```

So `uv run python -m <slug>` works.

## Tests

### Template-level (`test_cookiecutter.py`)

After M2, the suite covers:

1. `test_default_bake_succeeds` — bake with defaults, assert exit 0 + no exception (kept).
2. `test_default_bake_creates_expected_files` — assert each file in the generated tree exists.
3. `test_generated_project_passes_ruff` — run `uv run ruff check .` in the baked project; assert exit 0.
4. `test_generated_project_passes_pytest` — run `uv run pytest` in the baked project; assert exit 0.
5. `test_python_version_choices` — bake with each Python version; assert `pyproject.toml` `requires-python` matches.
6. `test_license_choice_renders` — bake with each license choice; assert `LICENSE` content matches.
7. `test_post_gen_hook_handles_missing_uv` — mock `shutil.which("uv")` to return `None`; assert hook exits non-zero with a friendly message.

Tests run via `uv run pytest` at the repo root.

### Generated-project-level (`tests/test_smoke.py`)

```python
from {{ cookiecutter.project_slug }} import settings


def test_settings_loads():
    assert settings.PROJECT_NAME == "{{ cookiecutter.project_name }}"
    assert settings.PROJECT_SLUG == "{{ cookiecutter.project_slug }}"


def test_logger_configured():
    assert settings.logger is not None
```

Just enough to prove the package layout, settings module, and pytest config all work end-to-end.

## Documentation

### Template repo

- **`README.md`** (uppercase): What this is → Quickstart (`uvx cookiecutter gh:karthicraghupathi/cookiecutter-rapyd-automation`) → What you get (file tree) → Customizing → Contributing pointer.
- **`AGENTS.md`**: How the template works — Jinja substitution in dir name, hook execution order, where to add a new prompt, how to test changes locally (`uv run pytest`). One screenful, written for both humans and LLM coding agents.
- **`CONTRIBUTING.md`**: dev setup (`uv sync`, `pre-commit install`), how to run tests, how to add a new license template, release process (tag → bump CHANGELOG → push tag).
- **`CHANGELOG.md`**: Keep a Changelog format. Initial entries: M1 + M2.

### Generated project

- **`README.md`**: install (`uv sync`) → run (`uv run python -m <slug>`) → lint (`uv run ruff check .`) → format (`uv run ruff format .`) → test (`uv run pytest`) → env vars (`cp .env.example .env`).
- **`AGENTS.md`**: conventions — uv only (no pip), ruff for lint+format, `src/<slug>/` package layout, settings module pattern, logger naming convention. Tells AI agents the canonical commands.

## Generated `Makefile`

```make
.PHONY: install lint format test run

install:
	uv sync --all-groups

lint:
	uv run ruff check .

format:
	uv run ruff format .

test:
	uv run pytest

run:
	uv run python -m {{ cookiecutter.project_slug }}
```

## Generated `.env.example`

```
LOG_LEVEL=INFO
```

End users `cp .env.example .env` and edit. The post-gen hook does this copy on first generation; subsequent edits are the user's responsibility.

## Migration Notes for Existing Users

This is a template repo, so "existing users" means people who previously generated projects from older versions. There is no migration path — already-generated projects keep their pipenv/black/etc setup. The maintainer may consider tagging the last pre-modernization commit (e.g., `v0.x` or `pre-uv`) so users who want the old behavior can still pin to it.

The new template is a clean break, not a migration tool.

## Open Decisions Resolved

- **Post-gen hook language:** Python (cross-platform).
- **`src/` layout:** `src/<slug>/` as a package.
- **AI docs:** `AGENTS.md` in both repos.
- **Python versions in choice list:** 3.10, 3.11, 3.12, 3.13. Default 3.12.
- **CI:** none.
- **`git init` default branch:** force `main`.
- **`LOG_LEVEL` env loading:** route through `environs` for consistency.

## Risks

- **uv pre-commit hook freshness:** `astral-sh/ruff-pre-commit` revs frequently. Pinning to a fixed `rev` means generated projects ship with whatever was current at template-publish time. Acceptable; users can `pre-commit autoupdate`.
- **Hook portability:** the new Python hook still depends on `uv` and `git` being installed. Hook detects missing tools and explains; hard requirement remains.
- **No CI safety net:** regressions in the template can ship undetected. Mitigation: the expanded local test suite. Maintainer should run `uv run pytest` before tagging a release.
