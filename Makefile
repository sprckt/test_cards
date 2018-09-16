.PHONY: clean clean-test clean-pyc clean-build docs help

.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test clean-docs ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

clean-docs: ## remove mkdocs site
	rm -fr site/

lint: ## check style with flake8
	python3.6 -m flake8 --show-source src tests setup.py

test: ## run tests quickly with the default Python
	pytest

smoketest: ## run tests marked with @pytest.mark.smoke
	pytest -m smoke

alactest: ## run tests marked with @pytest.mark.alac
	pytest -m alac

test-all: ## run tests on every Python version with tox
	tox

pytest: test ## alias so "make pytest" works

tox: test-all ## alias so "make tox" works

coverage: ## check code coverage quickly with the default Python
	coverage run --source cards -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs: ## generate HTML documentation
	pip install mkdocs
	mkdocs build

servedocs: docs ## compile the docs watching for changes
	mkdocs serve

VERSION := v$(shell python setup.py --version)

release: clean ## package and upload a release
	python setup.py sdist
	python setup.py bdist_wheel
	twine upload dist/*
	@echo "pushing tags"
	git tag $(VERSION)
	git push --tags

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install
