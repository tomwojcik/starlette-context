from starlette_context.errors import StarletteContextError


def test_context_exception_is_catchable():
    """Ensure base context error inherits from Exception so that a normal
    try/except will catch it (test exists to prevent future regression)"""
    assert issubclass(StarletteContextError, Exception)
