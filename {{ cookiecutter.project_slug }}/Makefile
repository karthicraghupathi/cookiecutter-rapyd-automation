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
