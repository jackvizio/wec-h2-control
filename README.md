WEC H2 Control: Maximum Induced Power Optimal Output Feedback

This repository implements the H₂ optimal output feedback controller for a heaving wave energy converter (WEC) from the paper:


"Maximum Induced Power Optimal H₂ Output Feedback Control Design for Heaving Wave Energy Converters"



The implementation translates the original MATLAB code into clean, modular Python using modern scientific computing libraries.


Project Structure

wec-h2-control/
├── README.md                   # This file
├── requirements.txt            # Python dependencies
│
├── config/
│   └── parameters.py           # All system parameters (to be filled from paper)
│
├── models/
│   ├── __init__.py
│   ├── radiation_force.py      # Radiation state-space model (Eq. 5-7)
│   ├── excitation_force.py     # Wave excitation + JONSWAP spectrum (Eq. 8-13)
│   └── wec_system.py           # Augmented WEC system (Eq. 1-2, 23-24)
│
├── control/
│   ├── __init__.py
│   └── h2_controller.py        # H2 optimal controller (LMI solver) [IN PROGRESS]
│
├── simulation/
│   ├── __init__.py
│   └── simulator.py            # Time-domain ODE solver [IN PROGRESS]
│
├── visualization/
│   ├── __init__.py
│   └── plots.py                # Result plotting [IN PROGRESS]
│
└── main.py                     # Entry point / workflow orchestrator [IN PROGRESS]


Installation

1. Clone or setup the repository

bashcd wec-h2-control

2. Create a virtual environment (recommended)

bashpython3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies

bashpip install -r requirements.txt

Required packages:


NumPy: Linear algebra and numerical computing
SciPy: Signal processing, ODE solvers, optimization
Matplotlib: Plotting results
CVXPY: Convex optimization (for LMI solver)
Control: Control systems library



Development Workflow

Current Stage

We are building the project progressively, following the paper step by step:


✅ Models (Radiation, Excitation, WEC System) - Implemented
⏳ Controller Design (H2 LMI Solver) - Next step
⏳ Simulation (Time-domain ODE solver) - Next step
⏳ Visualization (Plotting & validation) - Final step


How to Progress

Each new feature follows this workflow in PyCharm:


Write → New Python module or function based on paper equations
Run → Execute test script in PyCharm to verify
Validate → Check output matches paper logic (dimensions, signs, physics)
Understand → Review comments to ensure clarity
Approve → Mark as complete and move to next step


Example: When we implement the radiation force model:

pythonfrom models import RadiationForce

# Create instance with test matrices
A_r = np.array(...)  # 4x4 from paper
B_r = np.array(...)  # 4x1
C_r = np.array(...)  # 1x4

rad_force = RadiationForce(A_r, B_r, C_r)

# Simulate
z_dot = 0.5  # Test input
f_r = rad_force.state_derivative(z_dot)
print(f"Radiation force: {f_r}")  # Verify output


Paper Reference: Key Equations Implemented

SectionEquationImplementationDynamics(1) M·z̈ = f_h + f_cWECSystemHydro Forces(2) f_h = f_b + f_r + f_ecompute_forces()Buoyancy(4) f_b = -k_b·zLinear springRadiation (state-space)(5-7) ẋ_r = A_r·x_r + B_r·żRadiationForceExcitation (freq domain)(8) F_e(ω) = H_e(ω)·A(ω)JonswapSpectrumExcitation (time domain)(9) f_e(t) = ∫ h_e(t-τ)η(τ)dτExcitationForceJONSWAP spectrum(13) S_η(ω)JonswapSpectrum.spectrum()Excitation (state-space)(12) ẋ_e = A_e·x_e + B_e·ηExcitationForceGenerator dynamics(14) v_a = R_a·i + L_a·di/dt + K_v·ż[To implement]Generator force(15-17) P_c, P_s, P_d[To implement]MIPC condition(18-21) α = 1/(2K)[To implement]Performance output(22) z_p(t) = ż(t) - α·f_c(t)[To implement]Augmented system(23-24) State + output equationsWECSystem


Key Physics & Implementation Notes

Radiation Force


Frequency-dependent hydrodynamic reaction
Approximated as order-4 state-space (Figure 2)
Includes added mass + damping memory effect
Solver: NEMOH → FDI Toolbox → state-space conversion


Excitation Force


Wave elevation η(t) extracted from JONSWAP spectrum
Frequency-dependent excitation transfer function H_e(ω)
Time-domain convolution approximated as state-space
Python implementation: JonswapSpectrum.generate_time_series()


Control Strategy (H₂ LMI)


Objective: Maximize energy absorption while respecting constraints
Approach: Formulate as semidefinite programming problem
Solver: CVXPY (open-source LMI solver)
Reference condition (Eq. 18): ż = -α·f_c (velocity in phase with control force)



Next Steps


Fill numerical parameters from the paper (mass, stiffness, etc.)
Implement H₂ controller using CVXPY LMI solver
Build time-domain simulator with ODE solver
Generate synthetic waves and simulate WEC motion
Reproduce paper results (figures, energy plots, etc.)



Dependencies & Why Each

LibraryPurposeUsed inNumPyMatrix operationsAll modulesSciPySignal proc, ODEs, optimizationradiation_force, excitation_force, simulationMatplotlibPlottingvisualization/plots.pyCVXPYConvex optimization (LMI)control/h2_controller.pyControlControl theory utilities(optional, for analysis)


Running Tests

Once modules are implemented, run in PyCharm:

bash# Test radiation force model
python -c "from models import RadiationForce; ..."

# Test excitation force (JONSWAP)
python -c "from models import JonswapSpectrum; ..."

# Full system simulation
python main.py


References


Paper: "Maximum Induced Power Optimal H₂ Output Feedback Control Design for Heaving Wave Energy Converters"
NEMOH: BEM hydrodynamic solver (https://github.com/lheea/nemoh)
CVXPY: Convex optimization (https://www.cvxpy.org/)
JONSWAP Spectrum: ISO 19901-1 standard for ocean waves



Notes for Development


Placeholder values: parameters.py has None entries—fill from paper as we go
Modular design: Each component is independent and testable
Comments: Extensive comments explain physics and equations
Reproducibility: Random seeds for wave generation ensure consistent results



Contact & Status

Project Status: 🟡 In Development


Models: ✅ Implemented (Radiation, Excitation, WEC System)
Controller: ⏳ Pending (LMI formulation needed)
Simulation: ⏳ Pending (ODE solver)
Visualization: ⏳ Pending (Plotting)


Next move: Send control formulation (LMI section) from paper → implement H2 controller solver.


Built with Python 3.8+, NumPy, SciPy, CVXPY
