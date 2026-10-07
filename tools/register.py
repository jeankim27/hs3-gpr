"""Check the variable register and build the readable table.

    python tools/register.py            # check + write params/REGISTER.md + print progress
    python tools/register.py --check    # check only (used by GitHub Actions)
    python tools/register.py --json out.json   # also write JSON (used by the website)
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from hs3gpr.params import DEFAULT_PATH, QUARTERS, STATUSES, read_yaml, validate  # noqa: E402

OUT_MD = ROOT / "params" / "REGISTER.md"
STATUS_ICON = {"TBD": "🔴 TBD", "assumed": "🟡 assumed", "derived": "🔵 derived", "frozen": "🟢 frozen"}
QUARTER_TITLE = {"Q1": "Q1 · pin down by week 10", "Q2": "Q2 · pin down by week 20", "Q3": "Q3 · pin down by week 30"}
PREFIXABLE = {"Hz", "m", "s", "W", "B", "bit/s"}
PREFIXES = [(1e9, "G"), (1e6, "M"), (1e3, "k"), (1.0, ""), (1e-3, "m"), (1e-6, "µ"), (1e-9, "n")]


def pretty(value, unit):
    """20e6, 'Hz' → '20 MHz'. Text and lists pass through."""
    if value is None:
        return "TBD"
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, list):
        return ", ".join(pretty(v, unit) if isinstance(v, (int, float)) else str(v) for v in value)
    if not isinstance(value, (int, float)):
        return str(value)
    u = "" if unit in ("-", None) else unit
    if u in PREFIXABLE and value != 0:
        for scale, prefix in PREFIXES:
            if u == "m" and prefix in ("M", "G"):
                continue
            if abs(value) >= scale * 0.9999:
                return f"{_num(value / scale)} {prefix}{u}"
        return f"{_num(value / 1e-9)} n{u}"
    return f"{_num(value)} {u}".strip()


def _num(x):
    if float(x).is_integer():
        return f"{int(x):,}"
    return f"{x:.4g}"


def pretty_range(rng, unit):
    if not rng:
        return ""
    return f"{pretty(rng[0], unit)} – {pretty(rng[1], unit)}"


def progress_bar(fraction, width=10):
    filled = round(fraction * width)
    return "■" * filled + "□" * (width - filled)


def build_markdown(entries):
    lines = [
        "# Variable register",
        "",
        "> Generated from [`variables.yaml`](variables.yaml) by `python tools/register.py`. "
        "**Edit `variables.yaml`, not this file.** It is regenerated automatically when changes land on `main`.",
        "",
        "Status: 🔴 **TBD** no value yet · 🟡 **assumed** placeholder, needs a source or trade · "
        "🔵 **derived** backed by an analysis · 🟢 **frozen** agreed baseline (change only with a decision record)",
        "",
        "## Progress",
        "",
        "| Quarter | Variables | 🔴 TBD | 🟡 Assumed | 🔵 Derived | 🟢 Frozen | Pinned down (derived + frozen) |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for q in QUARTERS:
        qe = [e for e in entries.values() if e.get("quarter") == q]
        counts = {s: sum(1 for e in qe if e.get("status") == s) for s in STATUSES}
        pinned = counts["derived"] + counts["frozen"]
        frac = pinned / len(qe) if qe else 0.0
        lines.append(f"| [{q}](#{q.lower()}) | {len(qe)} | {counts['TBD']} | {counts['assumed']} | "
                     f"{counts['derived']} | {counts['frozen']} | {progress_bar(frac)} {frac:.0%} |")
    lines.append("")

    # who owes what
    tbd_q1 = [(k, e) for k, e in entries.items() if e.get("quarter") == "Q1" and e.get("status") == "TBD"]
    if tbd_q1:
        lines += ["### Q1 variables still TBD, by owner", ""]
        owners = sorted({e.get("owner") or "unassigned" for _, e in tbd_q1})
        for owner in owners:
            keys = [f"`{k}`" for k, e in tbd_q1 if (e.get("owner") or "unassigned") == owner]
            lines.append(f"- **{owner}** ({len(keys)}): " + ", ".join(keys))
        lines.append("")

    for q in QUARTERS:
        qe = {k: e for k, e in entries.items() if e.get("quarter") == q}
        if not qe:
            continue
        lines += [f'<a id="{q.lower()}"></a>', f"## {QUARTER_TITLE[q]}", ""]
        groups = []
        for e in qe.values():
            if e["group"] not in groups:
                groups.append(e["group"])
        for g in groups:
            lines += [f"### {g}", "",
                      "| Variable | Symbol | Value | Range considered | Status | Owner | Source |",
                      "|---|---|---|---|---|---|---|"]
            for k, e in qe.items():
                if e["group"] != g:
                    continue
                name = f"**{e['name']}**<br>`{k}`"
                sym = e.get("symbol") or ""
                lines.append(
                    f"| {name} | {sym} | {pretty(e.get('value'), e.get('unit'))} | "
                    f"{pretty_range(e.get('range'), e.get('unit'))} | {STATUS_ICON.get(e.get('status'), e.get('status'))} | "
                    f"{e.get('owner') or ''} | {e.get('source') or ''} |")
            lines.append("")
    return "\n".join(lines)


def build_json(entries):
    out = []
    for k, e in entries.items():
        item = {"key": k}
        item.update(e)
        item["display"] = pretty(e.get("value"), e.get("unit"))
        item["range_display"] = pretty_range(e.get("range"), e.get("unit"))
        out.append(item)
    return {"statuses": list(STATUSES), "quarters": list(QUARTERS), "variables": out}


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="only check; do not write REGISTER.md")
    ap.add_argument("--json", metavar="PATH", help="also write the register as JSON")
    args = ap.parse_args(argv)

    data = read_yaml(DEFAULT_PATH) or {}
    entries = data.get("variables") or {}
    errors = validate(entries)
    if errors:
        print(f"✖ {len(errors)} problem(s) in params/variables.yaml:")
        for e in errors:
            print("   -", e)
        return 1
    print(f"✔ params/variables.yaml is valid ({len(entries)} variables)")

    if args.json:
        pathlib.Path(args.json).write_text(json.dumps(build_json(entries), ensure_ascii=False, indent=1), encoding="utf-8")
    if args.check:
        return 0

    OUT_MD.write_text(build_markdown(entries) + "\n", encoding="utf-8")
    print(f"✔ wrote {OUT_MD.relative_to(ROOT)}")
    for q in QUARTERS:
        qe = [e for e in entries.values() if e.get("quarter") == q]
        counts = {s: sum(1 for e in qe if e.get("status") == s) for s in STATUSES}
        print(f"  {q}: {len(qe):>2} variables · " + " · ".join(f"{counts[s]} {s}" for s in STATUSES))
    return 0


if __name__ == "__main__":
    sys.exit(main())
