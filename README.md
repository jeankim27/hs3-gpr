# HS-3 GPR

Ground-penetrating radar (radar sounder) for **HuskySat-3**, a UW Husky Satellite Lab lunar CubeSat that will map lava tubes beneath the Moon's surface.

Project lead: Jean Kim ([@jeankim27](https://github.com/jeankim27))

## Goal for this year

By week 30, show with first- and second-order models that HS-3 can detect a lava tube at a chosen site through surface clutter. Then freeze the frequency, observation strategy and hardware requirements so we can start building next year.

By the end of the year we will have:

1. **Design decisions:** target site, frequency and bandwidth, orbit and observation strategy.
2. **Detectability result:** whether the tube is visible through clutter after processing, at that site.
3. **Build readiness:** frozen hardware requirements, benchtop demos, and a build plan for next year.

## Quarters

| Quarter | Question | Modeling | Ends with |
|---|---|---|---|
| [**Q1** · weeks 1–10](q1-first-order-baseline/) | Which frequencies could work at all? | First-order, generic lunar surface | Frequency band narrowed to 1–2 candidates |
| [**Q2** · weeks 11–20](q2-sites-and-decision/) | Which frequency, at which site, with which orbit? | First-order at real sites, plus signal-to-clutter ratio (SCR) | **Frequency and target decision** (week 20) |
| [**Q3** · weeks 21–30](q3-second-order-and-hardware/) | Can we see the tube through the clutter, and what do we build? | Second-order, plus hardware development | Hardware requirements frozen |

## Who owns what

[**ownership.md**](ownership.md) lists the 12 ownership areas, what each one covers, and who owns it.

## Where things go

| File or folder | What's in it |
|---|---|
| [`parameters.m`](parameters.m) | Shared input numbers for everyone's MATLAB models. The only place a shared number is typed. |
| [`q1-first-order-baseline/`](q1-first-order-baseline/), [`q2-sites-and-decision/`](q2-sites-and-decision/), [`q3-second-order-and-hardware/`](q3-second-order-and-hardware/) | Each quarter's goal, deliverables, and the work itself |
| [`ownership.md`](ownership.md) | Ownership areas and owners |
| [`notes/`](notes/) | Meeting notes, starting with [Adrian's advice (JPL)](notes/2026-10-adrian-jpl.md) |

## Three rules

1. **Name files by deliverable.** Put work in the current quarter's folder, starting with its deliverable ID: `D1.2_dielectric_model.m`, `D1.2_attenuation_vs_depth.png`.
2. **Shared numbers live in `parameters.m`.** Load them with `p = parameters();`, and don't retype them in your own script. If you change one, say so at the weekly sync.
3. **Cite a source for every number,** as a comment next to it.

## Using `parameters.m`

From any quarter folder in MATLAB:

```matlab
addpath('..');        % make parameters.m visible
p = parameters();     % load the shared numbers
lambda = p.c / p.f_center;
```

The earlier Python design model is kept in history: [browse the old version](https://github.com/jeankim27/hs3-gpr/tree/182ab915dc7354da9153c5e57de83ab7cf84bf5a).
