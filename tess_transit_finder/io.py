"""
I/O operations for TESS transit finder.
"""
from typing import Optional
import lightkurve as lk
from lightkurve.lightcurve import LightCurve

def search_download_lightcurve(target: str, mission: str = "TESS", sector: Optional[int] = None) -> LightCurve:
    """
    Searches and downloads a target's light curve.

    Args:
        target (str): The target identifier (e.g., TIC ID or name).
        mission (str, optional): The mission to search. Defaults to "TESS".
        sector (Optional[int], optional): The TESS sector to search. Defaults to None (all sectors).

    Returns:
        LightCurve: The downloaded light curve object.
    """
    print(f"Searching for {target} in {mission} data...")
    search_result = lk.search_lightcurve(target, mission=mission, sector=sector)
    if not search_result:
        raise ValueError(f"No light curve found for target '{target}' with the specified criteria.")
    
    print(f"Found {len(search_result)} light curve(s). Downloading...")
    lc_collection = search_result.download_all()
    
    if not lc_collection:
        raise ValueError(f"Failed to download light curve for target '{target}'.")

    # Stitch the light curves together if there are multiple sectors
    lc = lc_collection.stitch()
    print("Download and stitching complete.")
    return lc
