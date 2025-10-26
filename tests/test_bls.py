"""
Test for the BLS module.
"""
import numpy as np
from tess_transit_finder.bls import run_bls

def test_run_bls_on_synthetic_data():
    """Test BLS on a synthetic light curve with an injected transit."""
    # Generate a synthetic light curve
    time = np.linspace(0, 30, 1000)
    flux = np.ones_like(time)
    flux_err = np.random.normal(0, 0.0001, len(time))

    # Inject a transit
    period = 3.5
    t0 = 1.0
    duration = 0.1
    depth = 0.01
    phase = (time - t0 + 0.5 * period) % period - 0.5 * period
    in_transit = np.abs(phase) < duration / 2
    flux[in_transit] -= depth
    flux += flux_err

    # Run BLS
    results = run_bls(time, flux, min_period=3.0, max_period=4.0)

    # Check if the period is recovered
    assert np.isclose(results["period"].value, period, atol=0.01)
    assert results["snr"] > 5
