========
Examples
========

**********************************
Set context in middleware and view
**********************************

.. code-block:: python

   from starlette.applications import Starlette
   from starlette.requests import Request
   from starlette.responses import JSONResponse

   import uvicorn
   from starlette_context import context
   from starlette_context.middleware import ContextMiddleware

   app = Starlette(debug=True)


   @app.route("/")
   async def index(request: Request):
       context["view"] = True
       return JSONResponse(context.data)


   class ContextFromMiddleware(ContextMiddleware):
       async def set_context(self, request: Request) -> dict:
           return {"middleware": True}


   app.add_middleware(ContextFromMiddleware)


   uvicorn.run(app, host="0.0.0.0")

**************************
Log json with request info
**************************

.. code-block:: python

   # app.py
   from starlette.applications import Starlette
   from starlette.middleware import Middleware
   from starlette.requests import Request
   from starlette.responses import JSONResponse

   import uvicorn
   from examples.example_with_logger.logger import log
   from starlette_context import context, middleware, plugins

   middleware = [
       Middleware(
           middleware.ContextMiddleware,
           plugins=(
               plugins.CorrelationIdPlugin(),
               plugins.RequestIdPlugin(),
               plugins.DateHeaderPlugin(),
               plugins.ForwardedForPlugin(),
               plugins.UserAgentPlugin(),
           ),
       )
   ]

   app = Starlette(debug=True, middleware=middleware)


   @app.route("/")
   async def index(_: Request):
       log.info("Log from view")
       return JSONResponse(context.data)


   uvicorn.run(app, host="0.0.0.0")

.. code-block:: python

   # logger.py
   import logging
   import sys

   from pythonjsonlogger import jsonlogger  # pip install python-json-logger
   from starlette_context import context

   global_logger = logging.getLogger("logger_test")
   handler = logging.StreamHandler(sys.stdout)
   handler.setLevel(logging.DEBUG)

   formatter = jsonlogger.JsonFormatter()

   handler.setFormatter(formatter)

   global_logger.addHandler(handler)


   class MyApiLoggingAdapter(logging.LoggerAdapter):
       def __init__(self, logger, extra=None):
           if extra is None:
               extra = {}
           super(MyApiLoggingAdapter, self).__init__(logger, extra)

       def process(self, msg, kwargs):
           extra = self.extra.copy()
           extra.update(context.data)  # <----  here we are basically adding context to log
           kwargs["extra"] = extra
           return msg, kwargs


   log = MyApiLoggingAdapter(global_logger)

