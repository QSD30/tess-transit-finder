"""
Plotting functions for TESS transit finder.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from lightkurve.lightcurve import LightCurve

def plot_raw(lc: LightCurve, output_path: str):
    """Plots the raw light curve."""
    plt.figure(figsize=(10, 5))
    lc.scatter()
    plt.title("Raw Light Curve")
    plt.xlabel("Time [BJD]")
    plt.ylabel("Flux")
    plt.savefig(os.path.join(output_path, "raw.png"))
    plt.close()

def plot_flattened(lc_flat: LightCurve, output_path: str):
    """Plots the flattened light curve."""
    plt.figure(figsize=(10, 5))
    lc_flat.scatter()
    plt.title("Flattened Light Curve")
    plt.xlabel("Time [BJD]")
    plt.ylabel("Normalized Flux")
    plt.savefig(os.path.join(output_path, "flattened.png"))
    plt.close()

def plot_bls(periods: np.ndarray, power: np.ndarray, best_period: float, output_path: str):
    """Plots the BLS power spectrum."""
    plt.figure(figsize=(10, 5))
    plt.plot(periods, power)
    plt.axvline(best_period, color='r', linestyle='--', label=f"Best Period: {best_period:.4f} days")
    plt.title("BLS Power Spectrum")
    plt.xlabel("Period [days]")
    plt.ylabel("Power")
    plt.legend()
    plt.savefig(os.path.join(output_path, "bls.png"))
    plt.close()

def plot_phase_folded(time: np.ndarray, flux: np.ndarray, period: float, t0: float, duration: float, output_path: str):
    """Plots the phase-folded light curve with a simple box model."""
    phase = (time - t0 + 0.5 * period) % period - 0.5 * period
    
    plt.figure(figsize=(10, 5))
    plt.scatter(phase, flux, s=2)
    
    # Box model
    half_duration = duration / 2.0
    plt.plot([-half_duration, half_duration], [1.0, 1.0], 'r-')
    plt.plot([-half_duration, -half_duration], [1.0, np.min(flux)], 'r-')
    plt.plot([half_duration, half_duration], [1.0, np.min(flux)], 'r-')
    plt.plot([-half_duration, half_duration], [np.min(flux), np.min(flux)], 'r-')

    plt.title(f"Phase-Folded Light Curve (P={period:.4f} d)")
    plt.xlabel("Phase [days]")
    plt.ylabel("Normalized Flux")
    plt.savefig(os.path.join(output_path, "phase_folded.png"))
    plt.close()

def animate_phase_folded(time: np.ndarray, flux: np.ndarray, period: float, t0: float, output_path: str):
    """Creates an MP4 animation of the phase-folded transit."""
    fig, ax = plt.subplots(figsize=(8, 6))

    def update(frame):
        ax.clear()
        phase = (time - t0 - frame * period / 100) % period
        ax.scatter(phase, flux, s=5)
        ax.set_title(f"Phase-Folded Transit Animation (Frame {frame}/100)")
        ax.set_xlabel("Phase")
        ax.set_ylabel("Normalized Flux")
        ax.set_xlim(0, period)

    anim = FuncAnimation(fig, update, frames=100, interval=50)
    anim.save(os.path.join(output_path, "phase_animation.mp4"), writer='ffmpeg')
    plt.close()
