DOCKER_IMAGES := $(docker images |grep 'starlette_context')

run_hooks:
	pre-commit run --all-files

test:
	docker-compose -f docker-compose.yml run --rm tests sh scripts/test.sh
	$(MAKE) run_hooks

rebuild:
	docker-compose -f docker-compose.yml up --build

clean:
	sh scripts/clean.sh

purge:
	clean
	docker-compose rm -sfv
	clean_docker

clean_docker:
	@if [ -n "$(DOCKER_IMAGES)" ]; then echo "Removing docker"; else echo "Nothing found"; fi;

bash:
	docker-compose -f docker-compose.yml run --rm tests sh

doc:
	docker-compose -f docker-compose.yml run --rm tests sh -c "cd docs && make html"

push:
	sh scripts/clean.sh
	$(MAKE) run_hooks
	bump2version patch
	python3 setup.py sdist bdist_wheel
	twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
