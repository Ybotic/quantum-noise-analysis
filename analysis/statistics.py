import pandas as pd


INPUT_FILE = "noise_experiment.csv"
OUTPUT_FILE = "results/processed/statistical_results.csv"


def calculate_statistics(df):
    """
    Calculate summary statistics for each
    experimental condition.
    """

    grouped = (
        df.groupby(
            [
                "qubits",
                "depth",
                "noise_model",
                "noise_probability"
            ]
        )
        .agg(
            mean_success=(
                "success_probability",
                "mean"
            ),
            std_success=(
                "success_probability",
                "std"
            ),
            mean_fidelity=(
                "fidelity",
                "mean"
            ),
            std_fidelity=(
                "fidelity",
                "std"
            )
        )
        .reset_index()
    )

    grouped["mean_error_rate"] = (
        1 - grouped["mean_success"]
    )

    return grouped


def main():

    df = pd.read_csv(INPUT_FILE)

    statistics = calculate_statistics(df)

    statistics.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("Statistical analysis complete.")
    print(f"Rows: {len(statistics)}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()