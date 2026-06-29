# System Parameters Reference

## Mechanical Parameters

| Parameter | Symbol | Unit | Source | Status |
|-----------|--------|------|--------|--------|
| Total Mass | M | kg | Paper specs | ❌ To fill |
| Buoyancy Stiffness | k_b | N/m | k_b = ρ·D'(0)·g | ❌ To fill |
| Displaced Volume | D | m³ | Geometry | ❌ To fill |

## Radiation Force (State-Space, Order 4)

| Parameter | Dimension | Source | Status |
|-----------|-----------|--------|--------|
| A_r | 4×4 | NEMOH → FDI → state-space | ❌ To fill |
| B_r | 4×1 | From hydrodynamic analysis | ❌ To fill |
| C_r | 1×4 | Derived from frequency response | ❌ To fill |

**Reference:** Figure 2 of paper shows magnitude/phase fit.

## Excitation Force (State-Space)

| Parameter | Dimension | Source | Status |
|-----------|-----------|--------|--------|
| A_e | n_e×n_e | Wave spectrum analysis | ❌ To fill |
| B_e | n_e×1 | JONSWAP spectrum coupling | ❌ To fill |
| C_e | 1×n_e | Frequency response | ❌ To fill |
| n_e | — | Usually 2-6 (order TBD) | ❌ To determine |

## Wave Spectrum (JONSWAP)

| Parameter | Symbol | Unit | Typical Range | Status |
|-----------|--------|------|----------------|--------|
| Significant Wave Height | H_s | m | 1-10 | ❌ To fill |
| Peak Period | T_p | s | 5-15 | ❌ To fill |
| Peakedness Factor | γ | — | 1-7 (default 3.3) | ❌ To fill |

## Generator / Actuator

| Parameter | Symbol | Unit | Source | Status |
|-----------|--------|------|--------|--------|
| Armature Resistance | R_a | Ω | Machine specs | ❌ To fill |
| Armature Inductance | L_a | H | Machine specs | ❌ To fill |
| Force Constant | K_i | N/A | From Eq. (14) | ❌ To fill |
| Back-EMF Constant | K_v | V·s/m | Machine specs | ❌ To fill |

## Control Parameters

| Parameter | Symbol | Unit | Formula | Status |
|-----------|--------|------|---------|--------|
| MIPC Gain | K | — | From paper | ❌ To fill |
| Optimal Factor | α | — | 1/(2K) | ❌ Computed |

## Simulation Parameters

| Parameter | Value | Unit | Notes |
|-----------|-------|------|-------|
| Start Time | t_start | s | Usually 0 |
| End Time | t_end | s | 600-1000 (10+ periods) |
| Time Step | dt | s | 0.01 (typical) |
| ODE Solver | RK45 | — | Or RK23, DOP853, etc. |
| Relative Tolerance | rtol | — | 1e-8 typical |
| Absolute Tolerance | atol | — | 1e-10 typical |

## How to Fill Parameters

1. **From Paper Screenshots**
   - Mass M, buoyancy k_b → Text or table in paper
   - Wave parameters H_s, T_p, γ → Test case specifications

2. **From NEMOH/FDI Toolbox Output**
   - Radiation matrices A_r, B_r, C_r → Saved `.mat` or exported data
   - Excitation matrices A_e, B_e, C_e → Similar export

3. **From Generator Selection**
   - R_a, L_a, K_i, K_v → Machine datasheet or paper Sec. III.A

4. **From Simulation Needs**
   - t_end, dt → Based on wave period T_p

## Parameter Checklist

```
Mechanical:
  ☐ M (total mass)
  ☐ k_b (buoyancy stiffness)

Radiation (4 matrices):
  ☐ A_r (4×4)
  ☐ B_r (4×1)
  ☐ C_r (1×4)

Excitation (3 matrices):
  ☐ A_e (n_e×n_e)
  ☐ B_e (n_e×1)
  ☐ C_e (1×n_e)
  ☐ n_e (order)

Wave Spectrum:
  ☐ H_s (significant height)
  ☐ T_p (peak period)
  ☐ γ (peakedness)

Generator:
  ☐ R_a (resistance)
  ☐ L_a (inductance)
  ☐ K_i (force constant)
  ☐ K_v (back-EMF constant)

Control:
  ☐ K (from MIPC formulation)

Simulation:
  ☐ t_end (simulation end time)
  ☐ dt (time step)
```