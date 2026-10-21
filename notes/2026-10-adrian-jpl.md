# Meeting with Adrian (JPL GPR expert) · October 2026

Notes taken by Jean Kim. Adrian works on the Mars Skyfall helicopter GPR. Our team's follow-up comments are marked **Team note**.

## 1. Surface and subsurface knowledge comes first

- GPR is very application-specific, so other missions' models don't transfer to ours.
- We need regional context at our sites down to a few centimeters or meters.
- For Skyfall, they are moving MRO to collect DEM topography for this.
- We are better off than Mars: there is more lunar topography data.
- We also need the dielectric properties of our area of interest.
- Data: [NASA open data: Moon](https://data.nasa.gov/dataset/?tags=moon) · [LROC QuickMap](https://quickmap.lroc.im-ldi.com/)

**Team note:** At 20 MHz the wavelength is about 15 m in vacuum, so meter-scale roughness matters most. NAC DTMs at a few meters per post are the right resolution; finer scales come from statistical extrapolation.

## 2. Signal versus clutter

- Clutter, more than the signal itself, will be the issue. We must predict how clutter behaves to be sure we can see anything.
- Surface roughness is the biggest contributor.
- Clutter "blinds the subsurface linear to distance"; at some distance the noise completely blinds the data. (Unclear whether this means depth or horizontal distance.)

**Team note:** Echoes from depth d arrive at the same time as surface echoes from about √(2·h·d·√εr) off-nadir. At 50 km altitude and 100–500 m depth, that is 4–12 km off-nadir, where a dipole gives almost no rejection.

## 3. Reducing clutter

- Needs sophisticated ground processing with excellent knowledge of the antenna beam and surface geometry. Context-heavy; can take days on a supercomputer.
- Skyfall uses along-track migration: a hypothesis of the track plus coherent summation along it. This only cancels clutter along the track, not left and right.
- For our satellite, Adrian recommends cross-track processing and "baseline ___" (missed the word). Along-track migration alone is likely not enough for our mission.

**Team note:** We keep along-track SAR (orbital sounders like SHARAD need it) and add cross-track processing. "Baseline" probably means repeat-pass / multi-baseline processing, which has been demonstrated on SHARAD data.

## 4. Orbit must support the processing

- Our orbital trajectory must support our specific SAR processing technique.

**Team note:** In a polar low lunar orbit, adjacent tracks are about 31 km apart at the equator, and a site is passed roughly twice per month. Building up closely spaced tracks over one tube could take months.

## 5. Chirp and pulse compression

- Adrian: you cannot combine chirp and pulse compression.
- Omar: to compress a pulse, we need to emit a chirp.

**Team note:** Pulse compression is matched filtering of a chirp, and SHARAD uses exactly this. We keep chirp + ground pulse compression. Adrian may have meant impulse-type GPRs.

## 6. Avoid singularities

- We must not pick parameters where the computation produces essentially nothing.

**Team note:** Likely candidates: echoes landing on the next transmit pulse (PRF too high), or Doppler aliasing after presumming.

## 7. In-situ calibration

- Skyfall's helicopters repeat sampling, filtering and averaging for in-situ calibration.

**Team note:** Our equivalents: calibration loopback, the surface echo over flat mare, and repeat passes at orbit crossings.

## 8. Modeling order

1. **First-order:** basic SNR equation terms: antenna gain, geometric and wavelength spreading, bedrock reflection, roughness loss, surface transmission, dielectric attenuation. This gives a sense of frequency.
2. **Second-order:** Gaussian statistics, clutter management, surface roughness modeling.
3. **Third-order:** Hurst fits with topography data.

**Team note:** We add the noise floor, processing gains and a crude first-order SCR to first-order.

## Open questions for Adrian

1. "Linear to distance": depth (attenuation) or off-nadir distance (clutter geometry)?
2. "Cross-track processing and baseline ___": repeat-pass multi-baseline, or single-pass interferometry with two antennas?
3. "Singularity": Doppler/presum aliasing, transmit eclipsing, or something else?
4. Chirp comment: was that about impulse radars like Skyfall's?
5. What minimum DEM resolution would he accept at our frequency?
