# Q2 · End-to-end simulation (weeks 11–20)

**The question this quarter answers:** does the signal chain work end to end?
**Exit:** every verification test passes and the demo radargram shows a lava tube's roof and floor.

The code lives in [`hs3gpr/sim/`](../hs3gpr/sim/), one module per flowchart stage. This folder holds
the plans, the interface contract and the notebooks.

## Deliverables

- [ ] **D2.1 Architecture and interfaces** · [`interfaces.md`](interfaces.md) · owner: sim · due week 11
- [ ] **D2.2 Scene model v1** · `hs3gpr/sim/scene.py` · owner: scene · due week 12
  Flat surface, regolith over basalt, one void, point targets. *(Data classes exist; add what the echo generator needs.)*
- [ ] **D2.3 Echo generator + receiver/ADC** · `hs3gpr/sim/echo.py`, `receiver.py` · owners: scene, radar-hw · due week 16
  Point targets first (unlocks V-03), then layers and the void, then noise and quantization.
- [ ] **D2.4 Onboard model** · `hs3gpr/sim/onboard.py` · owner: processing · due week 15
  *(Presumming and requantization work; add data-volume accounting that matches BUDGET.md.)*
- [ ] **D2.5 Ground processing v1** · `hs3gpr/sim/ground.py` · owner: processing · due week 17
  *(Range compression, multilook and time-to-depth work; build SAR back-projection.)*
- [ ] **D2.6 Verification suite passes** · [`verification-plan.md`](verification-plan.md) · owner: sim · due week 19
- [ ] **D2.7 Demo radargram of a synthetic lava tube** · `notebooks/02_lava_tube_demo.ipynb` (create it) · owner: everyone (lead: sim) · week 20

## Weekly plan

| Weeks | Focus | Test that should turn green |
|---|---|---|
| 11–12 | Interfaces; point-target echoes | — |
| 13–14 | SAR back-projection on a point target | V-03 |
| 15–16 | Layers, void, noise, ADC | — |
| 17–18 | Full chain; compare with the budget | V-05 |
| 19–20 | Demo radargram; mid-project review | all |

Start with [`notebooks/01_sim_quickstart.ipynb`](notebooks/01_sim_quickstart.ipynb) to see what works today.

## Variables to pin down this quarter

Everything marked **Q2** in [`params/REGISTER.md`](../params/REGISTER.md#q2):
`sim_sample_rate`, `sim_track_length`, `void_model`, `snr_tolerance`, `trace_format`, `multilook_count`,
`sar_algorithm`, `detection_rule`.

## How to work on the simulation

```bash
pytest                         # run all tests; skipped ones say what to build next
pytest -k V03                  # run one test
```
Keep every number in the register; functions take `p` (the loaded register) as an argument.

## Exit criteria

- [ ] V-01 … V-06 pass (or each exception is written up in `verification-plan.md`)
- [ ] Simulated roof SNR within `snr_tolerance` of BUDGET.md
- [ ] Demo radargram shows surface, roof and floor at the right depths
- [ ] `interfaces.md` matches the code
