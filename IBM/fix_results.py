import pandas as pd
import ast

df = pd.read_csv("ibm_hardware_results.csv")

def fix_row(row):
    counts = ast.literal_eval(row["counts"])
    expected_state = "0" * int(row["qubits"])
    total_shots = sum(counts.values())
    successful_shots = counts.get(expected_state, 0)

    row["expected_state"] = expected_state
    row["success_probability"] = successful_shots / total_shots
    row["error_rate"] = 1 - row["success_probability"]

    return row

df = df.apply(fix_row, axis=1)

df.to_csv("ibm_hardware_results_fixed.csv", index=False)

print(df[
    ["qubits", "depth", "repetition",
     "expected_state", "success_probability", "error_rate"]
].to_string(index=False))

print("\nSaved to ibm_hardware_results_fixed.csv")