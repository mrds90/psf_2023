import numpy as np


def SinFunc(fs: float, f0: float, amp: float = 1.0, samples: int = 100, phase: float = 0.0) -> [np.ndarray, np.ndarray]:
    t = np.arange(0, samples) / fs
    sin = (amp * np.sin(2 * np.pi * f0 * t + 2 * np.pi * phase))
    return t, sin


def SquareFunc(fs: float, f0: float, amp: float = 1.0, samples: int = 100) -> [np.ndarray, np.ndarray]:
    t = np.arange(0, samples) / fs
    square = (amp * np.sign(np.sin(2 * np.pi * f0 * t)))
    return t, square


def TriangularFunc(fs: float, f0: float, amp: float, samples: int) -> [np.ndarray, np.ndarray]:
    t = np.arange(0, samples) / fs
    triangular_wave = (2 * amp / np.pi) * np.arcsin(np.sin(2 * np.pi * f0 * t))
    return t, triangular_wave

def DeltaFunc(fs: float, samples: int) -> [np.ndarray, np.ndarray]:
    t = np.arange(0, samples) / fs
    delta_values = np.zeros(samples)
    delta_values[0] = 1.0
    return t, delta_values
