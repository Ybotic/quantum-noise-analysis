import pandas as pd
import numpy as np

from config import RAW_DATA_FILE, STATISTICS_FILE

INPUT_FILE = RAW_DATA_FILE
OUTPUT_FILE = STATISTICS_FILE

def calculate_statistics(df):

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

    n = 5
    t_critical = 2.776

    grouped["success_ci"] = (
        t_critical
        * grouped["std_success"]
        / np.sqrt(n)
    )

    grouped["success_ci_lower"] = (
        grouped["mean_success"]
        - grouped["success_ci"]
    )

    grouped["success_ci_upper"] = (
        grouped["mean_success"]
        + grouped["success_ci"]
    )


    grouped["success_ci_lower"] = (
        grouped["success_ci_lower"].clip(0, 1)
    )

    grouped["success_ci_upper"] = (
        grouped["success_ci_upper"].clip(0, 1)
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