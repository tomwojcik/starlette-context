from starlette_context.header_keys import HeaderKeys


def test_consistent_header_keys_format():
    for member in HeaderKeys:
        assert member.__format__("") == member.value
