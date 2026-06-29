# Paper Equations Reference

## System Dynamics

| # | Equation | Description | Location |
|----|----------|-------------|----------|
| 1 | M·z̈ = f_h + f_c | Equation of motion | Eq. (1) |
| 2 | f_h = f_b + f_r + f_e | Hydrodynamic forces | Eq. (2) |
| 3 | f_b = -ρ·D'(0)·g·z | Buoyancy force | Eq. (3-4) |
| 5 | f_r = -m_h·ż - f_r0(t) | Radiation force | Eq. (5) |
| 6 | f_r0(t) = ∫₀ᵗ h_rs(t-τ)·ż(τ)dτ | Memory effect (convolution) | Eq. (6) |
| 7 | ẋ_r = A_r·x_r + B_r·ż | Radiation state-space | Eq. (7) |
|    | f_r ≈ C_r·x_r | Radiation output | Fig. 2 |
| 8 | F_e(ω) = H_e(ω)·A(ω) | Excitation (freq domain) | Eq. (8) |
| 9 | f_e(t) = ∫ h_e(t-τ)·η(τ)dτ | Excitation (time domain) | Eq. (9) |
| 10 | h_e(t) = (1/2π)·∫ H_e(ω)·e^(iωt)dω | Impulse response | Eq. (10) |
| 11 | H_e,T(ω) = H_e(ω)·e^(jωT(ω)) | Frequency-dependent delay | Eq. (11) |
| 12 | ẋ_e = A_e·x_e + B_e·η_up(t) | Excitation state-space | Eq. (12) |
|    | f_e(t) ≈ C_e·x_e | Excitation output | Eq. (12) |
| 13 | S_η(ω) = (αg²/ω⁵)·exp(-5/4(ω_p/ω)⁴)·γ^r | JONSWAP spectrum | Eq. (13) |
| 14 | v_a = R_a·i + L_a·di/dt + K_v·ż | Generator voltage | Eq. (14) |
|    | f_c = K_i·i | Control force | Eq. (14) |
| 15 | P_c = ζ·P_m | Electrical power | Eq. (15) |
| 16 | P_s = f_e·ż | Wave power input | Eq. (16) |
| 17 | P_d = R_a·i² | Dissipation loss | Eq. (17) |
| 18 | ż = -α·f_c | MIPC ideal condition | Eq. (18) |
| 19 | P_s = -α·f_c² | Resulting power | Eq. (19) |
| 20 | v_opt = (1/2K)·f_e | Optimal velocity | Eq. (20) |
| 21 | α = 1/(2K) | MIPC gain | Eq. (21) |
| 22 | z_p = ż - α·f_c | Performance output (H2) | Eq. (22) |
| 23 | ẋ_o = A·x_o + B·i + E·f_e | Augmented system | Eq. (23) |
| 24 | x_o = [x_r1 x_r2 x_r3 x_r4 z ż]ᵀ | Augmented state vector | Eq. (24) |

## Implementation Map

```
Python Class/Function → Paper Equation
─────────────────────────────────────
RadiationForce.state_derivative() → Eq. (7)
RadiationForce.output() → Eq. (7) output
ExcitationForce.state_derivative() → Eq. (12)
ExcitationForce.output() → Eq. (12) output
JonswapSpectrum.spectrum() → Eq. (13)
JonswapSpectrum.generate_time_series() → Eq. (13) + inverse FFT
WECSystem.compute_forces() → Eq. (1-3)
WECSystem.state_derivatives() → Eq. (1, 7, 12)
H2Controller.design() → Eq. (22-24) + LMI
Simulator.run() → Numerical integration of all
```