==========
Testing
==========


As part of your application logic flow, you will come to functions that expect the context to be available with specific data at runtime.

Testing such functions while very much valid during usual server runtime, may be trickier in a testing environnment, as it is not during an actual request-response cycle.
While it can be done in a full-blown integration test, if you want to test the functionality of your function extensively while keeping it to a limited scope during unit test,
you can use the ``request_cycle_context`` context manager.

.. code-block:: python

    import logging
    from starlette_context import context, request_cycle_context

    # original function assuming a context available
    def original_function():
        client_id = context["x-client-id"]
        return client_id

    # test
    def test_my_function():
        assumed_context = {"x-client-id": "unit testing!"}
        with request_cycle_context(assumed_context):
            assert original_function() == "unit testing!"


Or using pytest fixture

.. code-block:: python

    from starlette_context import context, request_cycle_context
    from starlette_context.ctx import _Context
    from starlette_context.errors import ConfigurationError


    @pytest.fixture
    def ctx_store():
        return {"a": 0, "b": 1, "c": 2}


    @pytest.fixture
    def mocked_context(ctx_store) -> None:
        with request_cycle_context(ctx_store):
            yield context

    def test_my_function(mocked_context, ctx_store):
        assert mocked_context == ctx_store
