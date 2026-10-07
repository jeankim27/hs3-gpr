"""Load and check the variable register (params/variables.yaml).

Usage
-----
    from hs3gpr.params import load
    p = load()
    p["f_center"]                 # value in SI units (20000000.0), or None while TBD
    p.unit("f_center")            # "Hz"
    p.info("f_center")            # the full entry as a dict
    q = p.with_values(f_center=5e6, bandwidth=2e6)   # copy with changes, for what-ifs
"""

from __future__ import annotations

import copy
import pathlib
import re

import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_PATH = REPO_ROOT / "params" / "variables.yaml"

STATUSES = ("TBD", "assumed", "derived", "frozen")
QUARTERS = ("Q1", "Q2", "Q3")
REQUIRED_FIELDS = ("name", "unit", "status", "quarter", "group")
KNOWN_FIELDS = set(REQUIRED_FIELDS) | {
    "symbol", "value", "range", "owner", "source", "drives", "notes"}


class _Loader(yaml.SafeLoader):
    """SafeLoader that also reads 20e6 and 2.5e6 as numbers (plain PyYAML reads them as text)."""


_Loader.add_implicit_resolver(
    "tag:yaml.org,2002:float",
    re.compile(r"^[-+]?(?:\d[\d_]*(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?$"),
    list("-+0123456789."),
)


def read_yaml(path):
    with open(path, encoding="utf-8") as fh:
        return yaml.load(fh, Loader=_Loader)


class MissingValue(KeyError):
    """Raised when a calculation needs a variable that is still TBD."""

    def __init__(self, keys):
        self.keys = list(keys)
        super().__init__(", ".join(self.keys))

    def __str__(self):
        return ("still TBD in params/variables.yaml: " + ", ".join(self.keys)
                + " (give it a value to compute this)")


class Register:
    """Read-only view of the register. Values are in SI units."""

    def __init__(self, entries: dict, path=None):
        self._entries = entries
        self.path = path

    # dictionary-style access -------------------------------------------------
    def __getitem__(self, key):
        return self._entry(key).get("value")

    def __contains__(self, key):
        return key in self._entries

    def __iter__(self):
        return iter(self._entries)

    def __len__(self):
        return len(self._entries)

    def keys(self):
        return self._entries.keys()

    def items(self):
        return ((k, v.get("value")) for k, v in self._entries.items())

    # metadata -----------------------------------------------------------------
    def info(self, key) -> dict:
        return copy.deepcopy(self._entry(key))

    def unit(self, key) -> str:
        return self._entry(key).get("unit", "-")

    def status(self, key) -> str:
        return self._entry(key).get("status", "TBD")

    def entries(self) -> dict:
        return copy.deepcopy(self._entries)

    # helpers for calculations ---------------------------------------------------
    def require(self, *keys):
        """Return the values of `keys`; raise MissingValue listing any that are TBD."""
        missing = [k for k in keys if self[k] is None]
        if missing:
            raise MissingValue(missing)
        values = tuple(self[k] for k in keys)
        return values[0] if len(values) == 1 else values

    def with_values(self, **changes) -> "Register":
        """Copy of the register with some values changed (does not touch the file)."""
        entries = copy.deepcopy(self._entries)
        for key, value in changes.items():
            if key not in entries:
                raise KeyError(f"unknown variable '{key}'")
            entries[key]["value"] = value
        return Register(entries, self.path)

    def _entry(self, key):
        try:
            return self._entries[key]
        except KeyError:
            raise KeyError(f"'{key}' is not in params/variables.yaml") from None


def load(path=None) -> Register:
    """Load the register. Raises ValueError with every problem listed if it is invalid."""
    path = pathlib.Path(path) if path else DEFAULT_PATH
    data = read_yaml(path) or {}
    entries = data.get("variables") or {}
    errors = validate(entries)
    if errors:
        raise ValueError("Problems in " + str(path) + ":\n  - " + "\n  - ".join(errors))
    return Register(entries, path)


def validate(entries: dict) -> list[str]:
    """Return a list of human-readable problems (empty list = valid)."""
    errors = []
    if not isinstance(entries, dict) or not entries:
        return ["no variables found (expected a 'variables:' section)"]
    for key, e in entries.items():
        where = f"{key}:"
        if not re.fullmatch(r"[a-z][a-z0-9_]*", str(key)):
            errors.append(f"{where} key must be lowercase_with_underscores")
        if not isinstance(e, dict):
            errors.append(f"{where} must be a block of fields")
            continue
        for field in REQUIRED_FIELDS:
            if field not in e or e[field] in (None, ""):
                errors.append(f"{where} missing '{field}'")
        unknown = set(e) - KNOWN_FIELDS
        if unknown:
            errors.append(f"{where} unknown field(s) {sorted(unknown)} (typo?)")
        status = e.get("status")
        if status not in STATUSES:
            errors.append(f"{where} status '{status}' must be one of {', '.join(STATUSES)}")
        if e.get("quarter") not in QUARTERS:
            errors.append(f"{where} quarter '{e.get('quarter')}' must be one of {', '.join(QUARTERS)}")
        value = e.get("value")
        if status == "TBD" and value not in (None, "", []):
            errors.append(f"{where} has a value but status TBD (set status to assumed)")
        if status != "TBD" and value in (None, "", []):
            errors.append(f"{where} status '{status}' but no value (set a value or status TBD)")
        if isinstance(value, str) and _looks_numeric(value):
            errors.append(f"{where} value '{value}' is text; write it as a plain number like 20e6")
        rng = e.get("range")
        if rng is not None:
            if (not isinstance(rng, list) or len(rng) != 2
                    or not all(isinstance(x, (int, float)) for x in rng)):
                errors.append(f"{where} range must be [min, max] numbers")
            elif rng[0] > rng[1]:
                errors.append(f"{where} range min is larger than max")
            elif isinstance(value, (int, float)) and not isinstance(value, bool) \
                    and not (rng[0] <= value <= rng[1]):
                errors.append(f"{where} value {value} is outside its range {rng}")
        if status in ("derived", "frozen") and not e.get("source"):
            errors.append(f"{where} status '{status}' needs a source")
    return errors


def _looks_numeric(text: str) -> bool:
    return bool(re.fullmatch(r"\s*[-+]?\d[\d_]*(\.\d*)?([eE][-+]?\d+)?\s*", text))
