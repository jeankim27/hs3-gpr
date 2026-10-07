"""The variable register must always be valid (this also runs on every pull request)."""

from hs3gpr.params import DEFAULT_PATH, QUARTERS, load, read_yaml, validate


def test_register_is_valid():
    errors = validate(read_yaml(DEFAULT_PATH)["variables"])
    assert not errors, "\n".join(errors)


def test_every_quarter_has_variables():
    p = load()
    quarters = {p.info(k)["quarter"] for k in p}
    assert set(QUARTERS) <= quarters


def test_scientific_notation_reads_as_numbers():
    p = load()
    assert isinstance(p["f_center"], (int, float)), "write numbers like 20e6, not '20e6' in quotes"


def test_what_if_copy_leaves_original_alone():
    p = load()
    q = p.with_values(f_center=5e6)
    assert q["f_center"] == 5e6
    assert p["f_center"] == load()["f_center"]
