import pandas as pd
import matplotlib.pyplot as plt


# Load experiment data
df = pd.read_csv("noise_experiment.csv")


# Focus on 3 qubits
df = df[df["qubits"] == 3]


# Choose noise levels to compare
noise_levels = [0.001, 0.01, 0.05, 0.10]


# Plot each noise level
for probability in noise_levels:

    data = (
        df[df["noise_probability"] == probability]
        .groupby("depth")["success_probability"]
        .mean()
        .reset_index()
    )

    plt.plot(
        data["depth"],
        data["success_probability"],
        marker="o",
        label=f"Noise = {probability}"
    )


plt.xlabel("Circuit depth")
plt.ylabel("Success probability")
plt.title("Effect of Circuit Depth on Quantum Algorithm Success")

plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()