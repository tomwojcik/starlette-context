import pytest

from starlette_context.ctx import Context


@pytest.fixture(scope="function", autouse=True)
def ctx_store():
    return {"a": 0, "b": 1, "c": 2}


@pytest.fixture(scope="function", autouse=True)
def mocked_context(monkeypatch, ctx_store) -> Context:
    monkeypatch.setattr(
        "starlette_context.ctx.Context.store", ctx_store.copy()
    )
    return Context()


def test_ctx_init():
    with pytest.raises(AttributeError):
        Context(test=True)


def test_ctx_eq(mocked_context: Context, ctx_store: dict):
    assert ctx_store == mocked_context


def test_ctx_repr(mocked_context: Context, ctx_store: dict):
    assert f"<Context: {ctx_store}>" == mocked_context.__repr__()


def test_ctx_len(mocked_context: Context, ctx_store: dict):
    assert 3 == len(mocked_context)


def test_ctx_dict(mocked_context: Context, ctx_store: dict):
    assert ctx_store == mocked_context.dict()


def test_ctx_get_many(mocked_context: Context, ctx_store: dict):
    expected = {k: ctx_store.get(k) for k in ["a", "b", "z"]}
    actual = mocked_context.get_many("a", "b", "z")
    assert 3 == len(actual)
    assert expected == actual
    assert expected["z"] is None


def test_ctx_update(mocked_context: Context, ctx_store: dict):
    update_kwargs = {"c": 5, "d": 6}
    ctx_store.update(**update_kwargs)
    mocked_context.update(**update_kwargs)
    assert ctx_store == mocked_context
    assert mocked_context["c"] == 5
    assert mocked_context["d"] == 6


def test_ctx_del(mocked_context: Context, ctx_store: dict):
    del mocked_context["a"]
    del ctx_store["a"]
    assert "a" not in mocked_context
    assert "a" not in mocked_context.dict()
    assert ctx_store == mocked_context


def test_ctx_iter(mocked_context: Context, ctx_store: dict):
    iterator = mocked_context.__iter__()

    assert next(iterator) == "a"
    assert next(iterator) == "b"
    assert next(iterator) == "c"
    with pytest.raises(StopIteration):
        next(iterator)
