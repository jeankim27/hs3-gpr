# Equations

Every calculation in the project cites one of these IDs. Each entry lists the register keys it uses
([`params/variables.yaml`](../params/variables.yaml)), its assumptions, a source, and the function that implements it
in [`hs3gpr/budget.py`](../hs3gpr/budget.py).

**Adding an equation:** use the next free ID, fill in the same five parts, implement it as a function
whose docstring starts with the ID, and add a check to `tests/test_budget.py`.

| ID | Quantity | Function |
|---|---|---|
| [EQ-01](#eq-01) | Echo delay | `two_way_delay`, `extra_delay` |
| [EQ-02](#eq-02) | Depth from delay | `depth_from_delay` |
| [EQ-03](#eq-03) | Vertical resolution | `vertical_resolution` |
| [EQ-04](#eq-04) | Attenuation | `attenuation_db_per_m` |
| [EQ-05](#eq-05) | Reflection at a boundary | `reflection_coefficient` |
| [EQ-06](#eq-06) | Specular radar equation | `specular_echo_power` |
| [EQ-07](#eq-07) | Noise | `galactic_noise_temperature`, `system_noise_temperature` |
| [EQ-08](#eq-08) | Processing gain and SNR | `compressed_snr`, `final_snr_db` |
| [EQ-09](#eq-09) | Footprints and SAR resolution | `fresnel_zone_diameter`, `pulse_limited_diameter`, `synthetic_aperture_length` |
| [EQ-10](#eq-10) | Presum limit | `presummed_spacing` |
| [EQ-11](#eq-11) | Data rate | `data_rate` |
| [EQ-12](#eq-12) | Free-space path loss | `fspl_db` |
| [EQ-13](#eq-13) | Orbit speed and period | `orbital_speed`, `ground_speed`, `orbital_period` |
| [EQ-14](#eq-14) | Timing and duty cycle | `window_clear_of_transmit`, `duty_cycle` |
| [EQ-15](#eq-15) | Radar power | in `compute` (Power rows) |

---

<a id="eq-01"></a>
## EQ-01 · Echo delay

$$t_{surface} = \frac{2h}{c} \qquad \Delta t_{depth} = \frac{2 d \sqrt{\varepsilon_r}}{c}$$

- **Uses:** `altitude_min`, `altitude_nominal`, `altitude_max`, `roof_depth_max`, `eps_basalt`
- **Assumes:** nadir path, flat surface, layers of constant permittivity
- **Source:** any radar textbook; see `porcello1974` for the lunar sounder case
- **Code:** `two_way_delay`, `extra_delay`

<a id="eq-02"></a>
## EQ-02 · Depth from delay

$$d = \frac{c\,\Delta t}{2\sqrt{\varepsilon_r}}$$

- **Uses:** `eps_regolith`, `eps_basalt`
- **Assumes:** the permittivity of the material above the reflector is known; this is the main depth uncertainty
- **Source:** `olhoeft1975` for lunar permittivity
- **Code:** `depth_from_delay`

<a id="eq-03"></a>
## EQ-03 · Vertical resolution

$$\delta z = \frac{c}{2B\sqrt{\varepsilon_r}}$$

- **Uses:** `bandwidth`, `eps_regolith`, `eps_basalt`
- **Assumes:** ideal pulse compression; a window function widens it slightly
- **Source:** `cumming2005`
- **Code:** `vertical_resolution`

<a id="eq-04"></a>
## EQ-04 · Attenuation

$$\alpha\,[\text{dB/m}] \approx 8.686\,\frac{\pi\sqrt{\varepsilon_r}\,\tan\delta}{\lambda_0} \qquad L_{two\text{-}way} = 2\,\alpha\,d$$

- **Uses:** `f_center`, `eps_*`, `tan_delta_*`, `regolith_thickness`
- **Assumes:** low-loss material (tanδ ≪ 1), uniform layers
- **Source:** `heiken1991` (lunar loss tangents); low-loss approximation from electromagnetics texts
- **Code:** `attenuation_db_per_m`

<a id="eq-05"></a>
## EQ-05 · Reflection at a boundary

$$\Gamma = \frac{\sqrt{\varepsilon_1} - \sqrt{\varepsilon_2}}{\sqrt{\varepsilon_1} + \sqrt{\varepsilon_2}} \qquad \text{power: } \Gamma^2, \quad \text{transmitted: } 1 - \Gamma^2$$

- **Uses:** `eps_regolith`, `eps_basalt` (void: ε = 1)
- **Assumes:** normal incidence, smooth boundary
- **Code:** `reflection_coefficient`

<a id="eq-06"></a>
## EQ-06 · Specular radar equation

$$P_r = \frac{P_t\,G^2\,\lambda^2\,\Gamma^2\,T_s}{(4\pi)^2\,(2R)^2}\,10^{-L/10} \qquad R = h + \frac{d_{reg}}{\sqrt{\varepsilon_{reg}}} + \frac{d_{bas}}{\sqrt{\varepsilon_{bas}}}$$

$T_s$ is the two-way transmission through the boundaries above the reflector; $G$ includes antenna efficiency.

- **Uses:** `tx_peak_power`, `antenna_gain`, `antenna_efficiency`, `f_center`, `altitude_nominal`, permittivities, loss tangents
- **Assumes:** flat (mirror-like) reflectors; rough surfaces return less and spread it in angle
- **Source:** `porcello1974`, `ono2010`
- **Code:** `specular_echo_power`, `single_pulse_snr_db`

<a id="eq-07"></a>
## EQ-07 · Noise

$$P_n = k\,T_{sys}\,B \qquad T_{sys} = \eta\,T_{gal} + (1-\eta)\,T_{phys} + T_0\left(10^{NF/10} - 1\right)$$

$$T_{gal} = T_0 \cdot 10^{F_a/10}, \qquad F_a = 52 - 23\log_{10}(f/\text{1 MHz})\ \text{dB}$$

- **Uses:** `f_center`, `antenna_efficiency`, `receiver_noise_figure`, `galactic_noise_model`
- **Assumes:** galactic noise dominates at HF; spacecraft self-noise is below it (`bus_emi_limit`)
- **Source:** `itur_p372`
- **Code:** `galactic_noise_temperature`, `system_noise_temperature`

<a id="eq-08"></a>
## EQ-08 · Processing gain and SNR

$$\text{SNR}_1 = \frac{P_r\,T}{k\,T_{sys}} \;\; (\text{one pulse, includes } T\!\cdot\!B) \qquad \text{SNR}_{final} = \text{SNR}_1 \cdot N \cdot M \,/\, L_{sys}$$

- **Uses:** `chirp_length`, `bandwidth`, `presum_factor`, `system_losses`, M from EQ-09/EQ-10
- **Assumes:** coherent integration over N·M pulses; real gains are lower (phase errors, windows)
- **Source:** `cumming2005`
- **Code:** `compressed_snr`, `processing_gains_db`, `final_snr_db`

<a id="eq-09"></a>
## EQ-09 · Footprints and SAR resolution

$$D_{Fresnel} = \sqrt{2\lambda h} \qquad D_{pulse} = 2\sqrt{\frac{h\,c}{B}} \qquad L_{SA} = \frac{\lambda h}{2\,\delta x} \qquad M = \frac{L_{SA}}{\text{presummed spacing}}$$

- **Uses:** `f_center`, `altitude_nominal`, `bandwidth`, `along_track_resolution_req`
- **Source:** `cumming2005`, `kobayashi2012`
- **Code:** `fresnel_zone_diameter`, `pulse_limited_diameter`, `synthetic_aperture_length`

<a id="eq-10"></a>
## EQ-10 · Presum limit

$$\frac{N\,v_g}{\text{PRF}} \;\le\; \frac{\lambda}{4\sin\theta_{max}} \;=\; \delta x$$

Presummed traces must be close enough together for SAR to reach the along-track resolution you want.

- **Uses:** `presum_factor`, `prf`, `along_track_resolution_req`; $v_g$ from EQ-13
- **Code:** `presummed_spacing`

<a id="eq-11"></a>
## EQ-11 · Data rate

$$R = \frac{\text{PRF} \cdot (t_{win} \cdot f_s) \cdot n_{bits}}{N}$$

- **Uses:** `prf`, `window_length`, `adc_sample_rate`, `adc_bits` or `requant_bits`, `presum_factor`
- **Code:** `data_rate`

<a id="eq-12"></a>
## EQ-12 · Free-space path loss

$$L_{fs} = 20\log_{10}\!\left(\frac{4\pi R}{\lambda}\right)$$

- **Uses:** `downlink_frequency`; R = Earth–Moon distance
- **Note:** at lunar distance the loss is ≈ 58 dB higher than at 500 km (LEO)
- **Code:** `fspl_db`

<a id="eq-13"></a>
## EQ-13 · Orbit speed and period

$$v = \sqrt{\frac{GM}{R_m + h}} \qquad v_g = v\,\frac{R_m}{R_m + h} \qquad P = 2\pi\sqrt{\frac{(R_m+h)^3}{GM}}$$

- **Assumes:** circular orbit, spherical Moon
- **Code:** `orbital_speed`, `ground_speed`, `orbital_period`

<a id="eq-14"></a>
## EQ-14 · Timing and duty cycle

The receive window $[t_{surface} - t_{pre},\; t_{surface} - t_{pre} + t_{win}]$ must not overlap any transmit
interval $[k/\text{PRF},\; k/\text{PRF} + T + t_{rec}]$. The chirp must end before the surface echo returns at the
lowest altitude. Duty cycle $= T \cdot \text{PRF}$.

- **Uses:** `prf`, `chirp_length`, `window_length`, `window_margin`, `tr_recovery_time`, altitudes
- **Code:** `window_clear_of_transmit`, `duty_cycle`

<a id="eq-15"></a>
## EQ-15 · Radar power

$$P_{peak,DC} = P_{idle} + \frac{P_t}{\eta_{PA}} \qquad P_{obs} = P_{idle} + \frac{P_t\,T\,\text{PRF}}{\eta_{PA}} \qquad E_{pulse} = \frac{P_t\,T}{\eta_{PA}}$$

- **Uses:** `radar_idle_power`, `tx_peak_power`, `pa_efficiency`, `chirp_length`, `prf`, `obs_time_per_day`
- **Code:** Power rows in `compute`
