.PHONY: init run_hooks test clean docs
.ONESHELL :


init:
	sh scripts/init

run_hooks:
	pre-commit run --all-files --show-diff-on-failure

test:
	sh scripts/test

clean:
	sh scripts/clean

docs:
	cd docs && make html
