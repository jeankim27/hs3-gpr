# Q1 · Design baseline (weeks 1–10)

**The question this quarter answers:** can the design close on paper?
**Exit:** the baseline review in week 10 ([`4-baseline-review.md`](4-baseline-review.md)).

## Deliverables

Open one GitHub issue per deliverable (**Issues → New issue → Deliverable task**) and tick the box here when it is done.

- [ ] **D1.1 Requirements flow-down** · [`1-requirements.md`](1-requirements.md) · owner: systems · due week 3
  Turn "map lava tubes" into numbers: smallest tube, roof depth, SNR threshold, resolutions, sites.
- [ ] **D1.2 Variable register v1** · [`params/variables.yaml`](../params/variables.yaml) · owner: everyone · due week 9
  No Q1 variable left 🔴 TBD; each has a value or range, a source and an owner.
- [ ] **D1.3 Radar budget** · [`BUDGET.md`](BUDGET.md) + [`notebooks/01_radar_budget.ipynb`](notebooks/01_radar_budget.ipynb) · owner: systems · due week 7
  SNR vs depth for 2–3 candidate frequencies, with attenuation, reflection, noise and processing gains.
- [ ] **D1.4 Trade studies TS-1, TS-2, TS-3 + decision records** · [`2-trades/`](2-trades/) · owners: radar-hw, processing · due week 8
- [ ] **D1.5 Interface agreements** · [`3-budgets.md`](3-budgets.md) · owner: systems · due week 9
  Power, data per day, mass and volume, orbit and attitude knowledge, agreed with each subteam lead.
- [ ] **D1.6 Toolchain** · repo, Zotero group, notebooks running for everyone · owner: sim · due week 2
- [ ] **D1.7 Baseline review** · [`4-baseline-review.md`](4-baseline-review.md) · owner: systems · week 10

## Weekly plan

| Weeks | Focus | You should end with |
|---|---|---|
| 1–2 | Learn the system; set up tools | Everyone has read items 1–5 of the [reading list](../docs/reading-list.md) and run the budget notebook |
| 3–4 | Requirements; lunar environment | `1-requirements.md` drafted; `eps_*`, `tan_delta_*`, galactic noise sourced |
| 5–7 | Radar budget; frequency and antenna trades | TS-1 and TS-2 analyses; BUDGET.md reviewed by the team |
| 8–9 | Power and data with other subteams; presum trade | TS-3 done; `3-budgets.md` signed off |
| 10 | Baseline review | Review held; open-issues list with owners |

## Variables to pin down this quarter

Everything marked **Q1** in [`params/REGISTER.md`](../params/REGISTER.md#q1) (it also lists the TBDs by owner).
Settle these five first, because most other numbers depend on them:

1. `f_center`, `bandwidth` → TS-1
2. `antenna_type`, `antenna_length`, `antenna_efficiency` → TS-2
3. `tan_delta_basalt` → research (the biggest unknown for 500 m depth)
4. `tx_peak_power` → with the EPS team (`payload_power_peak`, `payload_power_orbit_avg`)
5. `presum_factor`, `requant_bits`, `obs_time_per_day` vs `downlink_rate` → TS-3 with the comms team

## Tools

```bash
python -m hs3gpr.budget                      # print the budget from the register
python -m hs3gpr.budget --set f_center=5e6   # what-if without editing the file
```
[`BUDGET.md`](BUDGET.md) is the same table, regenerated automatically on `main`.
✅ passes · ❌ fails · ⏳ needs an input that is still TBD.

## Watch-outs from day one

- **Frequency vs depth vs antenna.** The TS-1 notebook shows how strongly the reachable depth depends on
  the loss tangent. Going lower in frequency lengthens the antenna (half-wave ≈ 30 m at 5 MHz, 7.5 m at 20 MHz)
  and coarsens resolution.
- **Raw downlink from the Moon.** Path loss is ≈ 58 dB higher than for a 500 km LEO link with the same radio
  (BUDGET.md, *Data & downlink*). The comms team's rate × contact time caps all radar data.
- **Pivot rule.** If no frequency reaches `snr_required` at `roof_depth_max` with an antenna and power you can fly,
  decide at the review: shallower depth goal, bigger antenna, or different targets.

## Exit criteria (checked at the review)

- [ ] No Q1 variable is 🔴 TBD; the five above are 🔵 derived or 🟢 frozen
- [ ] BUDGET.md shows no ❌, or each ❌ has an agreed plan
- [ ] TS-1, TS-2, TS-3 finished, each with an accepted decision record
- [ ] Interface agreements signed in `3-budgets.md`
- [ ] Open-issues list with owners and due dates for Q2
