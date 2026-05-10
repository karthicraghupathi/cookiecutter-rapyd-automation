"""Smoke tests for {{ cookiecutter.project_name }}.

Asserts the package imports and the settings module is configured correctly.
"""

from {{ cookiecutter.project_slug }} import settings


def test_project_metadata():
    assert settings.PROJECT_NAME == {{ cookiecutter.project_name | tojson }}
    assert settings.PROJECT_SLUG == {{ cookiecutter.project_slug | tojson }}


def test_logger_configured():
    assert settings.logger is not None
    assert settings.logger.name.startswith({{ cookiecutter.project_slug | tojson }})
