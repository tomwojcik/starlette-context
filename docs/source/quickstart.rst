==========
Quickstart
==========

************
Installation
************

The only dependency for this project is `Starlette <https://github.com/encode/starlette>`_, therefore this library
should work with all Starlette-based frameworks, such as Responder, FastAPI or Flama.

.. code-block:: bash

   $ pip install starlette-context

**********
How to use
**********

You can access the magic `context` if and only if all those conditions are met:
 * you access it within a request-response cycle
 * you used a ``ContextMiddleware`` or ``RawContextMiddleware`` in your ASGI app

Minimal working example

.. code-block:: python

   # app.py

   from starlette.middleware import Middleware
   from starlette.applications import Starlette

   from starlette_context.middleware import ContextMiddleware

   middleware = [Middleware(ContextMiddleware)]
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
