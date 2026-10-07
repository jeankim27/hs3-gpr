# How we work

## The loop
1. **Issue.** Every piece of work starts as an issue. Use a template: *Deliverable task*, *Pin down / change a
   variable*, or *Research question*. Add the quarter label (`Q1`, `Q2`, `Q3`) and assign yourself.
2. **Branch.** Name it after the issue: `12-tan-delta-sources`. (On GitHub's web editor, choose
   *Create a new branch* when you commit.)
3. **Pull request.** Link the issue (`Closes #12`). Fill the checklist. Checks run automatically.
4. **Review.** One teammate reviews: are the sources real, are the units right, does the budget still pass?
5. **Merge.** The bot refreshes `params/REGISTER.md` and `q1-baseline/BUDGET.md`.

## Numbers
- Design numbers live **only** in `params/variables.yaml`. No numbers typed into code, notebooks or slides.
- SI units in the register. Write `20e6`, not `20 MHz`.
- Every value needs a `source`. "team" is allowed for assumptions, but say so.
- A 🟢 frozen value changes only with a decision record (`docs/decisions/`).

## IDs
| Prefix | Meaning | Where |
|---|---|---|
| `REQ-xx` | Requirement | `q1-baseline/1-requirements.md` |
| `EQ-xx` | Equation | `docs/equations.md` |
| `TS-x` | Trade study | `q1-baseline/2-trades/` |
| `DR-xxx` | Decision record | `docs/decisions/` |
| `Dq.n` | Deliverable n of quarter q | quarter READMEs |
| `V-xx` | Verification test | `q2-simulation/verification-plan.md` |

## Sources
- Add every paper or datasheet to the team's **Zotero group library** first.
- Cite by key (e.g. `kaku2017`) in the register's `source` field and in docs. Put page or table numbers in `notes`.
- Refresh `refs/references.bib` from Zotero (Better BibTeX export) when you add sources.

## Code
- Python, NumPy. Functions take the register `p` as an argument and use SI units.
- New equation → function in `hs3gpr/budget.py` with the EQ-ID in its docstring + a test in `tests/test_budget.py`
  + an entry in `docs/equations.md`.
- Run `pytest` before opening a pull request (the checks will run it anyway).

## Notebooks
- One notebook per analysis, named `NN_short_name.ipynb` inside the quarter folder.
- First cell: the setup cell (copy it from an existing notebook). Never edit values in a notebook; use
  `p.with_values(...)` for what-ifs.
- Re-run all cells before committing so the outputs match the code ("Restart & Run All").

## Weekly sync (30 min)
Use `docs/meetings/TEMPLATE.md`: register changes → deliverables → blockers for other subteams → decisions.
