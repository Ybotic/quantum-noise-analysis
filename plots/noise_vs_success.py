import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("noise_experiment.csv")

grouped = (
    df.groupby(["noise_model", "noise_probability"])
    ["success_probability"]
    .mean()
    .reset_index()
)


for noise_model in grouped["noise_model"].unique():

    model_data = grouped[
        grouped["noise_model"] == noise_model
    ]

    plt.plot(
        model_data["noise_probability"],
        model_data["success_probability"],
        marker="o",
        label=noise_model
    )


plt.xlabel("Noise probability")
plt.ylabel("Success probability")
plt.title("Quantum Algorithm Success Under Different Noise Models")

plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()