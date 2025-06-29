#!/usr/bin/env bash

git init
git add .
pipenv --rm
pipenv --python "{{ cookiecutter.python_version }}"
echo -n "Interpreter Location : "
pipenv --py
echo -n "Interpreter Version: "
pipenv run python --version
pipenv install --dev
git add .
pipenv run pre-commit install
pipenv run pre-commit run --all-files
