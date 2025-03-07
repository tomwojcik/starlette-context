import pytest

from starlette_context import context, request_cycle_context
from starlette_context.ctx import _Context
from starlette_context.errors import ConfigurationError


@pytest.fixture(scope="function")
def ctx_store():
    return {"a": 0, "b": 1, "c": 2}


@pytest.fixture
def mocked_context(ctx_store) -> None:
    with request_cycle_context(ctx_store):
        yield context


def test_ctx_init():
    with pytest.raises(ConfigurationError):
        _Context(test=True)


def test_ctx_eq(mocked_context: _Context, ctx_store: dict):
    assert ctx_store == mocked_context


def test_ctx_repr_within_cycle(mocked_context: _Context, ctx_store: dict):
    assert (
        repr(mocked_context)
        == f"<starlette_context.ctx._Context {str(ctx_store)}>"
    )


def test_ctx_repr_out_of_cycle():
    assert repr(context) == "<starlette_context.ctx._Context {}>"


def test_ctx_data_str_within_cycle(mocked_context: _Context, ctx_store: dict):
    assert str(mocked_context.data) == str(ctx_store)


def test_ctx_data_str_out_of_cycle():
    assert str(context) == "{}"


def test_ctx_len(mocked_context: _Context, ctx_store: dict):
    assert len(mocked_context) == 3


def test_ctx_dict(mocked_context: _Context, ctx_store: dict):
    assert ctx_store == mocked_context.data


def test_ctx_update(mocked_context: _Context, ctx_store: dict):
    update_kwargs = {"c": 5, "d": 6}
    ctx_store.update(**update_kwargs)
    mocked_context.update(**update_kwargs)
    assert ctx_store == mocked_context
    assert mocked_context["c"] == 5
    assert mocked_context["d"] == 6


def test_ctx_del(mocked_context: _Context, ctx_store: dict):
    del mocked_context["a"]
    del ctx_store["a"]
    assert "a" not in mocked_context
    assert "a" not in mocked_context.data
    assert ctx_store == mocked_context


def test_ctx_iter(mocked_context: _Context, ctx_store: dict):
    iterator = mocked_context.__iter__()

    assert next(iterator) == "a"
    assert next(iterator) == "b"
    assert next(iterator) == "c"
    with pytest.raises(StopIteration):
        next(iterator)


def test_copy(mocked_context: _Context, ctx_store: dict):
    initial_data = mocked_context.data
    copied_data = mocked_context.copy()

    assert initial_data == copied_data
    copied_data["a"] = 123
    assert initial_data != copied_data

    assert id(initial_data) == id(mocked_context.data)
    assert id(mocked_context.copy()) != id(mocked_context.copy())


def test_dict_unpacking(mocked_context):
    def func(**kwargs):
        return sum(kwargs.values())

    assert func(**context) == 3
