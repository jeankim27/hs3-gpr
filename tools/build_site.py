"""Build the team website into _site/ (GitHub Pages publishes that folder).

    python tools/build_site.py
    python -m http.server -d _site 8000      # then open http://localhost:8000

Reads website/flowchart.yaml, params/variables.yaml and the budget, and writes JSON
next to the HTML. Fails with a clear message if the flowchart file has a mistake.
"""

from __future__ import annotations

import json
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

from hs3gpr import budget  # noqa: E402
from hs3gpr.params import load, read_yaml  # noqa: E402
from register import build_json  # noqa: E402

SRC = ROOT / "website"
OUT = ROOT / "_site"
KINDS = {"hardware", "firmware", "software", "physics"}
PLACES = {"ground", "spacecraft", "moon", "downlink"}


def build_flowchart(doc):
    errors = []
    support_names = [s.get("name") for s in doc.get("support", [])]
    steps_out, n = [], 0
    stages = []
    for si, stage in enumerate(doc.get("stages", [])):
        where = f"stages[{si}] ({stage.get('name', '?')})"
        if stage.get("place") not in PLACES:
            errors.append(f"{where}: place must be one of {sorted(PLACES)}")
        st = {k: stage.get(k) for k in ("place", "place_label", "name", "arrow")}
        st["steps"] = []
        for step in stage.get("steps", []):
            n += 1
            sw = f"{where} → step {n} ({step.get('title', '?')})"
            if step.get("kind") not in KINDS:
                errors.append(f"{sw}: kind must be one of {sorted(KINDS)}")
            for u in step.get("uses", []) or []:
                if u not in support_names:
                    errors.append(f"{sw}: uses '{u}' but no support subsystem has that name {support_names}")
            for field in ("title", "summary"):
                if not step.get(field):
                    errors.append(f"{sw}: missing '{field}'")
            item = dict(step)
            item["n"] = n
            item["id"] = str(n)
            item["place_label"] = stage.get("place_label")
            item["stage"] = stage.get("name")
            st["steps"].append(item)
            steps_out.append(item)
        if stage.get("side_path"):
            side = dict(stage["side_path"])
            side["id"] = f"side-{si}"
            side["place_label"] = stage.get("place_label")
            side["stage"] = stage.get("name")
            st["side_path"] = side
        stages.append(st)
    support = []
    for s in doc.get("support", []):
        item = dict(s)
        item["id"] = "support-" + str(s.get("name", "")).lower().replace(" ", "-")
        item["feeds"] = [x["n"] for x in steps_out if s.get("name") in (x.get("uses") or [])]
        support.append(item)
    if errors:
        raise SystemExit("✖ website/flowchart.yaml has problems:\n   - " + "\n   - ".join(errors))
    out = {k: doc.get(k) for k in ("eyebrow", "title", "lede", "one_line", "assumptions", "loop_label")}
    out.update(stages=stages, support=support, n_steps=n)
    return out


def main():
    flow = build_flowchart(read_yaml(SRC / "flowchart.yaml"))
    entries = read_yaml(ROOT / "params" / "variables.yaml")["variables"]
    rows = budget.compute(load())

    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(SRC, OUT, ignore=shutil.ignore_patterns("README.md", "flowchart.yaml"))
    (OUT / "data").mkdir(exist_ok=True)
    for name, payload in (("flowchart.json", flow), ("register.json", build_json(entries)),
                          ("budget.json", budget.to_json(rows))):
        (OUT / "data" / name).write_text(json.dumps(payload, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print(f"✔ built _site/ ({flow['n_steps']} flowchart steps, {len(entries)} variables, {len(rows)} budget rows)")
    print("  preview: python -m http.server -d _site 8000  →  http://localhost:8000")


if __name__ == "__main__":
    main()
