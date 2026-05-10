# AGENTS.md

This file orients AI coding agents and human contributors who are new to this repo.

## What this repo is

A Cookiecutter template that scaffolds a Python automation project. Running `uvx cookiecutter <this-repo>` produces a fresh project pre-configured with uv, ruff, pre-commit, and a logging-aware settings module.

## Two-tree layout

- **Root** — the template repo's own dev environment (uv-managed). You run tests from here.
- **`{{ cookiecutter.project_slug }}/`** — the templated tree. Cookiecutter substitutes Jinja tokens here at bake time. The literal directory name is the variable.

The two `.pre-commit-config.yaml` files (root + inside the template dir) are intentionally independent. Don't symlink them.

## Cookiecutter mechanics

- Prompts live in `cookiecutter.json` (lists become choice prompts; first item is the default).
- The post-generation hook is `hooks/post_gen_project.py` (cross-platform Python).
- License templates live in the rendered tree at `{{ cookiecutter.project_slug }}/.licenses/<choice>.txt` and are marked `_copy_without_render` in `cookiecutter.json` so Jinja skips them. The post-gen hook reads the chosen template, substitutes `{author_name}` and `{current_year}`, writes `LICENSE`, then removes the `.licenses/` staging directory.
- Files matched by `_copy_without_render` skip Jinja substitution.

## Verification commands

After any change, run these from the repo root:

```bash
uv sync                                          # ensure deps current
uv run pytest                                    # run template-level tests (bakes the template)
uv run ruff check .                              # lint
uv run pre-commit run --all-files                # full hook pass
```

If a test fails after editing template files, the bake itself probably broke — read the test output for the temp directory path and inspect the rendered tree.

## Adding a new cookiecutter prompt

1. Add the key to `cookiecutter.json` (use a list for choices).
2. Reference it in template files via `{{ cookiecutter.<key> }}`.
3. If the prompt should affect file rendering (e.g., choosing a license), update `hooks/post_gen_project.py`.
4. Add a test in `test_cookiecutter.py` that bakes with each value of the prompt and asserts the rendered output.
