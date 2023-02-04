.PHONY: init test run-hooks clean docs update-deps build
.ONESHELL :


init:
	sh scripts/init
	sh scripts/install

test:
	poetry install --with dev
	sh scripts/test

run-hooks:
	poetry install --with code-quality
	pre-commit run --all-files --show-diff-on-failure

clean:
	sh scripts/clean

docs:
	poetry install --with docs
	cd docs && make html

update-deps:
	poetry update

build:
	poetry version v$(git describe --tags --abbrev=0)
	poetry build
