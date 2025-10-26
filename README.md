# TESS Transit Finder

This is a simple tool to find exoplanet transits in TESS data.

## How to use it

1.  **Clone the code:**
    ```bash
    git clone https://github.com/QSD30/tess-transit-finder.git
    cd tess-transit-finder
    ```

2.  **Install the good stuff:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run it!**
    Here's an example for the star Pi Mensae:
    ```bash
    python -m tess_transit_finder.cli --target "Pi Men" --sector 1
    ```
    This will create an `outputs` directory with the results.

## What you get

The tool will spit out a few files:

*   `raw.png`: The raw data from TESS.
*   `flattened.png`: The cleaned-up data.
*   `bls.png`: A plot that shows the most likely transit periods.
*   `phase_folded.png`: The transit, nice and clear.
*   `report.csv`: A file with the nitty-gritty details of the transit.
*   `phase_animation.mp4`: A cool animation of the transit (if you have ffmpeg installed).