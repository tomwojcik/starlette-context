import pytest
from starlette_context.ctx import Context


def test_ctx_init():
    with pytest.raises(AttributeError):
        Context(test=True)


@pytest.fixture(scope="function", autouse=True)
def ctx_store():
    return {'a': 0, 'b': 1, 'c': 2}


@pytest.fixture(scope="function", autouse=True)
def context(monkeypatch, ctx_store) -> Context:
    monkeypatch.setattr(
        'starlette_context.ctx.Context.store',
        ctx_store.copy()
    )
    return Context()


def test_ctx_eq(context: Context, ctx_store: dict):
    assert ctx_store == context


def test_ctx_repr(context: Context, ctx_store: dict):
    assert f"<Context: {ctx_store}>" == context.__repr__()


def test_ctx_len(context: Context, ctx_store: dict):
    assert 3 == len(context)


def test_ctx_dict(context: Context, ctx_store: dict):
    assert ctx_store == context.dict()


def test_ctx_get_many(context: Context, ctx_store: dict):
    expected = {k: ctx_store.get(k) for k in ['a', 'b', 'z']}
    actual = context.get_many('a', 'b', 'z')
    assert 3 == len(actual)
    assert expected == actual
    assert expected['z'] is None


def test_ctx_update(context: Context, ctx_store: dict):
    update_kwargs = {'c': 5, 'd': 6}
    ctx_store.update(**update_kwargs)
    context.update(**update_kwargs)
    assert ctx_store == context
    assert context['c'] == 5
    assert context['d'] == 6


def test_ctx_del(context: Context, ctx_store: dict):
    del context['a']
    del ctx_store['a']
    assert 'a' not in context
    assert 'a' not in context.dict()
    assert ctx_store == context


def test_ctx_iter(context: Context, ctx_store: dict):
    iterator = context.__iter__()

    assert next(iterator) == 'a'
    assert next(iterator) == 'b'
    assert next(iterator) == 'c'
    with pytest.raises(StopIteration):
        next(iterator)
