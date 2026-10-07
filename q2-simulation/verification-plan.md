# D2.6 · Verification plan

Each check compares the simulation with something we already trust (an equation or the Q1 budget).
The tests live in [`tests/test_sim_verification.py`](../tests/test_sim_verification.py).

| ID | What it proves | Pass when | Test | Status |
|---|---|---|---|---|
| V-01 | Pulse compression gives the T·B gain | within 0.3 dB of 10·log10(T·B) | `test_V01_…` | ✅ passing |
| V-02 | Presumming gives the N gain | within 0.3 dB of 10·log10(N) | `test_V02_…` | ✅ passing |
| V-03 | SAR reaches the along-track resolution | −3 dB width within 35% of `along_track_resolution_req` | `test_V03_…` | ⏳ needs D2.3, D2.5 |
| V-04 | Depth conversion is consistent | a reflector placed at d comes back at d ± δz | *(write it)* | ⏳ |
| V-05 | End-to-end SNR matches the budget | within `snr_tolerance` of BUDGET.md at 300 m | `test_V05_…` | ⏳ needs D2.3, D2.5 |
| V-06 | Data volume matches the budget | within 5% of EQ-11 | `test_V06_…` | ✅ passing |

## If a test fails
1. Check units first (µs vs s, MHz vs Hz).
2. Plot the intermediate signals in a notebook.
3. If the **budget** is wrong, fix the equation, the docs and its test together.
4. If you change a pass criterion, write why here.
