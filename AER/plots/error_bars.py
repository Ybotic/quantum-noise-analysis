import pandas as pd
import matplotlib.pyplot as plt

from config import STATISTICS_FILE

df = pd.read_csv(STATISTICS_FILE)

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

from pathlib import Path

output_dir = Path("results/figures")
output_dir.mkdir(parents=True, exist_ok=True)

plt.tight_layout()
plt.savefig(
    output_dir / "error_bars.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()