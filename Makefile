.PHONY: init run_hooks test testdocker clean docs
.ONESHELL :


init:
	sh scripts/init
	sh scripts/install

test:
	sh scripts/test

run_hooks:
	pre-commit run --all-files --show-diff-on-failure

testdocker:
	docker-compose build
	docker-compose run --rm tests sh scripts/test
	docker-compose down

clean:
	sh scripts/clean

docs:
	cd docs && make html

minor:
	bump2version patch
