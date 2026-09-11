import pandas as pd

df = pd.read_csv("analysis/statistical_results.csv")

comparison = (
    df.groupby("noise_model")["mean_success"]
    .mean()
    .reset_index()
)

comparison["mean_error_rate"] = (
    1 - comparison["mean_success"]
)

comparison["overall_degradation"] = (
    (1 - comparison["mean_success"]) * 100
)

comparison = comparison.sort_values(
    "mean_success"
)

print(comparison)

comparison.to_csv(
    "analysis/noise_model_comparison_results.csv",
    index=False
)

print("\nSaved to analysis/noise_model_comparison_results.csv")