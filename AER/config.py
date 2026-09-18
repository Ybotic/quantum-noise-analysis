import json
from pathlib import Path

NOISE_PROBABILITIES = [
    0.000,
    0.001,
    0.002,
    0.005,
    0.010,
    0.020,
    0.050,
    0.100
]

DEPTHS = [
    1,
    2,
    4,
    8,
    16,
    32
]

QUBIT_COUNTS = [
    2,
    3,
    4,
    5,
    6
]

NOISE_MODELS = [
    "bit_flip",
    "phase_flip",
    "depolarizing",
    "readout",
    "thermal"
]

DEFAULT_SHOTS = 1000
DEFAULT_REPETITIONS = 5

# Experiment metadata

T1 = 50e-6
T2 = 70e-6

EXPERIMENT_METADATA = {
    "shots": DEFAULT_SHOTS,
    "repetitions": DEFAULT_REPETITIONS,
    "qubit_counts": QUBIT_COUNTS,
    "depths": DEPTHS,
    "noise_probabilities": NOISE_PROBABILITIES,
    "noise_models": NOISE_MODELS,
    "t1_seconds": T1,
    "t2_seconds": T2
}

RAW_DATA_FILE = "results/raw/noise_experiment.csv"
STATISTICS_FILE = "results/processed/statistical_results.csv"
SENSITIVITY_FILE = "results/processed/noise_sensitivity_results.csv"
MODEL_COMPARISON_FILE = "results/processed/noise_model_comparison_results.csv"
METADATA_FILE = "results/processed/experiment_metadata.json"


def save_metadata(output_file=METADATA_FILE):
    Path(output_file).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(output_file, "w") as file:
        json.dump(
            EXPERIMENT_METADATA,
            file,
            indent=4
        )

