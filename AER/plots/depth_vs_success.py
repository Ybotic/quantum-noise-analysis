import pandas as pd
import matplotlib.pyplot as plt

from config import RAW_DATA_FILE

df = pd.read_csv(RAW_DATA_FILE)

df = df[df["qubits"] == 3]

noise_levels = [0.001, 0.01, 0.05, 0.10]

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

from pathlib import Path

output_dir = Path("results/figures")
output_dir.mkdir(parents=True, exist_ok=True)

plt.tight_layout()
plt.savefig(
    output_dir / "depth_vs_success.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()