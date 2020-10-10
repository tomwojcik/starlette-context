============
Contributing
============

I'm very happy with all the tickets you open. Feel free to open PRs if you feel like it.
If you've found a bug but don't want to get involved, that's more than ok and I'd appreciate such ticket as well.

If you have opened a PR it can't be merged until CI passed. Stuff that is checked:
 * codecov has to be kept at 100%
 * pre commit hooks consist of flake8 and mypy, so consider installing hooks before commiting. Otherwise CI might fail

You can ``make test`` for yourself. Everything is dockerized.

Have in mind that PyCharm debugger for pytest won't work if there's `--cov` in ``pytest.ini`` so just remove this line when you debug.
