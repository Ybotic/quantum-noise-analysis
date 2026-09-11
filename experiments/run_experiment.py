def get_ideal_reference(circuit, shots=1000):

    ideal_counts, expected_state = get_ideal_reference(
        circuit,
        shots
    )

    return ideal_counts, expected_state

import pandas as pd

from config import (
    NOISE_PROBABILITIES,
    DEPTHS,
    QUBIT_COUNTS,
    NOISE_MODELS,
    DEFAULT_SHOTS,
    DEFAULT_REPETITIONS
)

from src.experiment_engine import run_repeated_experiment


def run_full_experiment():

    all_results = []

    for noise_model in NOISE_MODELS:

        print(f"\nRunning {noise_model} noise...")

        for num_qubits in QUBIT_COUNTS:

            for depth in DEPTHS:

                for probability in NOISE_PROBABILITIES:

                    df = run_repeated_experiment(
                        num_qubits=num_qubits,
                        depth=depth,
                        noise_model=noise_model,
                        noise_probability=probability,
                        shots=DEFAULT_SHOTS,
                        repetitions=DEFAULT_REPETITIONS
                    )

                    all_results.append(df)

    final_df = pd.concat(
        all_results,
        ignore_index=True
    )

    return final_df


if __name__ == "__main__":

    final_df = run_full_experiment()

    print("\nFinal dataset:")
    print(final_df)

    final_df.to_csv(
        "results/raw/noise_experiment.csv",
        index=False
    )

    print("\nResults saved to results/raw/noise_experiment.csv")
    print(f"Total rows: {len(final_df)}")