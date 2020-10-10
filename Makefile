DOCKER_IMAGES := $(docker images |grep 'starlette_context')

test:
	docker-compose -f docker-compose.yml run --rm tests sh scripts/test.sh

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

lint:
	pre-commit run --all-files

bash:
	docker-compose -f docker-compose.yml run --rm tests sh

doc:
	docker-compose -f docker-compose.yml run --rm tests sh -c "cd docs && make html"

push:
	sh scripts/clean.sh
	lint
	bump2version patch
	python3 setup.py sdist bdist_wheel
	twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

run-hooks:
	pre-commit run --all-files
