# params · the variable register

| File | What it is | Edit it? |
|---|---|---|
| [`variables.yaml`](variables.yaml) | Every design number, with its status, source and owner | **Yes, this is the one** |
| [`REGISTER.md`](REGISTER.md) | Readable tables + progress per quarter, generated from the YAML | No (regenerated automatically) |

## Change a value (no installs needed)
1. Open `variables.yaml` on GitHub → pencil icon.
2. Edit `value` (SI units: write `20e6` for 20 MHz). If it is now backed by an analysis or a decision,
   change `status` and put the reference in `source`.
3. **Commit changes → Create a new branch → Propose changes**, then open the pull request.
4. The checks run (✅/❌ on the pull request). A teammate reviews and merges.
5. `REGISTER.md` and `q1-baseline/BUDGET.md` update by themselves on `main`.

Proposing a change you aren't sure about? Open an issue with the **Pin down / change a variable** template instead.

## Status lifecycle

```
🔴 TBD  ──►  🟡 assumed  ──►  🔵 derived  ──►  🟢 frozen
no value     placeholder       backed by an      agreed baseline;
             or estimate       analysis or TS    change only with a DR
```

## Conventions
- **Units:** SI in the file (Hz, m, s, W, bit/s, B). Tables show prefixes (MHz, km, µs) for you.
- **Owner:** a role tag. Our team: `systems`, `radar-hw`, `scene`, `processing`, `sim` (see [`docs/roles.md`](../docs/roles.md)). Other HS-3 subteams: `comms`, `eps`, `gnc`, `structures`.
  The Team table in the main README says who holds each role, so tags never need renaming.
- **Source:** a citation key from `refs/references.bib`, an equation (`EQ-04`), a trade (`TS-1`),
  a decision (`DR-001`), a notebook, or `team`.
- **New variable:** copy any block, give it a new lowercase key, fill every field.

## Check it on your computer
```bash
python tools/register.py           # validate + rebuild REGISTER.md
python tools/register.py --check   # validate only
```
