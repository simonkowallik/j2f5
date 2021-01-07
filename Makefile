.PHONY: clean clean-test clean-pyc clean-build docs

define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
        from urllib import pathname2url
except:
        from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . \( -path ./env -o -path ./venv -o -path ./.env -o -path ./.venv \) -prune -o -name '*.egg-info' -exec rm -fr {} +
	find . \( -path ./env -o -path ./venv -o -path ./.env -o -path ./.venv \) -prune -o -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -f .coverage
	rm -f coverage.xml
	rm -fr htmlcov/
	rm -fr .pytest_cache
	find . -name '.mypy_cache' -exec rm -fr {} +

black:
	black j2f5.py
	black tests/*.py

test:
	pytest tests/

tests: test

coverage:
	pytest --cov=j2f5 --cov-report=xml tests/
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

## generate Sphinx HTML documentation, including API docs
docs:
	rm -f docs/as3ninja.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ as3ninja
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

dependencies-update:
	poetry update

dependencies-lock:
	poetry lock

dependencies: dependencies-update dependencies-lock
