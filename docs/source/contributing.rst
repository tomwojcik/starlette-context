============
Contributing
============

I'm very happy with all the tickets you open. Feel free to open PRs if you feel like it.
If you've found a bug but don't want to get involved, that's more than ok and I'd appreciate such ticket as well.

If you have opened a PR it can't be merged until CI passed. Stuff that is checked:
 * codecov has to be kept at 100%
 * pre commit hooks consist of flake8 and mypy, so consider installing hooks before commiting. Otherwise CI might fail

Sometimes one pre-commit hook will affect another so you will run them a few times.

You can run tests with docker of with venv.

***********
With docker
***********

With docker run tests with ``make testdocker``.
If you want to plug docker env in your IDE run service ``tests`` from ``docker-compose.yml``.

***********
Local setup
***********

Running ``make init`` will result with creating local venv with dependencies. Then you can ``make test`` or plug venv into IDE.
