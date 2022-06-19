==============
Context object
==============

The context object utilizes ``ContextVar`` to store the information.
This ``ContextVar`` is a native Python object, introduced in Python 3.7.
For more information, see the official docs of `contextvars <https://docs.python.org/3/library/contextvars.html>`_.

.. warning::
    If you see ``ContextDoesNotExistError`` please see :ref:`errors`.

The idea was to create something like a ``g`` object in ``Flask``.

In ``Django`` there's no similar, builtin solution, though it can be compared to anything that allows you to store some
data in the thread such as `django-currentuser <https://github.com/PaesslerAG/django-currentuser>`_ or `django-crum <https://github.com/ninemoreminutes/django-crum>`_.

The interface hides the implementation, you can use the ``context`` object as if it was a native ``dict``.
Most significant difference is that you can't serialize the context object itself.
You'd have to use ``json.dumps(context.data)``, as ``.data`` returns a ``dict``.
Following operations work as expected

 - ``**context`` (``dict`` unpacking)
 - ``context["key"]``
 - ``context.get("key")``
 - ``context.items()``
 - ``context["key"] = "value"``

To make it available during the request-response cycle, it needs to be instantiated in the Starlette app with one of the middlewares,
or the ``request_cycle_context`` context manager, which can be useful in FastAPI Depends or unit tests requiring an available context.
The middleware approach offer extended capability the form of plugins to process and extend the request, but needs to redefine the error response in case those plugins raise an Exception.
The context manager approach is more barebone, which likely will lead you to implement the initial context population yourself.
