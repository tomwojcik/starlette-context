======
Errors
======

************************
ContextDoesNotExistError
************************

You will see this error whenever you try to access `context` object outside of the request-response cycle.
To be more specific:

 1. `ContextVar` store not created.

`RawContextMiddleware` uses `ContextVar` to create a storage that will be available within the request-response cycle.
So you will see the error if you are trying to access this object before using
`RawContextMiddleware` (fe. in another middleware), which instantiates `ContextVar` which belongs to event in the event loop.

 2. Wrong order of middlewares

.. code-block:: python

    class FirstMiddleware(BaseHTTPMiddleware): pass  # can't access context

    class SecondMiddleware(RawContextMiddleware): pass  # creates a context and can add into it

    class ThirdContextMiddleware(BaseHTTPMiddleware): pass  # can access context

    middlewares = [
        Middleware(FirstMiddleware),
        Middleware(SecondMiddleware),
        Middleware(ThirdContextMiddleware),
    ]


    app = Starlette(debug=True, middleware=middlewares)

As stated in the point no. 1, the order of middlewares matters. If you want to read more into order of execution of
middlewares, have a look at `#479 <https://github.com/encode/starlette/issues/479>`_.

Note, contents of this `context` object are gone when response pass `SecondMiddleware` in this example.

 3. Outside of the request-response cycle.

Depending on how you setup your logging, it's possible that your server (`uvicorn`) or other 3rd party loggers sometimes
will be able to access `context`, sometimes not. You might want to check if `context.exists()` to log it only if it's available.
