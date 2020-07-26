**********
Middleware
**********

There's only one middleware (``ContextMiddleware``) as my idea was to extend its functionality using plugins.

Everything this middleware does can be seen in this single method but it's important to understand what is actually happening here.

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
