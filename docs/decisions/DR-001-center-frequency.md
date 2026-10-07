# DR-001 · Center frequency and bandwidth

- **Status:** Proposed
- **Date:** YYYY-MM-DD
- **Owner:** radar-hw
- **Trade study:** [TS-1](../../q1-baseline/2-trades/TS-1-frequency-bandwidth.md)
- **Variables affected:** `f_center`, `bandwidth`, `antenna_length`, `chirp_length`

## Context
The radar must see a lava-tube roof at `roof_depth_max`. Lower frequencies penetrate deeper but need a
longer antenna and give coarser vertical resolution. The basalt loss tangent is uncertain, which moves
the answer a lot (see the TS-1 notebook).

## Options considered
| Option | Pros | Cons |
|---|---|---|
| ~5 MHz | Deepest penetration; Kaguya heritage | ~30 m dipole; coarse resolution |
| ~20 MHz | Balanced; SHARAD heritage | Depth depends strongly on tanδ |
| ~50 MHz | Short antenna; fine resolution | Shallow penetration in lossy basalt |

## Decision
_To be filled at the end of TS-1._

## Consequences
_To be filled._
