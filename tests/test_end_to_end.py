"""
End-to-end test for the CLI.
"""
import os
import shutil
import pytest

@pytest.fixture
def temp_output_dir():
    """Create a temporary output directory for tests."""
    path = "./temp_test_outputs"
    os.makedirs(path, exist_ok=True)
    yield path
    shutil.rmtree(path)

def test_cli_end_to_end(temp_output_dir):
    """Smoke test to run the CLI and check for output files."""
    target = "Pi Men"
    sector = 1
    command = f"tess-transit-finder --target \"{target}\" --sector {sector} --out {temp_output_dir}"
    
    # Run the CLI command
    exit_code = os.system(command)
    assert exit_code == 0, f"CLI command failed with exit code {exit_code}"

    # Check for expected output files
    expected_files = [
        "raw.png",
        "flattened.png",
        "bls.png",
        "phase_folded.png",
        "report.csv",
        # "phase_animation.mp4" # Optional, as ffmpeg might not be installed
    ]

    for filename in expected_files:
        assert os.path.exists(os.path.join(temp_output_dir, filename)), f"{filename} was not created."

