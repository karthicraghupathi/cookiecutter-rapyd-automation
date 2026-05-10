"""Tests for the cookiecutter template.

Tests bake the template into a temp directory and assert:
- The bake succeeds (post-gen hook runs without crashing).
- The expected files are present.
- The generated project passes ruff and pytest (uses uv).
- License + python_version choices render correctly.
- The hook fails gracefully when uv is missing.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

EXPECTED_FILES = [
    ".gitignore",
    ".pre-commit-config.yaml",
    ".env.example",
    "AGENTS.md",
    "LICENSE",
    "Makefile",
    "pyproject.toml",
    "README.md",
    "requirements.txt",
    "requirements-dev.txt",
    "uv.lock",
    "src/python_boilerplate/__init__.py",
    "src/python_boilerplate/__main__.py",
    "src/python_boilerplate/main.py",
    "src/python_boilerplate/settings.py",
    "tests/__init__.py",
    "tests/test_smoke.py",
]


def _run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def test_default_bake_succeeds(cookies):
    """Bake with default inputs and assert no errors."""
    result = cookies.bake()

    assert result.exit_code == 0, result.exception
    assert result.exception is None
    assert result.project_path.is_dir()


def test_default_bake_creates_expected_files(cookies):
    """Assert every expected file exists in the rendered tree."""
    result = cookies.bake()

    for relpath in EXPECTED_FILES:
        assert (result.project_path / relpath).exists(), f"missing: {relpath}"


def test_obsolete_files_not_present(cookies):
    """Assert the M1-era files are gone from the new template."""
    result = cookies.bake()

    obsolete = [
        "Pipfile",
        ".flake8",
        "setup_env.sh",
        "src/main.py",
        "src/settings.py",
        ".licenses",
    ]
    for relpath in obsolete:
        assert not (result.project_path / relpath).exists(), f"unexpected: {relpath}"


def test_custom_slug_renders(cookies):
    """Bake with a custom project_name; assert the slug is auto-derived."""
    result = cookies.bake(extra_context={"project_name": "My Cool Bot"})

    assert result.exit_code == 0
    assert result.project_path.name == "my_cool_bot"


def test_generated_project_passes_ruff(cookies):
    """Run `uv run ruff check .` in the baked project; expect exit 0."""
    result = cookies.bake()
    proc = _run(["uv", "run", "ruff", "check", "."], result.project_path)

    assert proc.returncode == 0, f"ruff failed:\n{proc.stdout}\n{proc.stderr}"


def test_generated_project_passes_pytest(cookies):
    """Run `uv run pytest` in the baked project; expect exit 0."""
    result = cookies.bake()
    proc = _run(["uv", "run", "pytest"], result.project_path)

    assert proc.returncode == 0, f"pytest failed:\n{proc.stdout}\n{proc.stderr}"


@pytest.mark.parametrize("python_version", ["3.10", "3.11", "3.12", "3.13"])
def test_python_version_choices(cookies, python_version):
    """Bake with each Python version; assert pyproject.toml reflects it."""
    result = cookies.bake(extra_context={"python_version": python_version})

    assert result.exit_code == 0
    pyproject = (result.project_path / "pyproject.toml").read_text()
    assert f'requires-python = ">={python_version}"' in pyproject


@pytest.mark.parametrize(
    "license_choice", ["MIT", "Apache-2.0", "BSD-3-Clause", "Proprietary"]
)
def test_license_choice_renders(cookies, license_choice):
    """Bake with each license; assert LICENSE content matches the choice."""
    result = cookies.bake(
        extra_context={"license": license_choice, "author_name": "Test User"}
    )

    assert result.exit_code == 0
    license_text = (result.project_path / "LICENSE").read_text()
    assert "Test User" in license_text

    if license_choice == "MIT":
        assert "MIT License" in license_text
    elif license_choice == "Apache-2.0":
        assert "Apache License" in license_text
    elif license_choice == "BSD-3-Clause":
        assert "BSD 3-Clause License" in license_text
    elif license_choice == "Proprietary":
        assert "proprietary" in license_text.lower()


def test_post_gen_hook_requires_uv(tmp_path):
    """Run the hook script directly with PATH stripped of uv.

    Asserts the hook exits non-zero with a friendly message about uv.
    """
    import sys

    repo_root = Path(__file__).parent
    hook_path = repo_root / "hooks" / "post_gen_project.py"

    # The hook script contains Jinja tokens like `{{ cookiecutter.author_name }}`
    # that aren't substituted when running directly. Replace with literals first.
    rendered = hook_path.read_text()
    rendered = rendered.replace("{{ cookiecutter.author_name }}", "Test")
    rendered = rendered.replace("{{ cookiecutter.license }}", "MIT")
    test_hook = tmp_path / "post_gen_project.py"
    test_hook.write_text(rendered)

    # Use the current Python interpreter directly (absolute path), but strip
    # PATH so `shutil.which("uv")` returns None inside the hook.
    proc = subprocess.run(
        [sys.executable, str(test_hook)],
        cwd=tmp_path,
        env={"PATH": "/usr/bin:/bin", "HOME": str(tmp_path)},
        capture_output=True,
        text=True,
    )

    assert proc.returncode != 0
    assert "uv" in proc.stderr.lower()


# --- Validation tests (pre-gen hook) -----------------------------------------


def test_invalid_slug_rejected(cookies):
    """A project_name that produces a non-identifier slug fails fast."""
    result = cookies.bake(extra_context={"project_name": "1bad start"})

    # Slug becomes "1bad_start" — invalid Python identifier (leading digit).
    assert result.exit_code != 0


def test_python_keyword_slug_rejected(cookies):
    """A slug equal to a Python reserved keyword is rejected."""
    result = cookies.bake(extra_context={"project_slug": "class"})

    assert result.exit_code != 0


def test_author_with_double_quote_rejected(cookies):
    """Quotes in author_name would break the generated pyproject.toml."""
    result = cookies.bake(extra_context={"author_name": 'Bad"Name'})

    assert result.exit_code != 0


def test_author_with_newline_rejected(cookies):
    result = cookies.bake(extra_context={"author_name": "Line\nTwo"})

    assert result.exit_code != 0


def test_invalid_email_rejected(cookies):
    result = cookies.bake(extra_context={"author_email": "not-an-email"})

    assert result.exit_code != 0


def test_non_ascii_author_renders(cookies):
    """Non-ASCII author names should work — only TOML-unsafe chars are blocked."""
    result = cookies.bake(extra_context={"author_name": "Café Owner"})

    assert result.exit_code == 0
    license_text = (result.project_path / "LICENSE").read_text(encoding="utf-8")
    assert "Café Owner" in license_text


# --- Generated requirements files --------------------------------------------


def test_requirements_files_have_content(cookies):
    """Both requirements files exist and are non-empty after the bake.

    The post-gen hook runs `uv-export` via pre-commit, which writes the files.
    `requirements-dev.txt` (prod + dev) is a strict superset of `requirements.txt`
    (prod only).
    """
    result = cookies.bake()

    req = (result.project_path / "requirements.txt").read_text()
    req_dev = (result.project_path / "requirements-dev.txt").read_text()

    # Both should at minimum mention environs (the only runtime dep).
    assert "environs" in req
    assert "environs" in req_dev
    # Dev superset: pytest is a dev dep, must be in requirements-dev.txt only.
    assert "pytest" in req_dev
    assert "pytest" not in req


# --- License resolution ------------------------------------------------------


def test_unknown_license_fails(cookies):
    """A license value not in the choice list (and missing template) fails."""
    result = cookies.bake(extra_context={"license": "GPL-3.0"})

    # No GPL-3.0.txt exists in .licenses/, so render_license() should fail
    # with a friendly message.
    assert result.exit_code != 0


def test_licenses_staging_dir_removed(cookies):
    """The .licenses/ staging directory is cleaned up by the post-gen hook."""
    result = cookies.bake()

    assert not (result.project_path / ".licenses").exists()
