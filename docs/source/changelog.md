# Change Log

This document records all notable changes to starlette-context.
This project adheres to [Semantic Versioning](http://semver.org/).

## Latest Release

## [0.3.6] - 2023-02-16

* Fix for being unable to catch some exceptions with a try/except due to base exc inheriting from the `BaseException` (Thanks @soundstripe) [#90](https://github.com/tomwojcik/starlette-context/issues/90)
* Minimal Python version required is now 3.8

## [0.3.5] - 2022-11-26

* Fix for accessing the context in error handlers (Thanks @hhamana) [#74](https://github.com/tomwojcik/starlette-context/issues/74)

## [0.3.4] - 2022-06-22

* Add `request_cycle_context`. It's a context manager that allows for easier testing and cleaner code (Thanks @hhamana) [#46](https://github.com/tomwojcik/starlette-context/issues/46)
* Fix for accessing context during logging, outside of the request-response cycle. Technically it should raise an exception, but it makes sense to include the context by default (in logs) and if it's not available, some logs are better than no logs. Now it will show context data if context is available, with a fallback to an empty dict (instead of raising an exc) [#65](https://github.com/tomwojcik/starlette-context/issues/65)
* Add `ContextMiddleware` deprecation warning
* `**context` context unpacking seems to be working now

## [0.3.3] - 2021-06-28

* Add support for custom error responses if error occurred in plugin / middleware -> fix for 500 (Thanks @hhamana)
* Better (custom) exceptions with a base `StarletteContextError` (Thanks @hhamana)

## [0.3.2] - 2021-04-22

* `ContextDoesNotExistError` is raised when context object can't be accessed. Previously it was `RuntimeError`. For backwards compatibility, it inherits from `RuntimeError` so it shouldn't result in any regressions.
* Added `py.typed` file so your mypy should never complain (Thanks @ginomempin)

## [0.3.1] - 2020-10-17

* Add `ApiKeyPlugin` plugin for `X-API-Key` header

## [0.3.0] - 2020-10-10

* Add `RawContextMiddleware` for `Streaming` and `File` responses
* Add flake8, isort, mypy
* Small refactor of the base plugin, moved directories and removed one redundant method (potentially breaking changes)

## [0.2.3] - 2020-07-27

* Add docs on read the docs
* Fix bug with `force_new_uuid=True` returning the same uuid constantly
* Due to ^ a lot of tests had to be refactored as well

## [0.2.2] - 2020-04-26

* For correlation id and request id plugins, add support for enforcing the generation of a new value
* For ^ plugins add support for validating uuid. It's a default behavior so will break things for people who don't use uuid4 there. If you don't want this validation, you need to pass validate=False to the plugin
* You can now check if context is available (Thanks @VukW)

## [0.2.1] - 2020-04-18

* Dropped with_plugins from the middleware as Starlette has it's own way of doing this
* Due to ^ this change some tests are simplified
* If context is not available no LookupError will be raised, instead there will be RuntimeError, because this error might mean one of two things: user either didn't use ContextMiddleware or is trying to access context object outside of request-response cycle

## [0.2.0] - 2020-02-21

* Changed parent of context object. More or less the API is the same but due to this change the implementation itself is way more simple and now it's possible to use .items() or keys() like in a normal dict, out of the box. Still, unpacking `**kwargs` is not supported and I don't think it ever will be. I tried to inherit from the builtin dict but nothing good came out of this. Now you access context as dict using context.data, not context.dict()
* There was an issue related to not having awaitable plugins. Now both middleware and plugins are fully async compatible. It's a breaking change as it forces to use await, hence new minor version

## [0.1.6] - 2020-01-02

* Breaking changes
* One middleware, one context, multiple plugins for middleware
* Very easy testing and writing custom plugins

## [0.1.5] - 2020-01-01

* Lint
* Tests (100% cov)
* Separate class for header constants
* BasicContextMiddleware add some logic

## [0.1.4] - 2019-12-31

* get_many in context object
* cicd improvements
* type annotations

**MVP until 0.1.4**
* experiments and tests with ContextVar

[0.3.6]: https://github.com/tomwojcik/starlette-context/compare/v0.3.5...v0.3.6
[0.3.5]: https://github.com/tomwojcik/starlette-context/compare/v0.3.4...v0.3.5
[0.3.4]: https://github.com/tomwojcik/starlette-context/compare/v0.3.3...v0.3.4
[0.3.3]: https://github.com/tomwojcik/starlette-context/compare/v0.3.2...v0.3.3
[0.3.2]: https://github.com/tomwojcik/starlette-context/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/tomwojcik/starlette-context/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/tomwojcik/starlette-context/compare/v0.2.3...v0.3.0
[0.2.3]: https://github.com/tomwojcik/starlette-context/compare/0.2.2...v0.2.3
[0.2.2]: https://github.com/tomwojcik/starlette-context/compare/0.2.1...0.2.2
[0.2.1]: https://github.com/tomwojcik/starlette-context/compare/0.2.0...0.2.1
[0.2.0]: https://github.com/tomwojcik/starlette-context/compare/0.1.6...0.2.0
[0.1.6]: https://github.com/tomwojcik/starlette-context/compare/0.1.5...0.1.6
[0.1.5]: https://github.com/tomwojcik/starlette-context/compare/0.1.4...0.1.5