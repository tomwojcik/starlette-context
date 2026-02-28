.PHONY: init test run-hooks clean docs update-deps build


init:
	sh scripts/init
	sh scripts/install

test:
	uv sync --group dev
	sh scripts/test

run-hooks:
	uv sync --group code-quality
	uv run pre-commit run --all-files --show-diff-on-failure

clean:
	sh scripts/clean

docs:
	uv sync --group docs
	cd docs && make html

update-deps:
	uv lock --upgrade

build:
	uv build
