# Glossary

| Term | Meaning |
|---|---|
| GPR / radar sounder | Radar that looks into the ground. Flown from orbit, it is usually called a radar sounder. |
| Nadir | Straight down from the spacecraft. |
| Chirp | A pulse whose frequency sweeps from low to high. |
| PRF | Pulse repetition frequency: pulses per second. |
| Trace | The recorded echo from one pulse, as samples against time. |
| Receive window | The slice of time in which the receiver records. |
| SNR | Signal-to-noise ratio: how far an echo stands above the noise. |
| dB | Log scale for ratios. +3 dB ≈ ×2, +10 dB = ×10, +20 dB = ×100 in power. |
| Coherent | Phase-preserving. Echoes add in step; random noise does not. |
| Presumming | Adding N consecutive traces onboard to raise SNR and cut data volume. |
| Pulse compression | Matched filtering that turns a long chirp echo into a sharp spike. Also called range compression. |
| SAR | Synthetic aperture radar: combining echoes from many positions along the track as if from one long antenna. |
| Synthetic aperture | The stretch of track whose echoes are combined for one output point. |
| Clutter | Surface echoes from off to the side that arrive at the same time as buried echoes. |
| Radargram | The output image: along-track distance across, echo delay or depth down, brightness for echo strength. |
| Permittivity (εr) | Material property that slows radio waves and sets how strongly boundaries reflect. |
| Loss tangent (tanδ) | Material property that sets how fast a radio wave loses energy in it. |
| DEM | Digital elevation model: a height map of the surface. |
| Fresnel zone | The patch of ground that dominates a nadir echo from a smooth surface. |
| Register | `params/variables.yaml`, the one place design numbers live. |
| TS / DR | Trade study (how we compared options) / decision record (what we decided). |
| UWB | Ultra-wide band |
