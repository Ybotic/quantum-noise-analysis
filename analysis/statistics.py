import pandas as pd

df = pd.read_csv("noise_experiment.csv")

stats = (
    df.groupby(
        [
            "qubits",
            "depth",
            "noise_model",
            "noise_probability"
        ]
    )["success_probability"]
    .agg(["mean", "std"])
    .reset_index()
)


stats = stats.rename(
    columns={
        "mean": "mean_success",
        "std": "std_success"
    }
)

stats["mean_error_rate"] = 1 - stats["mean_success"]



print(stats)

stats.to_csv(
    "analysis/statistical_results.csv",
    index=False
)

print("\nStatistical results saved to analysis/statistical_results.csv")