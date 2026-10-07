# D3.5 · Detectability map

**Question:** what is the smallest lava tube we detect, at each depth, given what we don't know
about the Moon and the spacecraft?

## Plan
1. Grid: roof depth 50–`roof_depth_max` m × tube height 10–200 m × each value in `tan_delta_sweep`.
2. For each grid point, run `monte_carlo_runs` simulations with random noise, orbit errors,
   clock phase noise and roughness drawn from their ranges.
3. Apply `detection_rule`. Record the detection probability and the false-alarm rate (runs with no tube).
4. Plot detection probability as a map per loss tangent; mark where it crosses 90%.

## Outputs
- Figure: detection probability vs depth and tube height (one panel per loss tangent)
- Table: smallest tube detected with ≥ 90% probability at 100, 300 and 500 m
- Sentence for the final report: "HS-3 detects tubes taller than __ m down to __ m when tanδ ≤ __."

## Run-time budget
Estimate seconds per run × runs before starting; reduce the grid or use Colab if needed.
