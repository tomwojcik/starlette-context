==================
Usage with FastAPI
==================

Although FastAPI is built on top of Starlette, its popularity justifies having a section dedicated to FastAPI. As both are build on top of ASGI standard, ``starlette_context`` library is compatible with the FastAPI framework.

It can be used in the same way, with the same middlewares as a regular Starlette application.

FastAPI however offers another interesting feature with its Depends system and auto-generated OpenAPI documentation.
Using a middleware escapes this documentation generation, so if your app requires some specific headers from a middleware,
those would not appear in your API documentation, which is quite infortunate.

FastAPI ``Depends`` offers a way to solve this issue.
Instead of using middlewares, you can use a common Dependency, taking the data from the request it needs there, all while documenting it.
A FastAPI Depends with a ``yield`` can have a similar role to a middleware to manage the context, allowing code to be executed before as well as after the request.
You can find more information regarding this usage on the `FastAPI documentation <https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/>`_

The same ``request_cycle_context`` presented in :ref:`Testing` can be used to create this Depends
As an upside, errors raised there would folow the regular error handling.
As a downside, it cannot use the plugins system for middlewares, so the data from headers or else that you need must be implemented yourself, respecting FastAPI usage.

.. code-block:: python

    from starlette_context import context, request_cycle_context
    from fastapi import FastAPI, Depends, HTTPException, Header


    async def my_context_dependency(x_client_id = Header(...)):
        # When used a Depends(), this fucntion get the `X-Client_ID` header,
        # which will be documented as a required header by FastAPI.
        # use `x_client_id: str = Header(None)` for an optional header.

        data = {"x_client_id": x_client_id}
        with request_cycle_context(data):
            # yield allows it to pass along to the rest of the request
            yield

    # use it as Depends across the whole FastAPI app
    app = FastAPI(dependencies=[Depends(my_context_dependency)])

    @app.get("/")
    async def hello():
        client = context["x_client_id"]
        return f"hello {client}"
