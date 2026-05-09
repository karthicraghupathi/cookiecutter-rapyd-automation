# Contributing

Thanks for your interest in this template.

## Dev setup

```bash
git clone <fork-url>
cd cookiecutter-rapyd-automation
uv sync                                          # creates .venv from pyproject.toml + uv.lock
uv run pre-commit install                        # registers the git pre-commit hook
```

## Running tests

```bash
uv run pytest
```

Tests bake the template into a temp directory and assert the generated project lints and tests cleanly.

## Adding a license option

1. Add the license name (e.g., `"GPL-3.0"`) to the `license` list in `cookiecutter.json`.
2. Drop a matching template file at `hooks/licenses/GPL-3.0.txt` containing `{author_name}` and `{current_year}` placeholders.
3. Add a test case to `test_license_choice_renders` in `test_cookiecutter.py`.

## Release process

1. Update `CHANGELOG.md` with the new version section.
2. Bump version in the root `pyproject.toml` (`[project].version`).
3. Commit, then tag: `git tag v<version> && git push --tags`.

## Code style

ruff handles lint + format. Pre-commit runs both on every commit. If you can't get pre-commit to pass, run `uv run ruff check --fix .` and `uv run ruff format .` locally first.
