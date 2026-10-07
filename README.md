# HS-3 GPR · Design model

Design and simulation of the ground-penetrating radar (radar sounder) on **HuskySat-3**, a lunar CubeSat
that will map lava tubes beneath the Moon's surface. Goal for this year: a complete design model that
works in simulation, built in three 10-week quarters.

| Quarter | Question | Folder |
|---|---|---|
| **Q1** · weeks 1–10 | Can the design close on paper? | [`q1-baseline/`](q1-baseline/) |
| **Q2** · weeks 11–20 | Does the signal chain work end to end? | [`q2-simulation/`](q2-simulation/) |
| **Q3** · weeks 21–30 | Does it find a lava tube under realistic conditions, within spacecraft limits? | [`q3-final-design/`](q3-final-design/) |

---

## New here? Start with these four steps

1. **See how the radar works:** the flowchart on the team website (link in the repo's *About* box), or
   [`website/flowchart.yaml`](website/flowchart.yaml) as text.
2. **See the numbers:** [`params/REGISTER.md`](params/REGISTER.md) (every design variable and its status) and
   [`q1-baseline/BUDGET.md`](q1-baseline/BUDGET.md) (what those numbers imply).
3. **See this quarter's work:** the README in the current quarter folder.
4. **Pick a task:** the [Issues](../../issues) tab, or ask in the weekly sync.

## Where things live

| Folder | What's in it |
|---|---|
| [`params/`](params/) | **The variable register.** The only place design numbers are typed. |
| [`q1-baseline/`](q1-baseline/), [`q2-simulation/`](q2-simulation/), [`q3-final-design/`](q3-final-design/) | Each quarter's deliverables: checklists, trade studies, plans, notebooks |
| [`hs3gpr/`](hs3gpr/) | Python code shared by all quarters: `budget.py` (Q1 equations), `sim/` (Q2–Q3 simulation) |
| [`docs/`](docs/) | [Equations](docs/equations.md), [decision records](docs/decisions/), [reading list](docs/reading-list.md), [glossary](docs/glossary.md), meeting notes |
| [`refs/`](refs/) | `references.bib`, exported from the team's Zotero group library |
| [`tests/`](tests/) | Checks that run on every pull request |
| [`tools/`](tools/) | `register.py` (check + build the register table), `build_site.py` (team website) |
| [`website/`](website/) | Optional team website: flowchart + live register (GitHub Pages) |

## The one rule

**A number lives in exactly one place: [`params/variables.yaml`](params/variables.yaml).**
Code, notebooks, `BUDGET.md`, `REGISTER.md` and the website all read it. To change a design value, change it
there (see [`params/README.md`](params/README.md)) and everything else follows.

## Run things

**In the browser (no installs):** Google Colab → *File → Open notebook → GitHub* → paste this repo's URL →
pick a notebook. The first cell asks for `owner/repo` and loads the code.

**On your computer:**
```bash
git clone <this repo's URL> && cd <repo folder>
pip install -r requirements.txt
python -m hs3gpr.budget          # the budget from the register
python tools/register.py         # check the register, rebuild REGISTER.md
pytest                           # all checks; skipped tests say what to build next
```

## How we work

Short version (full version in [`CONTRIBUTING.md`](CONTRIBUTING.md)):
**issue → branch → pull request → one reviewer → merge.** Cite a source for every number.
Big choices get a [decision record](docs/decisions/).

---

## One-time setup (team lead)

- [ ] Create the repo: easiest is **GitHub Desktop → File → Add local repository →** pick the unzipped `hs3-gpr` folder →
      *create a repository* → **Publish repository**. (Uploading in the browser works too, but your file browser may hide
      the `.github` folder and `.gitignore`; on macOS press ⌘⇧. in Finder to show them, and include them.)
- [ ] **Settings → Collaborators:** invite teammates (*Write* role)
- [ ] **Issues → Labels:** add `Q1`, `Q2`, `Q3`, `task`, `variable`, `research`, `decision`, `sim`, `docs`
- [ ] **Projects → New project → Board:** columns *To do / In progress / Review / Done*; add one issue per deliverable
- [ ] Replace owner roles (`systems`, `radar-hw`, …) in `params/variables.yaml` with GitHub usernames
- [ ] **Settings → Actions → General → Workflow permissions:** *Read and write* (lets the bot refresh REGISTER.md and BUDGET.md)
- [ ] Optional website: see [`website/README.md`](website/README.md) (two settings)
- [ ] Optional: **Settings → Branches →** protect `main` (require a pull request). If you do, the table-refresh bot can't push;
      run `python tools/register.py` and `python -m hs3gpr.budget --markdown q1-baseline/BUDGET.md` in your pull requests instead
- [ ] Add a license if the repo will be public (e.g. MIT)
- [ ] Create the Zotero group library and import `refs/references.bib`
