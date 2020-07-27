**************
Context object
**************

The context object is kept in ``ContextVar`` created for the request that is being processed asynchronously.
This ``ContextVar`` is a python object that has been introduced with 3.7 IIRC.
For more info go see the official docs of `contextvars <https://docs.python.org/3/library/contextvars.html>`_.

My idea was to create something like a ``g`` object in ``Flask``.

In ``Django`` I think there's no builtin similar solution but it can be compared to anything that allows you to store some
data in the thread such as `django-currentuser <https://github.com/PaesslerAG/django-currentuser>`_ or `django-crum <https://github.com/ninemoreminutes/django-crum>`_.

I wanted the interface to be as pythonic as possible so it mimics a ``dict``.
I think the only thing you can't do with it is unpack it using ``**context``.
You'd have to use ``**context.data`` for that.
Following operations work as expected

 - ``context["key"]``
 - ``context.get("key")``
 - ``context.items()``
 - ``context["key"] = "value"``

It will be available during the request-response cycle only if instantiated in the Starlette app with a ``ContextMiddleware``.
