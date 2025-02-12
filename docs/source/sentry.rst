=================
Sentry and FastAPI
=================

By adding a custom middleware, you can automatically tag Sentry transactions with a unique transaction identifier, which is retrieved from the request context. This enables you to correlate errors reported in Sentry with the corresponding HTTP requests, thereby enhancing debugging and performance monitoring.

The implementation leverages the Sentry SDK to access the current isolation scope and then sets a tag named "transaction_id" using a value obtained from the context (you could use correlation ID as well).

Here's an example of how to integrate Sentry with FastAPI:

.. code-block:: python

  import sentry_sdk
  from fastapi import FastAPI
  from starlette.middleware.base import RequestResponseEndpoint
  from starlette.requests import Request
  from starlette.responses import Response
  from starlette_context import context, plugins
  from starlette_context.header_keys import HeaderKeys
  from starlette_context.middleware import RawContextMiddleware

  def add_middleware(app: FastAPI):
    @app.middleware("http")
    async def sentry_transaction_id_middleware(
      request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
      # Retrieve the Sentry isolation scope.
      # Tag the transaction with a unique ID from the request context.
      scope = sentry_sdk.get_isolation_scope()
      scope.set_tag("transaction_id", context[HeaderKeys.request_id])
      return await call_next(request)

