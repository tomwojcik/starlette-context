=======
Plugins
=======

Context plugins allow you to extract any data you want from the request and store it in the context object.
I wrote plugins for the most common use cases that come to my mind, like extracting Correlation ID.
You can extend the built-in plugins and/or implement your own too.


==============
Using a plugin
==============

You may add as many plugins as you want to your middleware. You pass them to the middleware accordingly to the Starlette standard.

There may be a validation error occuring while processing the request in the plugins, which requires sending an error response.
Starlette however does not let middleware use the regular error handler
(`more details on this <https://www.starlette.io/exceptions/#errors-and-handled-exceptions>`_),
so middlewares facing a validation error have to send a response by themselves.

By default, the response sent will be a 400 with no body or extra header, as a Starlette `Response(status_code=400)`.
This response can be customized at both middleware and plugin level.

*************
Example usage
*************


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

You can use the middleware without plugin, it will only create the context for the request and not populate it directly.

================
Built-in plugins
================

starlette_context includes the following plugins you can import and use as shown above.
They are all accessible from  the `plugins` module.

Do note headers are case-insentive.
You can access the header value through the `<plugin class>.key` attribute,
or through the `starlette_context.header_keys.HeaderKeys` enum.


+-----------------+----------------------+-------------------+-----------------------------------+
| Plugin          | Class Name           | Extracted Header  | Notes                             |
+=================+======================+===================+===================================+
| API Key         | ApiKeyPlugin         | X-API-Key         |                                   |
+-----------------+----------------------+-------------------+-----------------------------------+
| Correlation ID  | CorrelationIdPlugin  | X-Correlation-ID  | UUID Plugin                       |
+-----------------+----------------------+-------------------+-----------------------------------+
| Date Header     | DateHeaderPlugin     | Date              | Keeps it in context as a datetime |
+-----------------+----------------------+-------------------+-----------------------------------+
| Forwarded For   | ForwardedForPlugin   | X-Forwarded-For   |                                   |
+-----------------+----------------------+-------------------+-----------------------------------+
| Request ID      | RequestIdPlugin      | X-Request-ID      | UUID Plugin                       |
+-----------------+----------------------+-------------------+-----------------------------------+
| User Agent      | UserAgentPlugin      | User-Agent        |                                   |
+-----------------+----------------------+-------------------+-----------------------------------+

************
UUID Plugins
************

UUID plugins accept ``force_new_uuid=True`` to enforce the creation of a new UUID. Defaults to ``False``.

If the target header has a value, it is validated to be a UUID (although kept as str in the context).
The error response if this validation fails can be customized with ``error_response=<Response object>``.
If no error response was specified, the middleware's default response will be used.
This validation can be turned off altogether with ``validate = False``.

=====================
Implementing your own
=====================

You can implement your plugin with variying degree of ease and flexibility.

*********
Easy mode
*********

You want a Plugin to extract a header that is not already available in the built-in ones.
There are indeed many, and your app may even want to use a custom header.

You just need to define the header key that you're looking for.

.. code-block:: python

    from starlette_context.plugins import Plugin

    class AcceptPlugin(Plugin):
        key = "Accept-Language"


That's it!
Just load it in your Middleware's plugins, and the value of the ``Accept-Language`` header will be put in the context,
which you can later get with ``context.get(AcceptPlugin.key)`` or ``context.get("Accept-Language")``
Hopefully you can use it to try and serve locally appropriate content.

You can notice the ``key`` attributes is both used to define the header you want to extract data from, and the key with which it is inserted in the context.


************
Intermediate
************

What if you don't want to put the header's value as a plain str, or don't even want to take data from the header?

You need to override the ``process_request`` method.
This gives you full access to the request, freedom to perform any processing in-between, and to return any value type.
Whatever is returned will be put in the context, again with the plugin's defined ``key``.

Any Exception raised from a middleware in Starlette would normally become a hard 500 response.
However you probably might find cases where you want to send a validation error instead.
For those cases, ``starlette_context`` provides a ``MiddleWareValidationError`` exception you can raise, and include a Starlette ``Response`` object.
The middleware class will take care of sending it.

You can also do more than extracting from requests, plugins also have a hook to modify the response before it's sent: ``enrich_response``.
It can access the Response object, and of course, the context, fully populated by that point.

Here an example of a plugin that extracts a `Session` from the request cookies, expects it to be encoded in base64,
attempts to decode it before returning it to the context. It generates an error response if it cannot be decoded.
On the way out, it retrieves the value it put in the context, and sets a new cookie.


.. code-block:: python

    import base64
    import logging
    from typing import Any, Optional, Union

    from starlette.responses import Response
    from starlette.requests import HTTPConnection, Request
    from starlette.types import Message

    from starlette_context.plugins import Plugin
    from starlette_context.errors import MiddleWareValidationError
    from starlette_context import context


    class MySessionPlugin(Plugin):
        # The returned value will be inserted in the context with this key
        key = "session_cookie"

        async def process_request(
            self, request: Union[Request, HTTPConnection]
        ) -> Optional[Any]:
            # access any part of the request
            raw_cookie = request.cookies.get("Session")
            if not raw_cookie:
                # it will be inserted a None in the context.
                return None

            try:
                decoded_cookie = base64.b64decode(bytes(raw_cookie, encoding="utf-8"))
            except Exception as e:
                logging.error("Raw cookie couldn't be decoded", exc_info=e)
                # create a response to signal the user of the invalid cookie.
                response = Response(
                    content=f"Invalid cookie: {raw_cookie}", status_code=400
                )
                # pass the response object in the exception so the middleware can abort processing and send it.
                raise MiddleWareValidationError("Cookie problem", error_response=response)
            return decoded_cookie

        async def enrich_response(self, response: Union[Response, Message]) -> None:
            # can access the pupulated context here.
            previous_cookie = context.get("session_cookie")
            response.set_cookie("PreviousSession", previous_cookie)
            response.set_cookie("Session", "SGVsbG8gV29ybGQ=")
            # mutate the response in-place, return nothing.

Do note, the type of request and response argument received depends on the middlewares class used.
The example shown here is valid for use with the ``ContextMiddleware``, receiveing built Starlette ``Request`` and ``Response`` objects.
In a ``RawContextMiddleware``, the hooks will receive ``HTTPConnection`` and ``Message`` objects passed as argument.
