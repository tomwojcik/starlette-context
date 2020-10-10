==========
Middleware
==========

There are two middlewares you can use. They achieve more or less the same thing.

``ContextMiddleware`` inherits from ``BaseHTTPMiddleware`` which is an interface prepared by ``encode``.
That is, in theory, the "normal" way of creating a middleware. It's simple and convenient.
However, if you are using StreamingResponse, you might bump into memory issues. See
- https://github.com/encode/starlette/issues/919
- https://github.com/encode/starlette/issues/1012

Authors `discourage the use of BaseHTTPMiddleware <https://github.com/encode/starlette/issues/1012#issuecomment-673461832>`_ in favor of what they call "raw middleware".
That's why I created a new one. It does more or less the same thing, but instead of creating the entire ``Request`` object,
only ``HTTPConnection`` is instantiated. That I think will be sufficient to mitigate this issue.

It is entirely possible that ``ContextMiddleware`` will be removed in the future release.
It is also possible that authors will make some changes to the ``BaseHTTPMiddleware`` to fix this issue.
I'd advise to only use ``RawContextMiddleware``.

.. warning::

    The `enrich_response` method won't run for unhandled exceptions.
    Even if you use your own 500 handler, the context won't be available in it as that's
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

Firstly we create a "storage" for the context. The ``set_context`` method allows us to assign something to the context
on creation therefore that's the best place to add everything that might come in
handy later on. You can always alter the context, so add/remove items from it, but each operation comes with some cost.

All ``plugins`` are executed when ``set_context`` method is called. If you want to add something else there you might
either write your own plugin or just overwrite the ``set_context`` method which returns a ``dict``. Just add anything you need to it before you return it.

Then, once the response is created, we iterate over plugins so it's possible to set some response headers based on the context contents.

Finally, the "storage" that async python apps can access is removed.



********************
RawContextMiddleware
********************

.. code-block:: python

    @staticmethod
    def get_request_object(
        scope, receive, send
    ) -> Union[Request, HTTPConnection]:
        # here we instantiate HTTPConnection instead of a Request object
        # because using the latter one might cause some memory problems
        # If you need the payload etc for your plugin instantiate Request(scope, receive, send)
        return HTTPConnection(scope)

    async def __call__(
        self, scope: Scope, receive: Receive, send: Send
    ) -> None:
        if scope["type"] not in ("http", "websocket"):  # pragma: no cover
            await self.app(scope, receive, send)
            return

        async def send_wrapper(message: Message) -> None:
            for plugin in self.plugins:
                await plugin.enrich_response(message)
            await send(message)

        request = self.get_request_object(scope, receive, send)

        _starlette_context_token: Token = _request_scope_context_storage.set(
            await self.set_context(request)  # noqa
        )

        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            _request_scope_context_storage.reset(_starlette_context_token)

Tries to achieve the same thing but differently. Here you can access only the request-like object you will instantiate yourself.
You might want to instantiate the ``Request`` object but ``HTTPConnection`` seems to be the interface that is needed as it gives
us an access to the headers. If you need to evaluate payload in the middleware, return ``Request`` object from the
``get_request_object`` instead.

So, in theory, this middleware does the same thing. Should be faster and safer. But have in mind that some **black magic is
involved here** and `I'm waiting for the documentation on this subject <https://github.com/encode/starlette/issues/1029>`_ to be improved.
