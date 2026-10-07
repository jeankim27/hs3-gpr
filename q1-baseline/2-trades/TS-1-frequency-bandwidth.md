# TS-1 · Center frequency and bandwidth

- **Owner:** radar-hw · **Due:** week 8 · **Decision:** [DR-001](../../docs/decisions/DR-001-center-frequency.md)
- **Analysis:** [`notebooks/02_frequency_trade.ipynb`](../notebooks/02_frequency_trade.ipynb)
- **Register keys:** `f_center`, `bandwidth`, `antenna_length`, `chirp_length`

## Question
Which center frequency lets us see a roof at `roof_depth_max` with an antenna we can fly, at the
resolution the requirements need?

## Options
| Option | f0 | B | Half-wave dipole | Heritage |
|---|---|---|---|---|
| A | 5 MHz | 2 MHz | 30 m | Kaguya LRS (4–6 MHz) |
| B | 10 MHz | 4 MHz | 15 m | |
| C | 20 MHz | 8–10 MHz | 7.5 m | SHARAD (15–25 MHz) |
| D | 40 MHz | 16 MHz | 3.75 m | |

## Criteria (agree weights before scoring)
| Criterion | Weight | How measured |
|---|---|---|
| Depth margin at the expected loss tangent | 30% | `max_detectable_depth` − `roof_depth_max` |
| Antenna feasibility on a 6U/12U | 25% | length, stowage, deployment risk (TS-2) |
| Vertical resolution vs requirement | 20% | EQ-03 in basalt vs `vertical_resolution_req` |
| Robustness to loss-tangent uncertainty | 15% | depth at the high end of `tan_delta_sweep` |
| Data rate and sampling | 10% | EQ-11, ADC rate needed |

## Results (fill from the notebook)
| Option | Depth @ tanδ low / mid / high | δz basalt | Antenna | Score |
|---|---|---|---|---|
| A | | | | |
| B | | | | |
| C | | | | |
| D | | | | |

## Recommendation
_Write 2–3 sentences, then fill DR-001._

## Open questions
- Best available loss-tangent values for the target sites (scene team)
- Longest antenna the structures team can stow and deploy
