import pandas as pd

from config import STATISTICS_FILE, MODEL_COMPARISON_FILE

df = pd.read_csv(STATISTICS_FILE)

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
    MODEL_COMPARISON_FILE,
    index=False
)

print("\nSaved to results/processed/noise_model_comparison_results.csv")