"""
CLI for TESS Transit Finder.
"""
import argparse
import os
import pandas as pd
from . import io, preprocess, bls, plotting

def main():
    parser = argparse.ArgumentParser(description="Find exoplanet transits in TESS light curves.")
    parser.add_argument("--target", type=str, required=True, help="Target identifier (e.g., TIC ID or name).")
    parser.add_argument("--sector", type=int, help="TESS sector to search.")
    parser.add_argument("--out", type=str, default="./outputs", help="Output directory for results.")
    parser.add_argument("--min-period", type=float, default=0.5, help="Minimum period for BLS search.")
    parser.add_argument("--max-period", type=float, default=30.0, help="Maximum period for BLS search.")
    parser.add_argument("--min-duration", type=float, default=0.05, help="Minimum transit duration.")
    parser.add_argument("--max-duration", type=float, default=0.3, help="Maximum transit duration.")
    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.out, exist_ok=True)

    # 1. Search and download light curve
    lc = io.search_download_lightcurve(args.target, sector=args.sector)
    plotting.plot_raw(lc, args.out)

    # 2. Clean and flatten
    lc_flat, _ = preprocess.clean_and_flatten(lc)
    plotting.plot_flattened(lc_flat, args.out)

    # 3. Run BLS
    time = lc_flat.time.value
    flux = lc_flat.flux.value
    flux_err = lc_flat.flux_err.value
    bls_results = bls.run_bls(time, flux, flux_err,
                                min_period=args.min_period, max_period=args.max_period,
                                min_duration=args.min_duration, max_duration=args.max_duration)

    # 4. Generate and save plots
    plotting.plot_bls(bls_results["periods"], bls_results["power"], bls_results["period"], args.out)
    plotting.plot_phase_folded(time, flux, bls_results["period"], bls_results["t0"], bls_results["duration"], args.out)
    
    # 5. Save animation
    try:
        plotting.animate_phase_folded(time, flux, bls_results["period"], bls_results["t0"], args.out)
    except Exception as e:
        print(f"Could not create animation. ffmpeg might not be installed. Error: {e}")

    # 6. Write CSV report
    report = {
        "target": args.target,
        "sector": args.sector,
        "best_period_days": bls_results["period"],
        "transit_time_bjd": bls_results["t0"],
        "transit_duration_days": bls_results["duration"],
        "transit_depth_ppm": bls_results["depth"],
        "snr": bls_results["snr"]
    }
    df = pd.DataFrame([report])
    df.to_csv(os.path.join(args.out, "report.csv"), index=False)

    print(f"\nResults saved to {args.out}")

if __name__ == "__main__":
    main()
