# Q1 budget

Generated from [`params/variables.yaml`](../params/variables.yaml) by `python -m hs3gpr.budget --markdown q1-baseline/BUDGET.md`.
**Don't edit this file by hand** — change the register and it regenerates. Equations: [docs/equations.md](../docs/equations.md).

**Checks:** ✅ 6 pass · ❌ 0 fail · ⏳ 5 need an input that is still TBD

## Timing

| Quantity | Value | Unit | Equation | Check |
|---|---:|---|---|---|
| Wavelength λ | 15.0 | m | λ = c/f0 |  |
| Surface echo delay, lowest altitude | 200 | µs | EQ-01 |  |
| Surface echo delay, nominal altitude | 334 | µs | EQ-01 |  |
| Surface echo delay, highest altitude | 667 | µs | EQ-01 |  |
| Extra delay to the deepest roof (basalt) | 8.83 | µs | EQ-01 |  |
| Window length needed (margin + deepest roof) | 13.8 | µs | EQ-01 | ✅ limit 40.0 µs |
| Time available for the chirp at lowest altitude | 190 | µs | EQ-14 | ✅ chirp is 50.0 µs |
| Duty cycle | 5.00 | % | EQ-14 |  |
| Receive window vs transmit pulses | clear at all altitudes |  | EQ-14 | ✅ |

## Resolution & footprint

| Quantity | Value | Unit | Equation | Check |
|---|---:|---|---|---|
| Vertical resolution, free space | 15.0 | m | EQ-03 |  |
| Vertical resolution, regolith | 9.12 | m | EQ-03 |  |
| Vertical resolution, basalt | 5.67 | m | EQ-03 | ⏳ to check, set vertical_resolution_req |
| Fresnel zone diameter (nominal altitude) | 1,224 | m | EQ-09 |  |
| Pulse-limited footprint (nominal altitude) | 2,449 | m | EQ-09 |  |
| Synthetic aperture length for δx_req | 1,499 | m | EQ-09 |  |
| Orbital period (nominal altitude) | 113 | min | EQ-13 |  |
| Ground speed (nominal altitude) | 1,610 | m/s | EQ-13 |  |
| Spacing between presummed traces | 25.8 | m | EQ-10 | ✅ limit 250 m |
| Traces combined by SAR, M | 58 | - | EQ-09 |  |
| SAR aperture time | 0.93 | s | EQ-09 | the clock must stay coherent this long; see clock_stability |

## Propagation

| Quantity | Value | Unit | Equation | Check |
|---|---:|---|---|---|
| Wave speed in regolith | 0.61 | × c | c/√εr |  |
| Wave speed in basalt | 0.38 | × c | c/√εr |  |
| Attenuation in regolith (one way) | 0.015 | dB/m | EQ-04 |  |
| Attenuation in basalt (one way) | 0.0482 | dB/m | EQ-04 |  |
| Two-way attenuation to the deepest roof | 47.8 | dB | EQ-04 |  |
| Surface reflection (vacuum → regolith) | -12.3 | dB | EQ-05 |  |
| Layer reflection (regolith → basalt) | -12.6 | dB | EQ-05 |  |
| Roof reflection (basalt → void) | -6.91 | dB | EQ-05 |  |

## Noise & SNR

| Quantity | Value | Unit | Equation | Check |
|---|---:|---|---|---|
| Galactic noise temperature at f0 | 46,777 | K | EQ-07 |  |
| System noise temperature | 33,119 | K | EQ-07 |  |
| Surface echo SNR, one pulse (compressed) | 40.8 | dB | EQ-06, EQ-08 |  |
| Deepest roof SNR, one pulse (compressed) | -2.67 | dB | EQ-06, EQ-08 |  |
| Gain: pulse compression T·B | 27.0 | dB | EQ-08 | already included in the one-pulse rows |
| Gain: presumming N | 12.0 | dB | EQ-08 |  |
| Gain: SAR M | 17.6 | dB | EQ-08 |  |
| Other losses | -3 | dB |  |  |
| Deepest roof SNR after processing | 24.0 | dB | EQ-08 | ✅ margin 14.0 dB |
| Deepest roof that meets SNR_req | 645 | m | EQ-08 | ✅ margin 145 m |
| Surface-to-roof echo ratio (one pulse) | 43.5 | dB |  | surface-echo sidelobes and ADC dynamic range must cope with this |

## Data & downlink

| Quantity | Value | Unit | Equation | Check |
|---|---:|---|---|---|
| Samples per trace | 2,000 | - |  |  |
| Raw data rate (no presum) | 24.0 | Mbit/s | EQ-11 |  |
| Data rate after presum + requantization | 1.00 | Mbit/s | EQ-11 |  |
| Radar data per day | 225 | MB | EQ-11 |  |
| Downlink rate needed to clear a day's data | 125 | kbit/s | EQ-11 | ⏳ to check, set downlink_rate |
| Memory needed for one day of data | 225 | MB |  | ⏳ to check, set mass_memory |
| Path loss Moon → Earth at f_dl | 223 | dB | EQ-12 |  |
| Extra path loss vs a 500 km LEO link | 57.7 | dB | EQ-12 |  |

## Power

| Quantity | Value | Unit | Equation | Check |
|---|---:|---|---|---|
| Peak DC power during a pulse | 30.0 | W | EQ-15 | ⏳ to check, set payload_power_peak |
| Average power while observing | 6.25 | W | EQ-15 |  |
| Radar power averaged over a day | 0.13 | W | EQ-15 | ⏳ to check, set payload_power_orbit_avg |
| Energy per day | 3.12 | Wh | EQ-15 |  |
| Energy drawn per pulse | 1.25 | mJ | EQ-15 | sizes the capacitor bank |

