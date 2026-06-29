# System Architecture

## Overview
The WEC H2 control system is organized into modular components:

### Subsystems
1. **Radiation Force Model** (`models/radiation_force.py`)
   - State-space approximation (order 4)
   - Hydrodynamic reaction of fluid to device motion

2. **Excitation Force Model** (`models/excitation_force.py`)
   - JONSWAP wave spectrum generation
   - Wave excitation force state-space

3. **WEC System** (`models/wec_system.py`)
   - Augmented system combining all subsystems
   - Computes total forces and dynamics

4. **H2 Controller** (`control/h2_controller.py`)
   - LMI-based optimal control design
   - Semidefinite programming solver (CVXPY)

5. **Simulator** (`simulation/simulator.py`)
   - Time-domain ODE integration
   - Runs closed-loop simulation

6. **Visualization** (`visualization/plots.py`)
   - Result plotting and figure generation

## Data Flow

Wave Input

↓

JONSWAP Spectrum → Excitation Force (state-space)

↓

↓

↙───┴───↖

↙         ↖

Radiation Force    Buoyancy

↓                ↓

└────────┬───────┘

↓

WEC Dynamics

↓

H2 Controller

↓

Generator Current

↓

Control Force

## Module Dependencies
config/parameters.py

↓

models/ (radiation_force, excitation_force, wec_system)

↓

control/ (h2_controller)

↓

simulation/ (simulator)

↓

visualization/ (plots)

↓

main.py

