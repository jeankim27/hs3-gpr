"""Physical constants (SI units). These are not design choices, so they live here, not in the register."""

C = 299_792_458.0            # speed of light, m/s
K_B = 1.380649e-23           # Boltzmann constant, J/K
T0 = 290.0                   # reference temperature, K
GM_MOON = 4.9028e12          # lunar gravitational parameter, m^3/s^2
R_MOON = 1_737_400.0         # mean lunar radius, m
EARTH_MOON_DISTANCE = 384_400e3   # mean distance, m
LEO_REFERENCE_RANGE = 500e3       # for comparing link losses with a LEO mission, m
