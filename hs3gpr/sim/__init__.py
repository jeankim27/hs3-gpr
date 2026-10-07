"""End-to-end simulation (Q2 builds it, Q3 makes it realistic).

One module per flowchart stage, so the code reads like the flowchart:

    scene.py     the Moon: surface, layers, voids, point targets           (steps 9–11)
    waveform.py  chirp generation and pulse compression                    (steps 5, 19)
    echo.py      raw echoes for each trace position                        (steps 8–11)   TODO Q2
    receiver.py  noise, gain, ADC quantization                             (steps 12–13)
    onboard.py   presumming and requantization                             (steps 14–15)
    ground.py    range compression, SAR focusing, multilook, depth        (steps 18–24)  SAR is TODO Q2
    metrics.py   SNR and detection measurements                            (step 25)

Data passed between modules (see q2-simulation/interfaces.md):
    traces : complex ndarray, shape (n_traces, n_samples), complex baseband
    meta   : dict with fs (Hz), t0 (s, window start per trace), x (m, along-track
             position per trace), h (m, altitude per trace)

Status: functions marked "TODO (Q2 …)" raise NotImplementedError until someone builds them.
The matching tests in tests/test_sim_verification.py skip until then and turn on automatically.
"""
