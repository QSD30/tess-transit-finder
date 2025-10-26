# TESS Transit Finder

A Python CLI project that detects exoplanet transits in TESS light curves.

## Installation

1.  Clone this repository:
    ```bash
    git clone <repository-url>
    cd tess-transit-finder
    ```

2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Install the project in editable mode:
    ```bash
    pip install -e .
    ```

4.  (Optional) For the animation feature, you need to have ffmpeg installed.

## Usage

The CLI tool can be run from the command line:

```bash
tess-transit-finder --target "<target-name-or-tic-id>" --sector <sector-number> --out <output-directory>
```

### Example

Here is an example of how to run the tool on a known TESS planet host, Pi Mensae (TIC 261136679), which was observed in Sector 1:

```bash
tess-transit-finder --target "Pi Men" --sector 1 --out ./outputs
```

## Expected Outputs

The tool will create an output directory (e.g., `./outputs`) containing the following files:

-   `raw.png`: The raw light curve as downloaded.
-   `flattened.png`: The cleaned and flattened light curve.
-   `bls.png`: The BLS power spectrum, with the best period highlighted.
-   `phase_folded.png`: The light curve folded on the best-fit period, with a simple box model.
-   `report.csv`: A CSV file containing the best-fit parameters (period, t0, duration, depth, SNR).
-   `phase_animation.mp4`: An animation of the phase-folded transit (requires ffmpeg).

### Example Output Images

**Flattened Light Curve:**

![Flattened Light Curve](https.storage.googleapis.com/gemini-community-governance/images/tess-transit-finder/flattened.png)

**BLS Power Spectrum:**

![BLS Power Spectrum](https.storage.googleapis.com/gemini-community-governance/images/tess-transit-finder/bls.png)

**Phase-Folded Light Curve:**

![Phase-Folded Light Curve](https.storage.googleapis.com/gemini-community-governance/images/tess-transit-finder/phase_folded.png)
