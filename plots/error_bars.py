import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("analysis/statistical_results.csv")

df = df[
    (df["qubits"] == 3) &
    (df["depth"] == 8) &
    (df["noise_model"] == "depolarizing")
]

plt.errorbar(
    df["noise_probability"],
    df["mean_success"],
    yerr=df["std_success"],
    marker="o",
    capsize=4,
    label="Depolarizing noise"
)


plt.xlabel("Noise probability")
plt.ylabel("Mean success probability")
plt.title("Success Probability with Experimental Variability")

plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()