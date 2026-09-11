import pandas as pd

df = pd.read_csv("analysis/statistical_results.csv")

sensitivity = (
    df.groupby(
        ["noise_model", "noise_probability"]
    )["mean_success"]
    .mean()
    .reset_index()
)

baseline = (
    sensitivity[
        sensitivity["noise_probability"] == 0
    ][
        ["noise_model", "mean_success"]
    ]
    .rename(
        columns={
            "mean_success": "baseline_success"
        }
    )
)

sensitivity = sensitivity.merge(
    baseline,
    on="noise_model"
)

sensitivity["success_drop"] = (
    sensitivity["baseline_success"]
    - sensitivity["mean_success"]
)

sensitivity["percent_degradation"] = (
    sensitivity["success_drop"]
    / sensitivity["baseline_success"]
) * 100

print(sensitivity)

sensitivity.to_csv(
    "analysis/noise_sensitivity_results.csv",
    index=False
)

print("\nSaved to analysis/noise_sensitivity_results.csv")