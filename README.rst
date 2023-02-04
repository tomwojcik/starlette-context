|Test Suite| |Python| |PyPI version| |codecov| |Docs| |Downloads|

starlette context
=================

Middleware for Starlette that allows you to store and access the context
data of a request. Can be used with logging so logs automatically use
request headers such as x-request-id or x-correlation-id.

Resources:

-  **Source**: https://github.com/tomwojcik/starlette-context
-  **Documentation**: https://starlette-context.readthedocs.io/
-  **Changelog**:
   https://starlette-context.readthedocs.io/en/latest/changelog.html

Installation
~~~~~~~~~~~~

.. code-block:: console

   $ pip install starlette-context

Requirements
~~~~~~~~~~~~

Should be working fine on 3.7+.
Official support starts at 3.8.

Dependencies
~~~~~~~~~~~~

-  ``starlette``

Example
~~~~~~~

.. code:: python

   import uvicorn

   from starlette.applications import Starlette
   from starlette.middleware import Middleware
   from starlette.requests import Request
   from starlette.responses import JSONResponse

   from starlette_context import context, plugins
   from starlette_context.middleware import RawContextMiddleware

   middleware = [
       Middleware(
           RawContextMiddleware,
           plugins=(
               plugins.RequestIdPlugin(),
               plugins.CorrelationIdPlugin()
           )
       )
   ]

   app = Starlette(middleware=middleware)


   @app.route("/")
   async def index(request: Request):
       return JSONResponse(context.data)


   uvicorn.run(app, host="0.0.0.0")

In this example the response contains a json with

.. code:: json

   {
     "X-Correlation-ID":"5ca2f0b43115461bad07ccae5976a990",
     "X-Request-ID":"21f8d52208ec44948d152dc49a713fdd"
   }

Context can be updated and accessed at anytime if it’s created in the
middleware.

Sponsorship
~~~~~~~~~~~

A huge thank you to `Adverity <https://www.adverity.com/>`__ for
sponsoring the development of this OSS library in 2022.

Contribution
~~~~~~~~~~~~

See the guide on `read the
docs <https://starlette-context.readthedocs.io/en/latest/contributing.html#contributing>`__.

.. |Test Suite| image:: https://github.com/tomwojcik/starlette-context/actions/workflows/test-suite.yml/badge.svg
   :target: https://github.com/tomwojcik/starlette-context/actions/workflows/test-suite.yml
.. |Python| image:: https://img.shields.io/badge/python-3.8+-blue.svg
   :target: https://www.python.org/downloads/release/python-370/
.. |PyPI version| image:: https://badge.fury.io/py/starlette-context.svg
   :target: https://badge.fury.io/py/starlette-context
.. |codecov| image:: https://codecov.io/gh/tomwojcik/starlette-context/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/tomwojcik/starlette-context
.. |Docs| image:: https://readthedocs.org/projects/pip/badge/?version=latest
   :target: https://starlette-context.readthedocs.io/
.. |Downloads| image:: https://img.shields.io/pypi/dm/starlette-context
