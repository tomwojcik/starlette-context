==========
Middleware
==========

There are two middlewares you can use. They achieve more or less the same thing.

``ContextMiddleware`` inherits from ``BaseHTTPMiddleware`` which is an interface prepared by ``encode``.
That is, in theory, the "normal" way of creating a middleware. It's simple and convenient.
However, if you are using StreamingResponse, you might bump into memory issues. See
- https://github.com/encode/starlette/issues/919
- https://github.com/encode/starlette/issues/1012

Authors `discourage the use of BaseHTTPMiddleware https://github.com/encode/starlette/issues/1012#issuecomment-673461832`_ in favor of what they call "raw middleware".
That's why I created a new one. It does more or less the same thing, but instead of creating the entire ``Request`` object,
only ``HTTPConnection`` is instantiated. That I think will be sufficient to mitigate this issue.

It is entirely possible that ``ContextMiddleware`` will be removed in the future release. Therefore, if possible, use only ``RawContextMiddleware``.

.. warning::

    The `enrich_response` method won't run for unhandled exceptions.
    Even if your tried to run it in your own 500 handler, the context won't be available in the handler as that's
    how Starlette handles 500 (it's the last middleware to be run).
    Therefore, at the current state of Starlette and this library, no response headers will be set for 500 responses either.

*****************
ContextMiddleware
*****************

.. code-block:: python

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        _starlette_context_token: Token = _request_scope_context_storage.set(
            await self.set_context(request)
        )
        try:
            response = await call_next(request)
            for plugin in self.plugins:
                await plugin.enrich_response(response)

        finally:
            _request_scope_context_storage.reset(_starlette_context_token)

        return response

Firstly we create a "storage" for the context. The ``set`` method allows us to assign something to the context
when we create it therefore that's the best place to add everything that might come in
handy later on. You can always alter the context, so add/remove items from it, but each operation comes with some cost.

All ``plugins`` are executed when ``set_context`` method is called. If you want to add something else there you might
either write your own plugin or just overwrite the ``set_context`` method which returns a ``dict``. Just add anything you need to it before you return it.

Then, once the response is created, we iterate over plugins so it's possible to set some response headers based on the context contents.

Finally, the "storage" that async python apps can access is removed.



********************
RawContextMiddleware
********************

Tries to achieve the same thing but differently. Here you can access only the request-like object you will instantiate yourself.
You can even instantiate the ``Request`` object but it's not recommended because it might cause memory issues as it tries to evaluate the payload.
All plugins so far need only access to headers. If you still need to access the ``Request`` object or do something custom, you might want to
overwrite the `get_request_object` method.

So, in theory, this middleware does the same thing. Should be faster and safer. But have in mind that some black magic is
involved over here and `I'm waiting for the documentation on this subject https://github.com/encode/starlette/issues/1029`_ to be improved.
