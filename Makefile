lint:
	black ./venv -prune -o
	sh -c "isort --skip-glob=.tox --recursive ./venv -prune -o "
	flake8 ./venv -prune -o --exclude=.tox
	mypy ./venv -prune -o

clean:
	rm -f $(obj) myprog
