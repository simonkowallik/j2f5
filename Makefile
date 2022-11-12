.PHONY: clean clean-test clean-pyc clean-build docs help

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
	rm -f coverage.lcov
	rm -fr htmlcov/
	rm -fr .pytest_cache
	find . -name '.mypy_cache' -exec rm -fr {} +

lint:
	pylint f5mkupy/*.py
	pylint tests/*.py

black:
	black f5mkupy/*.py
	black tests/*.py

isort:
	isort f5mkupy/*.py
	isort tests/*.py

code-format: isort black # black has the last word

test:
	PYTHONPATH=./ pytest --cov=j2f5 --cov-report=xml tests/
	coverage report -m
	coverage html
	coverage lcov

tests: test

dependencies-update:
	poetry update

dependencies-lock:
	poetry lock

dependencies: dependencies-update dependencies-lock
