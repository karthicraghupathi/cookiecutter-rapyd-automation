# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Setup

```bash
uv sync --all-groups
cp .env.example .env       # edit as needed
uv run pre-commit install  # one-time, registers git hooks
```

## Run

```bash
uv run python -m {{ cookiecutter.project_slug }}
# or
make run
```

## Test

```bash
make test
```

## Lint and format

```bash
make lint    # uv run ruff check .
make format  # uv run ruff format .
```

## Configuration

Environment variables are loaded from `.env` via [`environs`](https://pypi.org/project/environs/). See `.env.example` for the supported keys.
