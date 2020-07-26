DOCKER_IMAGES := $(docker images |grep 'starlette_context')

test:
	docker-compose -f docker-compose.yml run --rm app sh scripts/test.sh

rebuild:
	docker-compose -f docker-compose.yml up --build

clean_docker:
	@if [ -n "$(DOCKER_IMAGES)" ]; then echo "Removing docker"; else echo "Nothing found"; fi;

purge:
	docker-compose -f docker-compose.yml down -v --remove-orphans
	sh scripts/clean.sh
	docker-compose rm -sfv
	clean_docker

lint:
	pre-commit run --all-files

bash:
	docker-compose -f docker-compose.yml run --rm app sh

doc:
	docker-compose -f docker-compose.yml run --rm app sh -c "cd docs && make html"

make increment-patch:
	docker-compose -f docker-compose.yml run --rm app sh -c "bump2version part patch"

push:
	docker-compose -f docker-compose.yml run --rm app sh -c "bump2version part starlette_context"
