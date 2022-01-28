==============
Context object
==============

The context object is kept in ``ContextVar`` created for the request that is being processed asynchronously.
This ``ContextVar`` is a python object that has been introduced with 3.7.
For more info go see the official docs of `contextvars <https://docs.python.org/3/library/contextvars.html>`_.

.. warning::
    If you see ``ContextDoesNotExistError`` please see :ref:`errors`.

My idea was to create something like a ``g`` object in ``Flask``.

In ``Django`` I think there's no builtin similar solution but it can be compared to anything that allows you to store some
data in the thread such as `django-currentuser <https://github.com/PaesslerAG/django-currentuser>`_ or `django-crum <https://github.com/ninemoreminutes/django-crum>`_.

I wanted the interface to be as pythonic as possible so it mimics a ``dict``.
Most significant difference with ``dict`` is that you can't unpack or serialize the context object itself.
You'd have to use ``**context.data`` and ``json.dumps(context.data)`` accordingly, as ``.data`` returns a ``dict``.
Following operations work as expected

 - ``context["key"]``
 - ``context.get("key")``
 - ``context.items()``
 - ``context["key"] = "value"``


To make it available during the request-response cycle, it needs to be instantiated in the Starlette app with one of the middlewares,
or the ``starlette_context`` context manager, which can be useful in FastAPI Depends or unit tests requiring an available context.
The middleware approach offer extended capability the form of plugins to process and extend the request, but needs to redefine the error response in case those plugins raise an Exception.
The context manager approach is more barebone, which likely will lead you to implement the initial context population yourself.
