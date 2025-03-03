.PHONY: init test run-hooks clean docs update-deps build
.ONESHELL :


init:
	sh scripts/init
	sh scripts/install

test:
	poetry install --only dev
	sh scripts/test

run-hooks:
	poetry install --only code-quality
	poetry run pre-commit run --all-files --show-diff-on-failure

clean:
	sh scripts/clean

docs:
	poetry install --only docs
	cd docs && make html

update-deps:
	poetry update

# https://python-poetry.org/docs/cli/#version
build:
	poetry build
