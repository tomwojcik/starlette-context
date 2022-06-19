==========
Quickstart
==========

************
Installation
************

The only dependency for this project is `Starlette <https://github.com/encode/starlette>`_, therefore this library
should work with all Starlette-based frameworks, such as `Responder <https://github.com/taoufik07/responder>`_,
`FastAPI <https://github.com/tiangolo/fastapi>`_ or `Flama <https://github.com/perdy/flama>`_.

.. code-block:: bash

   $ pip install starlette-context

**********
How to use
**********

You can access the magic ``context`` object if and only if these two conditions are met:
 * you access it within a request-response cycle
 * you used a ``ContextMiddleware`` or ``RawContextMiddleware`` in your ASGI app

Minimal working example

.. code-block:: python

   # app.py

   from starlette.middleware import Middleware
   from starlette.applications import Starlette

   from starlette_context.middleware import RawContextMiddleware

   middleware = [Middleware(RawContextMiddleware)]
   app = Starlette(middleware=middleware)



.. code-block:: python

   # views.py

   from starlette.requests import Request
   from starlette.responses import JSONResponse

   from starlette_context import context

   from .app import app

   @app.route("/")
   async def index(request: Request):
       return JSONResponse(context.data)
