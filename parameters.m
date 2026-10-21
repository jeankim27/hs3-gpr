function p = parameters()
%PARAMETERS  Shared input numbers for the HS-3 GPR models.
%
%   p = parameters();   returns a struct of every shared number, in SI units.
%
%   RULES
%     - This is the only place a shared number is typed. Read it with
%       p = parameters(); and never retype a value in your own script.
%     - Every value has a comment: [area #] status, source.
%         status: assumed = placeholder or estimate, still needs a source
%                 sourced = taken from a cited source
%                 decided = agreed by the team; change only at a review
%     - NaN means "not known yet".
%     - Changed a value? Say so at the weekly sync.
%
%   Area numbers refer to ownership.md. Starting values were carried over
%   from the old variable register (commit 182ab91).

%% Physical constants
p.c   = 299792458;          % speed of light [m/s]
p.k_B = 1.380649e-23;       % Boltzmann constant [J/K]
p.T0  = 290;                % reference noise temperature [K]

%% Target  [areas 2, 11]
p.roof_depth_max  = 500;    % deepest tube roof to detect [m]         [11] assumed, mission assumption
p.tube_height_min = NaN;    % smallest tube height to detect [m]      [2]  range 20-200 m, literature
p.tube_width_min  = NaN;    % smallest tube width to detect [m]       [2]  range 50-1000 m, literature
p.snr_required    = 10;     % SNR after processing for detection [dB] [11] assumed, range 6-15 dB
p.target_regions  = {'Oceanus Procellarum', 'Mare Imbrium'};  % [2]  decided, team focus (HS-3 mission statement)
p.target_sites    = {'Marius Hills Hole'};  % [2]  assumed, haruyama2009; kaku2017 (Procellarum). Add candidates in both regions (D1.3)

%% Lunar materials  [area 1]
p.eps_regolith       = 2.7;    % rel. permittivity, regolith [-]      assumed, olhoeft1975 (rho ~1.5 g/cm3), range 2.3-3.5
p.eps_basalt         = 7.0;    % rel. permittivity, mare basalt [-]   assumed, olhoeft1975 (rho ~3.0 g/cm3), range 5.5-9.0
p.tan_delta_regolith = 0.005;  % loss tangent, regolith [-]           assumed, heiken1991 (research needed), range 0.001-0.03
p.tan_delta_basalt   = 0.01;   % loss tangent, mare basalt [-]        assumed, heiken1991; ono2009 (research needed), range 0.003-0.06
p.regolith_thickness = 5;      % regolith thickness, mare [m]         assumed, heiken1991 (verify), range 2-15

%% Surface and clutter  [area 3]
p.surface_rms_height = NaN;    % RMS height at wavelength scale [m]   to come from DEMs / literature
p.surface_rms_slope  = NaN;    % RMS slope at wavelength scale [deg]  range 1-10 deg, LOLA

%% Orbit  [area 10]
p.altitude_nominal = 50e3;     % nominal altitude [m]                 assumed, mission assumption
p.altitude_min     = 30e3;     % lowest altitude considered [m]       assumed
p.altitude_max     = 100e3;    % highest altitude considered [m]      assumed
p.inclination      = NaN;      % orbit inclination [deg]              from GNC/ADCS subteam

%% Waveform and timing  [areas 5, 7]
p.f_center      = 20e6;        % center frequency [Hz]                [5] assumed, open trade (Q1-Q2)
p.bandwidth     = 10e6;        % chirp bandwidth [Hz]                 [5] assumed, open trade
p.chirp_length  = 50e-6;       % chirp duration [s]                   [5] assumed
p.prf           = 1000;        % pulse repetition frequency [Hz]      [7] assumed
p.window_length = 40e-6;       % receive window length [s]            [7] assumed

%% Antenna  [area 4]
p.antenna_type       = 'half-wave dipole, deployable';  %             assumed, open trade
p.antenna_length     = 7.5;    % antenna length [m]                   assumed, c/(2*f_center) at 20 MHz
p.antenna_gain       = 2.15;   % antenna gain [dBi]                   assumed, half-wave dipole textbook value
p.antenna_efficiency = 0.7;    % radiation efficiency [-]             assumed, team estimate

%% Transmitter  [area 5]
p.tx_peak_power = 10;          % transmit peak power [W]              assumed, SHARAD uses 10 W (seu2007)
p.pa_efficiency = 0.4;         % power amplifier efficiency [-]       assumed

%% Receiver  [area 6]
p.receiver_noise_figure = 3;   % receiver noise figure [dB]           assumed
p.adc_bits              = 12;  % ADC resolution [bit]                 assumed
p.adc_sample_rate       = 50e6;% ADC sample rate [Hz]                 assumed
% Galactic noise (ITU-R P.372): Fa = 52 - 23*log10(f / 1 MHz) dB above k*T0*B.  assumed, verify

%% Power, onboard data, downlink  [area 8]
p.radar_idle_power     = 5;    % radar power when not transmitting [W] assumed
p.presum_factor        = 16;   % onboard coherent presums [-]          assumed, open trade
p.requant_bits         = 8;    % bits per sample after presum [bit]    assumed
p.obs_time_per_day     = 1800; % radar on-time per day [s]             assumed
p.contact_time_per_day = 14400;% ground contact per day [s]            assumed, Comms placeholder
p.downlink_rate        = NaN;  % downlink rate [bit/s]                 from Comms subteam
p.payload_power_avg    = NaN;  % orbit-average power allocation [W]    from EPS subteam
p.payload_power_peak   = NaN;  % peak power allocation [W]             from EPS subteam

%% Processing  [area 9]
p.system_losses   = 3;         % lumped system losses [dB]            assumed, team estimate
p.multilook_count = 4;         % incoherent looks [-]                 assumed
p.along_track_resolution = 250;% along-track resolution [m]           assumed, from tube_width_min

end
