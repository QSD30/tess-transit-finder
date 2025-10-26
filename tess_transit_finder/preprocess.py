"""
Preprocessing functions for TESS light curves.
"""
import numpy as np
from lightkurve.lightcurve import LightCurve

def clean_and_flatten(lc: LightCurve, sigma_clip: float = 5.0, window_length: int = 401, polyorder: int = 2) -> tuple[LightCurve, np.ndarray]:
    """
    Cleans and flattens a light curve.

    Args:
        lc (LightCurve): The input light curve.
        sigma_clip (float, optional): Sigma for outlier removal. Defaults to 5.0.
        window_length (int, optional): Window length for Savitzky-Golay filter. Defaults to 401.
        polyorder (int, optional): Polynomial order for Savitzky-Golay filter. Defaults to 2.

    Returns:
        tuple[LightCurve, np.ndarray]: The flattened light curve and the mask of good data.
    """
    print("Cleaning and flattening light curve...")
    
    # 1. Remove NaNs
    lc = lc.remove_nans()

    # 2. Mask bad quality cadences
    quality_mask = lc.quality == 0
    lc = lc[quality_mask]

    # 3. Remove outliers
    lc = lc.remove_outliers(sigma=sigma_clip)

    # 4. Flatten the light curve
    lc_flat = lc.flatten(window_length=window_length, polyorder=polyorder)
    
    print("Light curve cleaned and flattened.")
    return lc_flat, quality_mask
