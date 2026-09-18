import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from config import RAW_DATA_FILE

df = pd.read_csv(RAW_DATA_FILE)

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

output_dir = Path("results/figures")
output_dir.mkdir(parents=True, exist_ok=True)

plt.tight_layout()
plt.savefig(
    output_dir / "noise_vs_success.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()