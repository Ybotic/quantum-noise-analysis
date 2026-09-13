import pandas as pd
import matplotlib.pyplot as plt

from config import RAW_DATA_FILE

df = pd.read_csv(RAW_DATA_FILE)

df = df[
    (df["depth"] == 8) &
    (df["noise_model"] == "depolarizing")
]


noise_levels = [0.001, 0.01, 0.05, 0.10]


for probability in noise_levels:

    data = (
        df[df["noise_probability"] == probability]
        .groupby("qubits")["success_probability"]
        .mean()
        .reset_index()
    )

    plt.plot(
        data["qubits"],
        data["success_probability"],
        marker="o",
        label=f"Noise = {probability}"
    )


plt.xlabel("Number of qubits")
plt.ylabel("Success probability")
plt.title("Effect of Qubit Count on Quantum Algorithm Success")

plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()