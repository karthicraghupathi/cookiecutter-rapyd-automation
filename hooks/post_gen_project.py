"""Cookiecutter post-generation hook.

Runs after the template is rendered, in the generated project's directory:
- Renders LICENSE from the chosen license template.
- Initializes a git repo and bootstraps the uv venv.
- Installs and runs pre-commit (best-effort; non-fatal).

Cross-platform: uses subprocess + pathlib instead of bash.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path.cwd()
AUTHOR_NAME = "{{ cookiecutter.author_name }}"
LICENSE_CHOICE = "{{ cookiecutter.license }}"


def fail(message: str) -> None:
    """Print error message in red and exit non-zero."""
    print(f"\033[31m[post-gen hook] {message}\033[0m", file=sys.stderr)
    sys.exit(1)


def info(message: str) -> None:
    print(f"[post-gen hook] {message}")


def require_command(cmd: str, install_hint: str) -> None:
    if shutil.which(cmd) is None:
        fail(f"`{cmd}` not found on PATH. Install: {install_hint}")


def render_license() -> None:
    """Render LICENSE from the chosen license template.

    Cookiecutter copies the entire `hooks/` directory (including subdirectories)
    to a temp location and runs the hook from there. So
    `Path(__file__).parent / "licenses"` resolves correctly inside that
    temp location.
    """
    licenses_dir = Path(__file__).resolve().parent / "licenses"
    license_file = licenses_dir / f"{LICENSE_CHOICE}.txt"

    if not license_file.exists():
        fail(f"License template not found: {license_file}")

    template = license_file.read_text(encoding="utf-8")
    rendered = template.format(
        author_name=AUTHOR_NAME,
        current_year=datetime.now().year,
    )
    (PROJECT_DIR / "LICENSE").write_text(rendered, encoding="utf-8")
    info(f"Wrote LICENSE ({LICENSE_CHOICE})")


def copy_env_example() -> None:
    """If .env.example exists and .env doesn't, copy it."""
    src = PROJECT_DIR / ".env.example"
    dst = PROJECT_DIR / ".env"
    if src.exists() and not dst.exists():
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        info("Copied .env.example to .env")


def run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess:
    info(f"$ {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=PROJECT_DIR, check=check)


def main() -> None:
    require_command("git", "https://git-scm.com/downloads")
    require_command(
        "uv",
        "https://docs.astral.sh/uv/getting-started/installation/",
    )

    render_license()
    copy_env_example()

    run(["git", "init", "-b", "main"])
    run(["uv", "sync", "--all-groups"])
    run(["git", "add", "."])
    run(["uv", "run", "pre-commit", "install"])

    # Best-effort: run hooks once. Don't fail the whole hook if a hook
    # auto-fixes files (which exits non-zero by design).
    info("Running pre-commit on all files (best-effort)...")
    result = run(
        ["uv", "run", "pre-commit", "run", "--all-files"],
        check=False,
    )
    if result.returncode != 0:
        info(
            "pre-commit auto-fixed some files. "
            "Review and re-stage before committing."
        )

    info(f"Project ready at {PROJECT_DIR}")


if __name__ == "__main__":
    main()
