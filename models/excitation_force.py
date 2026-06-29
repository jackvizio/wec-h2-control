"""
Excitation Force Model
======================

The excitation force is the force exerted by the incoming waves on the device.
In frequency domain: F_e(ω) = H_e(ω) * A(ω)
In time domain, this is a convolution integral: f_e(t) = ∫ h_e(t-τ) * η(τ) dτ

The convolution is approximated as a state-space system:
    ẋ_e = A_e * x_e + B_e * η_up(t)
    f_e ≈ C_e * x_e

Where η(t) is the wave elevation (extracted from JONSWAP spectrum).

Reference: Eq. (8-13) in paper, frequency-dependent treatment of excitation.
"""

import numpy as np
from scipy import signal
from scipy.fft import fft, ifft, fftfreq


class JonswapSpectrum:
    """
    JONSWAP wave spectrum model.

    Parameters:
        H_s: Significant wave height [m]
        T_p: Peak period [s]
        gamma: Peakedness parameter (typically 1-7)

    Reference: Eq. (13) in paper
    """

    def __init__(self, H_s, T_p, gamma=3.3):
        """
        Initialize JONSWAP spectrum.

        Args:
            H_s: Significant wave height [m]
            T_p: Peak period [s]
            gamma: Peakedness parameter (default 3.3)
        """
        self.H_s = float(H_s)
        self.T_p = float(T_p)
        self.gamma = float(gamma)

        # Derived parameters
        self.omega_p = 2 * np.pi / self.T_p  # Peak angular frequency [rad/s]
        self.alpha = (0.0081 * 9.81 ** 2) / (0.0081 * 9.81 * self.T_p) ** 4
        # Simplified: alpha ≈ H_s² / (T_p⁴)

    def spectrum(self, omega):
        """
        Evaluate JONSWAP spectrum at angular frequencies.

        Args:
            omega: Angular frequency [rad/s], scalar or array

        Returns:
            S(ω): Spectral density [m²/(rad/s)]
        """
        omega = np.atleast_1d(omega)

        # Avoid division by zero
        omega_safe = np.where(omega > 0, omega, 1e-10)

        # Spectral components
        exp_term = np.exp(-5 / 4 * (self.omega_p / omega_safe) ** 4)

        # Peak enhancement factor
        sigma = np.where(omega_safe <= self.omega_p, 0.07, 0.09)
        r = np.exp(-(omega_safe - self.omega_p) ** 2 / (2 * sigma ** 2 * self.omega_p ** 2))
        gamma_r = self.gamma ** r

        # JONSWAP spectrum (Eq. 13 in paper)
        S = (self.alpha * 9.81 ** 2 / omega_safe ** 5) * exp_term * gamma_r

        return S

    def generate_time_series(self, t, random_seed=None):
        """
        Generate random wave elevation time series from JONSWAP spectrum.

        Uses inverse FFT method: generates spectrum in frequency domain,
        applies random phases, transforms to time domain.

        Args:
            t: Time vector [s]
            random_seed: Seed for reproducibility (default: None)

        Returns:
            eta: Wave elevation time series [m]
        """
        if random_seed is not None:
            np.random.seed(random_seed)

        dt = t[1] - t[0]  # Time step
        N = len(t)

        # Frequency vector (one-sided)
        freqs = fftfreq(N, dt)  # Hz
        omega = 2 * np.pi * freqs[: N // 2]  # Only positive frequencies [rad/s]

        # Evaluate spectrum
        S = self.spectrum(omega)

        # Amplitude spectrum (includes Nyquist twice in 2-sided, here one-sided)
        A = np.sqrt(2 * S * (omega[1] - omega[0]))  # Amplitude per frequency bin

        # Random phases
        phase = np.random.uniform(0, 2 * np.pi, len(A))

        # Complex spectrum (one-sided)
        H_pos = A * np.exp(1j * phase)

        # Construct two-sided spectrum
        H = np.zeros(N, dtype=complex)
        H[: len(H_pos)] = H_pos
        H[1: len(H_pos)] = np.conj(H_pos[1:][::-1])  # Hermitian symmetry

        # Inverse FFT to get time series
        eta = np.real(ifft(H)) * N  # Scale by N (FFT convention)

        return eta


class ExcitationForce:
    """
    State-space model for wave excitation force.

    Approximates the convolution: f_e(t) = ∫ h_e(t-τ) * η(τ) dτ

    As: ẋ_e = A_e * x_e + B_e * η_up(t)
        f_e ≈ C_e * x_e
    """

    def __init__(self, A_e, B_e, C_e, x_e_0=None):
        """
        Initialize excitation force model.

        Args:
            A_e: State matrix (n_e x n_e)
            B_e: Input matrix (n_e x 1)
            C_e: Output matrix (1 x n_e)
            x_e_0: Initial state (default: zeros)
        """
        self.A_e = np.array(A_e, dtype=float)
        self.B_e = np.array(B_e, dtype=float).reshape(-1, 1)
        self.C_e = np.array(C_e, dtype=float).reshape(1, -1)

        # Validate dimensions match
        n_e = self.A_e.shape[0]
        if self.B_e.shape[0] != n_e:
            raise ValueError(f"B_e rows ({self.B_e.shape[0]}) must match A_e size ({n_e})")
        if self.C_e.shape[1] != n_e:
            raise ValueError(f"C_e cols ({self.C_e.shape[1]}) must match A_e size ({n_e})")

        # Initialize state
        if x_e_0 is None:
            self.x_e = np.zeros((n_e, 1))
        else:
            self.x_e = np.array(x_e_0, dtype=float).reshape(-1, 1)

    def state_derivative(self, eta_up):
        """
        Compute state derivative: ẋ_e = A_e * x_e + B_e * η_up

        Args:
            eta_up: Wave elevation [m]

        Returns:
            State derivative (n_e x 1)
        """
        x_e_dot = self.A_e @ self.x_e + self.B_e * eta_up
        return x_e_dot

    def output(self):
        """
        Compute excitation force: f_e = C_e * x_e

        Returns:
            Excitation force [N]
        """
        f_e = (self.C_e @ self.x_e)[0, 0]
        return f_e

    def update(self, eta_up, dt):
        """
        Update excitation state using Euler forward integration.

        Args:
            eta_up: Wave elevation [m]
            dt: Time step [s]
        """
        x_e_dot = self.state_derivative(eta_up)
        self.x_e = self.x_e + x_e_dot * dt

    def get_state(self):
        """Return current state vector."""
        return self.x_e.flatten()

    def set_state(self, x_e_new):
        """Set state vector."""
        self.x_e = np.array(x_e_new, dtype=float).reshape(-1, 1)

    def reset(self, x_e_0=None):
        """Reset state to initial value or zero."""
        if x_e_0 is None:
            self.x_e = np.zeros(self.x_e.shape)
        else:
            self.x_e = np.array(x_e_0, dtype=float).reshape(-1, 1)