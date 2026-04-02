from molbatch.utils.chains import parse_chain_string


def test_parse_chain_string_compact():
    assert parse_chain_string("XYZ") == ["X", "Y", "Z"]


def test_parse_chain_string_split():
    assert parse_chain_string("XA XB") == ["XA", "XB"]
