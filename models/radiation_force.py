"""
Radiation Force Model
======================

The radiation force represents the hydrodynamic reaction of the fluid to the
body's motion. It has two components:

1. Added mass effect (frequency-dependent inertia)
2. Damping effect (memory/convolution integral)

Both are approximated as a finite-order state-space system (order 4 in this paper):

    ẋ_r = A_r * x_r + B_r * ż
    f_r ≈ C_r * x_r

Reference: Eq. (5-7) in paper, Figure 2 (state-space approximation)
"""

import numpy as np
from scipy.integrate import odeint


class RadiationForce:
    """
    State-space model for radiation force.

    Attributes:
        A_r: State matrix (4x4)
        B_r: Input matrix (4x1)
        C_r: Output matrix (1x4)
        x_r: Internal state vector (4x1)
    """

    def __init__(self, A_r, B_r, C_r, x_r_0=None):
        """
        Initialize radiation force model.

        Args:
            A_r: State matrix (4x4) - radiation dynamics
            B_r: Input matrix (4x1) - velocity input
            C_r: Output matrix (1x4) - radiation force output
            x_r_0: Initial state vector (default: zeros)
        """
        self.A_r = np.array(A_r, dtype=float)
        self.B_r = np.array(B_r, dtype=float).reshape(-1, 1)
        self.C_r = np.array(C_r, dtype=float).reshape(1, -1)

        # Validate dimensions
        if self.A_r.shape != (4, 4):
            raise ValueError(f"A_r must be 4x4, got {self.A_r.shape}")
        if self.B_r.shape != (4, 1):
            raise ValueError(f"B_r must be 4x1, got {self.B_r.shape}")
        if self.C_r.shape != (1, 4):
            raise ValueError(f"C_r must be 1x4, got {self.C_r.shape}")

        # Initialize state
        if x_r_0 is None:
            self.x_r = np.zeros((4, 1))
        else:
            self.x_r = np.array(x_r_0, dtype=float).reshape(-1, 1)

    def state_derivative(self, z_dot):
        """
        Compute state derivative: ẋ_r = A_r * x_r + B_r * ż

        Args:
            z_dot: Heave velocity [m/s]

        Returns:
            State derivative (4x1)
        """
        x_r_dot = self.A_r @ self.x_r + self.B_r * z_dot
        return x_r_dot

    def output(self):
        """
        Compute radiation force: f_r = C_r * x_r

        Returns:
            Radiation force [N]
        """
        f_r = (self.C_r @ self.x_r)[0, 0]
        return f_r

    def update(self, z_dot, dt):
        """
        Update radiation state using Euler forward integration.
        This is a simple update; more sophisticated integration can be used.

        Args:
            z_dot: Heave velocity [m/s]
            dt: Time step [s]
        """
        x_r_dot = self.state_derivative(z_dot)
        self.x_r = self.x_r + x_r_dot * dt

    def get_state(self):
        """Return current state vector."""
        return self.x_r.flatten()

    def set_state(self, x_r_new):
        """Set state vector."""
        self.x_r = np.array(x_r_new, dtype=float).reshape(-1, 1)

    def reset(self, x_r_0=None):
        """Reset state to initial value or zero."""
        if x_r_0 is None:
            self.x_r = np.zeros((4, 1))
        else:
            self.x_r = np.array(x_r_0, dtype=float).reshape(-1, 1)


# ============================================================================
# Utility function for verifying radiation force model stability
# ============================================================================

def check_radiation_stability(A_r):
    """
    Check if radiation force state matrix is stable (all eigenvalues have
    negative real part).

    Args:
        A_r: State matrix (4x4)

    Returns:
        is_stable: Boolean
        eigenvalues: Complex eigenvalues
    """
    eigenvalues = np.linalg.eigvals(A_r)
    is_stable = np.all(np.real(eigenvalues) < 0)

    return is_stable, eigenvalues