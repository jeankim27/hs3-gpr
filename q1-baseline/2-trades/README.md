# D1.4 · Trade studies

A trade study compares options against agreed criteria, then ends in a decision record.

| ID | Question | Owner | Notebook | Decision |
|---|---|---|---|---|
| [TS-1](TS-1-frequency-bandwidth.md) | Which center frequency and bandwidth? | radar-hw | [02_frequency_trade](../notebooks/02_frequency_trade.ipynb) | [DR-001](../../docs/decisions/DR-001-center-frequency.md) |
| [TS-2](TS-2-antenna.md) | Which antenna can we fly? | radar-hw | — | — |
| [TS-3](TS-3-presum-downlink.md) | How much data can we afford? | processing | budget notebook | — |

**How to run one**
1. Agree the criteria and weights **before** looking at results.
2. Put the analysis in a notebook that reads the register (use `p.with_values(...)` for options).
3. Fill the scoring table. Write the decision record. Update the register (`status: derived`, `source: TS-x`).
