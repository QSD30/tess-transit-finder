"""
BLS period search for TESS light curves.
"""
import numpy as np
from astropy.timeseries import BoxLeastSquares

def run_bls(time: np.ndarray, flux: np.ndarray, flux_err: np.ndarray = None, 
            min_period: float = 0.5, max_period: float = 30.0, 
            min_duration: float = 0.05, max_duration: float = 0.3) -> dict:
    """
    Runs a Box Least Squares (BLS) period search on a light curve.

    Args:
        time (np.ndarray): Time values of the light curve.
        flux (np.ndarray): Flux values of the light curve.
        flux_err (np.ndarray, optional): Flux errors. Defaults to None.
        min_period (float, optional): Minimum period for the search. Defaults to 0.5.
        max_period (float, optional): Maximum period for the search. Defaults to 30.0.
        min_duration (float, optional): Minimum transit duration. Defaults to 0.05.
        max_duration (float, optional): Maximum transit duration. Defaults to 0.3.

    Returns:
        dict: A dictionary containing the BLS results.
    """
    print("Running BLS period search...")
    
    # Use astropy's BoxLeastSquares
    bls = BoxLeastSquares(t=time, y=flux, dy=flux_err)
    
    # Define the period grid
    durations = np.linspace(min_duration, max_duration, 10)
    period_grid = bls.autoperiod(durations, minimum_period=min_period, maximum_period=max_period)
    
    # Compute the power
    power = bls.power(period_grid, durations)
    
    # Find the best-fit parameters
    best_period_index = np.argmax(power.power)
    best_period = power.period[best_period_index]
    best_t0 = power.transit_time[best_period_index]
    best_duration = power.duration[best_period_index]
    best_depth = power.depth[best_period_index]
    snr = power.depth_snr[best_period_index]

    results = {
        "period": best_period,
        "t0": best_t0,
        "duration": best_duration,
        "depth": best_depth,
        "snr": snr,
        "periods": power.period,
        "power": power.power
    }
    
    print(f"BLS search complete. Best period: {best_period:.4f} days")
    return results
