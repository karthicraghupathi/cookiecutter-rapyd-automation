# Cookiecutter Rapyd Automation

A [Cookiecutter](https://cookiecutter.readthedocs.io/) template for Python automation projects.

## Quickstart

```bash
uvx cookiecutter gh:karthicraghupathi/cookiecutter-rapyd-automation
```

You'll be prompted for project name, slug, description, Python version, author, email, and license. The post-generation hook then bootstraps the new project: `git init`, `uv sync`, pre-commit install, and a one-shot `pre-commit run --all-files`.

## What you get

A new project pre-configured with:

- **uv** for dependency management (single source of truth: `pyproject.toml`).
- **ruff** for lint + format (replaces black + isort + flake8).
- **pre-commit** wired up with ruff hooks, standard hygiene hooks, and `uv-lock` / `uv-export` so committed `requirements.txt` and `requirements-dev.txt` stay synced with `uv.lock`.
- **environs**-based settings module with logging configured for stdout/stderr split.
- **`src/<slug>/`** package layout — runnable as `uv run python -m <slug>`.
- A `tests/` directory with one passing smoke test.
- A `Makefile` with `lint`, `format`, `test`, `run` targets.
- An `AGENTS.md` so AI coding agents understand the conventions.

## Customizing the generated project

After generation, you can tune anything: ruff rules in `pyproject.toml`, pre-commit hooks in `.pre-commit-config.yaml`, dependencies via `uv add` / `uv add --dev`. The template is a starting point, not a contract.

## Contributing

See `CONTRIBUTING.md`.

## License

MIT — see `LICENSE`.
