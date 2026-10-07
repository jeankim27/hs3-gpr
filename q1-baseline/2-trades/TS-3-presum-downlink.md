# TS-3 · Presumming vs downlink

- **Owner:** processing (with the comms team) · **Due:** week 8 · **Decision:** DR-003 (to write)
- **Register keys:** `presum_factor`, `requant_bits`, `obs_time_per_day`, `prf`, `downlink_rate`, `contact_time_per_day`, `mass_memory`

## Question
How much radar data can we take per day, and how hard can we presum without hurting SAR?

## What limits it
- **Downlink:** day's data ≤ `downlink_rate` × `contact_time_per_day` (BUDGET.md, *Data & downlink*)
- **SAR sampling:** spacing between presummed traces ≤ `along_track_resolution_req` (EQ-10)
- **Dynamic range:** fewer bits after presumming must still hold the surface and buried echoes

## Options
| Option | N | Bits | Observing time/day | Data/day | Spacing (EQ-10) |
|---|---|---|---|---|---|
| A | 8 | 8 | | | |
| B | 16 | 8 | | | |
| C | 32 | 6 | | | |

Fill with `python -m hs3gpr.budget --set presum_factor=32 --set requant_bits=6`.

## Recommendation
_2–3 sentences, then write DR-003 and update the register._
