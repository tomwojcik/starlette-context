.PHONY: init run_hooks test clean docs push

init:
	sh scripts/init.sh

run_hooks:
	pre-commit run --all-files --show-diff-on-failure

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

testbuild:
	$(MAKE) prebuild
	python3 setup.py sdist bdist_wheel

stubs:
	stubgen starlette_context --output starlette_context

build:
	$(MAKE) prebuild
	bump2version patch
	python3 setup.py sdist bdist_wheel

push:
	twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
