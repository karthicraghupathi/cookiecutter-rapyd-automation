"""Tests for the cookiecutter template.

Each test bakes the template into a temp directory via pytest-cookies and
asserts the generated project has the expected shape.
"""


def test_default_bake_succeeds(cookies):
    """Bake with default inputs and assert no errors."""
    result = cookies.bake()

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.is_dir()


def test_default_bake_creates_expected_files(cookies):
    """Assert the current template tree's files all show up in the bake."""
    result = cookies.bake()

    expected = [
        "Pipfile",
        "pyproject.toml",
        "readme.md",
        "setup_env.sh",
        ".flake8",
        ".gitignore",
        "LICENSE",
        # .pre-commit-config.yaml temporarily missing; reinstated as real file in M2
        "src/main.py",
        "src/settings.py",
    ]
    for relpath in expected:
        assert (result.project_path / relpath).exists(), f"missing: {relpath}"


def test_custom_slug_renders(cookies):
    """Bake with a custom project_name; assert the slug is auto-derived."""
    result = cookies.bake(extra_context={"project_name": "My Cool Bot"})

    assert result.exit_code == 0
    assert result.project_path.name == "my_cool_bot"
