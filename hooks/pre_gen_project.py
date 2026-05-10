"""Cookiecutter pre-generation hook.

Runs after prompts are answered, before the template tree is rendered.
Validates user-supplied values to fail fast with a clear message instead
of producing a broken project.

Validations:
- `project_slug` must be a valid Python identifier (so the package is
  importable) and not a reserved keyword.
- `author_name` and `project_description` must not contain characters
  that would break the generated `pyproject.toml` (quotes, backslashes,
  newlines).
- `author_email` must look like a basic email.
"""

from __future__ import annotations

import keyword
import re
import sys

PROJECT_SLUG = "{{ cookiecutter.project_slug }}"
AUTHOR_NAME = "{{ cookiecutter.author_name }}"
AUTHOR_EMAIL = "{{ cookiecutter.author_email }}"
PROJECT_DESCRIPTION = "{{ cookiecutter.project_description }}"

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
TOML_UNSAFE = ('"', "\\", "\n", "\r")


def fail(message: str) -> None:
    print(f"\033[31m[pre-gen hook] {message}\033[0m", file=sys.stderr)
    sys.exit(1)


def validate_slug() -> None:
    if not PROJECT_SLUG.isidentifier():
        fail(
            f"project_slug={PROJECT_SLUG!r} is not a valid Python identifier. "
            "Use letters, digits, and underscores; must start with a letter or "
            "underscore. Try setting project_name to a value that produces a "
            "clean slug, or override project_slug at the prompt."
        )
    if keyword.iskeyword(PROJECT_SLUG):
        fail(
            f"project_slug={PROJECT_SLUG!r} is a Python reserved keyword. "
            "Pick a different project name."
        )


def validate_toml_safe(field: str, value: str) -> None:
    for ch in TOML_UNSAFE:
        if ch in value:
            label = repr(ch) if ch != "\n" else "newline"
            fail(
                f"{field}={value!r} contains {label}, which would break the "
                "generated pyproject.toml. Remove the offending character."
            )


def validate_email() -> None:
    if not EMAIL_RE.match(AUTHOR_EMAIL):
        fail(
            f"author_email={AUTHOR_EMAIL!r} doesn't look like an email "
            "address (expected user@host.tld)."
        )


def main() -> None:
    validate_slug()
    validate_toml_safe("author_name", AUTHOR_NAME)
    validate_toml_safe("project_description", PROJECT_DESCRIPTION)
    validate_email()


if __name__ == "__main__":
    main()
