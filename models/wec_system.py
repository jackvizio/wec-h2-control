"""
WEC System Model (Augmented)
=============================

Combines all subsystems into a single augmented state-space model:

    M·z̈ = f_b(t) + f_r(t) + f_e(t) + f_c(t)

Where:
    f_b = buoyancy (linear spring): -k_b * z
    f_r = radiation force (state-space): C_r * x_r
    f_e = excitation force (state-space): C_e * x_e
    f_c = control force: K_i * i(t)

Augmented state vector:
    x = [x_r1, x_r2, x_r3, x_r4, x_e1, ..., x_e(n_e), z, ż]ᵀ

Reference: Eq. (1-2, 23-24) in paper.
"""

import numpy as np
from scipy.integrate import odeint, solve_ivp


class WECSystem:
    """
    Complete WEC system with radiation, excitation, and dynamics.

    Attributes:
        M: Total mass [kg]
        k_b: Buoyancy stiffness [N/m]
        radiation_force: RadiationForce instance
        excitation_force: ExcitationForce instance
        K_i: Force constant of generator [N/A]
    """

    def __init__(self, M, k_b, radiation_force, excitation_force, K_i):
        """
        Initialize WEC system.

        Args:
            M: Total mass [kg]
            k_b: Buoyancy stiffness [N/m]
            radiation_force: RadiationForce instance
            excitation_force: ExcitationForce instance
            K_i: Force constant [N/A]
        """
        self.M = float(M)
        self.k_b = float(k_b)
        self.radiation_force = radiation_force
        self.excitation_force = excitation_force
        self.K_i = float(K_i)

        # Dimension info
        self.n_r = 4  # Radiation state dimension (fixed order 4)
        self.n_e = self.excitation_force.A_e.shape[0]  # Excitation state dimension
        self.n_total = self.n_r + self.n_e + 2  # Total: x_r + x_e + z + z_dot

    def compute_forces(self, z, z_dot, i, f_e):
        """
        Compute all forces on the system.

        Args:
            z: Displacement [m]
            z_dot: Velocity [m/s]
            i: Generator current [A]
            f_e: Excitation force [N]

        Returns:
            Dict with forces: f_b, f_r, f_e, f_c, f_h
        """
        f_b = -self.k_b * z  # Buoyancy (Eq. 4)
        f_r = self.radiation_force.output()  # Radiation
        f_c = self.K_i * i  # Control force (from Eq. 14 in paper)
        f_h = f_b + f_r + f_e  # Total hydrodynamic force

        return {
            'f_b': f_b,
            'f_r': f_r,
            'f_e': f_e,
            'f_c': f_c,
            'f_h': f_h
        }

    def state_derivatives(self, z, z_dot, i, f_e):
        """
        Compute derivatives for heave motion and subsystem states.

        Args:
            z: Displacement [m]
            z_dot: Velocity [m/s]
            i: Generator current [A]
            f_e: Excitation force [N]

        Returns:
            z_dot_out, z_ddot, x_r_dot, x_e_dot
        """
        # Heave acceleration (Eq. 1): M·z̈ = f_h + f_c
        forces = self.compute_forces(z, z_dot, i, f_e)
        f_h = forces['f_h']
        f_c = forces['f_c']
        z_ddot = (f_h + f_c) / self.M

        # Radiation state derivative
        x_r_dot = self.radiation_force.state_derivative(z_dot)

        # Excitation state derivative
        x_e_dot = self.excitation_force.state_derivative(0)  # eta_up=0 for now

        return z_dot, z_ddot, x_r_dot.flatten(), x_e_dot.flatten()

    def augmented_state_vector(self):
        """
        Assemble augmented state vector from subsystem states.

        Returns:
            x: [x_r (4,), x_e (n_e,), z, z_dot]
        """
        x_r = self.radiation_force.get_state()
        x_e = self.excitation_force.get_state()
        z = 0  # Placeholder - will be updated during simulation
        z_dot = 0  # Placeholder

        x = np.concatenate([x_r, x_e, [z, z_dot]])
        return x

    def reset(self, z_0=0, z_dot_0=0, x_r_0=None, x_e_0=None):
        """
        Reset system to initial conditions.

        Args:
            z_0: Initial displacement [m]
            z_dot_0: Initial velocity [m/s]
            x_r_0: Initial radiation state (default: zeros)
            x_e_0: Initial excitation state (default: zeros)

        Returns:
            Initial augmented state vector
        """
        self.radiation_force.reset(x_r_0)
        self.excitation_force.reset(x_e_0)

        x_r = self.radiation_force.get_state()
        x_e = self.excitation_force.get_state()

        x_init = np.concatenate([x_r, x_e, [z_0, z_dot_0]])
        return x_init

    def print_summary(self):
        """Print system summary."""
        print("\n" + "=" * 70)
        print("WEC SYSTEM SUMMARY")
        print("=" * 70)
        print(f"Total Mass (M):              {self.M:.3e} kg")
        print(f"Buoyancy Stiffness (k_b):    {self.k_b:.3e} N/m")
        print(f"Generator Force Constant:    {self.K_i:.3e} N/A")
        print(f"\nRadiation State Dimension:   {self.n_r}")
        print(f"Excitation State Dimension:  {self.n_e}")
        print(f"Total Augmented Dim:         {self.n_total}")
        print("=" * 70 + "\n")