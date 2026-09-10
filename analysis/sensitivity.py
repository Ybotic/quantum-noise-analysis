import pandas as pd

df = pd.read_csv("analysis/statistical_results.csv")

df_depth = df[df["qubits"] == 3]

shallow = df_depth[df_depth["depth"] == 1][
    ["noise_model", "noise_probability", "mean_success"]
].rename(
    columns={"mean_success": "success_depth_1"}
)

deep = df_depth[df_depth["depth"] == 32][
    ["noise_model", "noise_probability", "mean_success"]
].rename(
    columns={"mean_success": "success_depth_32"}
)

comparison = shallow.merge(
    deep,
    on=["noise_model", "noise_probability"]
)

comparison["success_drop"] = (
    comparison["success_depth_1"]
    - comparison["success_depth_32"]
)

comparison["percent_degradation"] = (
    comparison["success_drop"]
    / comparison["success_depth_1"]
) * 100

print(comparison)

df_qubits = df[df["depth"] == 8]

small = df_qubits[df_qubits["qubits"] == 2][
    ["noise_model", "noise_probability", "mean_success"]
].rename(
    columns={"mean_success": "success_2_qubits"}
)

large = df_qubits[df_qubits["qubits"] == 6][
    ["noise_model", "noise_probability", "mean_success"]
].rename(
    columns={"mean_success": "success_6_qubits"}
)

qubit_comparison = small.merge(
    large,
    on=["noise_model", "noise_probability"]
)

qubit_comparison["success_drop"] = (
    qubit_comparison["success_2_qubits"]
    - qubit_comparison["success_6_qubits"]
)

qubit_comparison["percent_degradation"] = (
    qubit_comparison["success_drop"]
    / qubit_comparison["success_2_qubits"]
) * 100

print("\n\nQUBIT SENSITIVITY")
print(qubit_comparison)