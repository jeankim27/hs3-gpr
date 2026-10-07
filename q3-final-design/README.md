# Q3 · Realistic scenes and final design (weeks 21–30)

**The question this quarter answers:** does it find a lava tube under realistic lunar conditions,
within the spacecraft's limits?
**Exit:** final design report, a frozen register, and a simulation anyone can rerun.

## Deliverables

- [ ] **D3.1 Realistic terrain** · [`scenes.md`](scenes.md) · owner: scene · due week 22
  LOLA elevation tiles over at least one target site; facet-based surface clutter; roughness.
- [ ] **D3.2 Realistic subsurface** · [`scenes.md`](scenes.md) · owner: scene · due week 23
  Variable regolith thickness, basalt flow layers, tube geometry and loss tangents from literature.
- [ ] **D3.3 Error sources** · `hs3gpr/sim/` · owner: radar-hw · due week 24
  Orbit and attitude knowledge errors, clock phase noise, altitude variation, ADC clipping, interference tones.
- [ ] **D3.4 Clutter discrimination demo** · notebook · owner: processing · due week 25
  Radargram next to its clutter simulation; candidates that survive.
- [ ] **D3.5 Detectability map** · [`analysis-plan.md`](analysis-plan.md) · owner: systems · due week 26
  Smallest detectable tube vs depth across `tan_delta_sweep` (Monte Carlo).
- [ ] **D3.6 Trades rerun, register frozen** · `params/variables.yaml` · owner: everyone · due week 28
- [ ] **D3.7 System closure** · [`closure.md`](closure.md) · owner: systems · due week 28
  Energy per orbit, data per day vs downlink, mass and volume, observation plan, requirement compliance.
- [ ] **D3.8 Final design report and presentation** · [`final-report-outline.md`](final-report-outline.md) · owner: everyone · week 30

**Stretch:** a small full-wave check of the tube response with gprMax (`warren2016`), or a bench test of
chirp generation and pulse compression.

## Weekly plan

| Weeks | Focus |
|---|---|
| 21–22 | Terrain from LOLA; clutter facets |
| 23–24 | Realistic subsurface; error sources |
| 25–26 | Clutter discrimination; detectability Monte Carlo |
| 27–28 | Rerun trades in the sim; freeze the register; close budgets |
| 29–30 | Final report and presentation |

## Variables to pin down this quarter

Everything marked **Q3** in [`params/REGISTER.md`](../params/REGISTER.md#q3), and every remaining
🟡 assumed variable becomes 🔵 derived or 🟢 frozen (or is explained in the report).

## Definition of done for the whole project

One command takes the register to simulated raw data, a processed radargram, detection metrics and
power/data budgets, and anyone on the team can rerun it from a fresh clone.
