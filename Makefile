.PHONY: init run_hooks citest test clean docs push
.ONESHELL :


init:
	sh scripts/init.sh

run_hooks:
	pre-commit run --all-files --show-diff-on-failure

citest:
	if [ ! -d "venv" ]; then $(MAKE) init; fi
	sh scripts/test.sh
	black starlette_context --check
	flake8 starlette_context

test:
	sh scripts/test.sh
	$(MAKE) run_hooks

clean:
	sh scripts/clean.sh

docs:
	cd docs && make html

prebuild:
	sh scripts/clean.sh
	$(MAKE) run_hooks
	$(MAKE) docs

build:
	$(MAKE) prebuild
	bump2version patch
	python3 setup.py sdist bdist_wheel

push:
	twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
