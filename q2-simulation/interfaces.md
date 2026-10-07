# D2.1 · Simulation interfaces

The contract between modules. If you change a signature, update this page in the same pull request.

## Conventions
- **Units:** SI everywhere (Hz, m, s, W). Convert only for display.
- **Signals:** complex baseband at `p["sim_sample_rate"]`.
- **Traces:** `ndarray`, complex, shape `(n_traces, n_samples)`.
- **Metadata:** `dict(fs=float, t0=ndarray[n_traces], x=ndarray[n_traces], h=ndarray[n_traces])`
  - `t0` time of the first sample after each pulse (window start), s
  - `x` along-track position, m · `h` altitude, m
- **Parameters:** every function that needs a design value takes `p` (the loaded register).

## Pipeline

| Step | Module · function | Input | Output | Status |
|---|---|---|---|---|
| 9–11 | `scene.flat_scene(p, …)` | register | `Scene` | ✅ works |
| 9–11 | `scene.point_target_scene(x, depth)` | position | `Scene` | ✅ works |
| 5 | `waveform.chirp(T, B, fs)` | timing | reference chirp | ✅ works |
| 8–11 | `echo.simulate_traces(scene, p, x, h, rng, noise)` | scene, positions | `traces, meta` | ⏳ D2.3 |
| 12–13 | `receiver.add_noise`, `receiver.adc` | traces | traces | ✅ works |
| 12–13 | `receiver.receiver_chain(traces, p, rng)` | traces | traces | ⏳ D2.3 |
| 14 | `onboard.presum(traces, N)` | traces | traces ÷ N | ✅ works |
| 15 | `onboard.requantize(traces, bits)` | traces | traces | ✅ works |
| 19 | `ground.range_compress(traces, p, fs)` | traces | compressed | ✅ works |
| 21 | `ground.sar_focus(compressed, meta, p, x_out)` | compressed | focused image | ⏳ D2.5 |
| 22 | `ground.multilook(image, L)` | image | power image | ✅ works |
| 24 | `ground.time_to_depth(dt, eps)` | delays | depths | ✅ works |
| 25 | `metrics.snr_db`, `metrics.resolution_3db` | traces | numbers | ✅ works |
| 25 | `metrics.detect(image, meta, p)` | image | detections | ⏳ Q2 |

## Decisions to record here
- How the ADC full scale is set (surface echo + headroom?)
- How presummed positions are defined (`onboard.presum_positions`)
- How the void is represented (register: `void_model`)
