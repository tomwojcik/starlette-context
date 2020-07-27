============
Contributing
============

I'm very happy with all the tickets you open. Feel free to open PRs if you feel like it.

It's a rather young and small project so I haven't defined any specific guidelines yet.

If you have opened a PR I won't merge it until
 * it will have 100% coverage
 * will be black/mypy positive

I'm willing to do that myself after your changes but I don't know if you want me to work on your branch. Just letting you know I will if those conditions are not met.

If you have found a bug or just want to open a feature request I'm more than happy to implement it myself as well.

If you plan to contribute and write some tests, have in mind that PyCharm debugger for pytest won't work if there's `--cov` in ``pytest.ini`` so just remove this line when you debug.
