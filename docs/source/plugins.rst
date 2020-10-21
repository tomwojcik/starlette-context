=======
Plugins
=======

Context plugins allow you to extract any data you want from the request and store it in the context object.
I wrote plugins for the most common use cases that come to my mind, like extracting Correlation ID.
If you want to write your own plugin or modify existing ones, it's super simple.

************
How to use
************

You add as many plugins as you want to your middleware. You pass them to the middleware accordingly to the Starlette standard.

.. code-block:: python

   from starlette.applications import Starlette
   from starlette.middleware import Middleware
   from starlette_context import plugins
   from starlette_context.middleware import ContextMiddleware

   middleware = [
       Middleware(
           ContextMiddleware,
           plugins=(
               plugins.RequestIdPlugin(),
               plugins.CorrelationIdPlugin()
           )
       )
   ]

   app = Starlette(middleware=middleware)

*******
API Key
*******

Extracts header "X-API-Key" and keeps it in context.

**************
Correlation ID
**************

Extracts header "X-Correlation-ID" and keeps it in context.
You can pass `force_new_uuid=True` to enforce the creation of a new UUID.

***********
Date Header
***********

Extracts header "Date" and keeps it in context as a datetime.

*************
Forwarded For
*************

Extracts header "X-Forwarded-For" and keeps it in context.

**********
Request ID
**********

Extracts header "X-Request-ID" and keeps it in context.
You can pass `force_new_uuid=True` to enforce the creation of a new UUID.
It validates the header value is a valid UUID, and raises a ValueError('Wrong uuid').
Pass `validate=False` to disable the check, or `validation_error=your_error`to raise a different error.


**********
User Agent
**********

Extracts header "User-Agent" and keeps it in context.
