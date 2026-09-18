import pandas as pd
import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent / "AER")
)

from qiskit_ibm_runtime import (
    QiskitRuntimeService,
    SamplerV2 as Sampler
)

from qiskit.transpiler import generate_preset_pass_manager

from src.circuits import create_circuit
from src.simulator import run_circuit

BACKEND_NAME = "ibm_marrakesh"

QUBIT_COUNTS = [2, 3, 4, 5, 6]
DEPTHS = [1, 2, 4, 8, 16, 32]

SHOTS = 1000
REPETITIONS = 5

service = QiskitRuntimeService(
    instance="open-instance"
)

backend = service.backend(BACKEND_NAME)

print(f"Using backend: {backend.name}")
print(f"Physical qubits: {backend.num_qubits}")

pass_manager = generate_preset_pass_manager(
    backend=backend,
    optimization_level=1
)

circuits = []
experiment_info = []

for num_qubits in QUBIT_COUNTS:

    for depth in DEPTHS:

        circuit = create_circuit(
            num_qubits=num_qubits,
            depth=depth
        )

        circuit.measure_all()

        ideal_counts = run_circuit(
            circuit,
            shots=SHOTS
        )

        expected_state = max(
            ideal_counts,
            key=ideal_counts.get
        )

        transpiled_circuit = pass_manager.run(circuit)

        for repetition in range(REPETITIONS):

            circuits.append(transpiled_circuit)

            experiment_info.append({
                "qubits": num_qubits,
                "depth": depth,
                "repetition": repetition,
                "expected_state": expected_state,
                "logical_gate_count": circuit.size(),
                "transpiled_gate_count": transpiled_circuit.size()
            })


print(f"\nPrepared {len(circuits)} hardware circuits.")


sampler = Sampler(mode=backend)

print("\nSubmitting job to IBM hardware...")

job = sampler.run(
    circuits,
    shots=SHOTS
)

print(f"Job ID: {job.job_id()}")
print("Waiting for IBM hardware results...")

result = job.result()

print("Hardware execution complete!")

results = []

for index, info in enumerate(experiment_info):

    counts = result[index].data.meas.get_counts()

    total_shots = sum(counts.values())

    successful_shots = counts.get(
        info["expected_state"],
        0
    )

    success_probability = (
        successful_shots / total_shots
    )

    error_rate = 1 - success_probability

    results.append({
        "backend": BACKEND_NAME,
        "qubits": info["qubits"],
        "depth": info["depth"],
        "repetition": info["repetition"],
        "shots": SHOTS,
        "expected_state": info["expected_state"],
        "logical_gate_count": info["logical_gate_count"],
        "transpiled_gate_count": info["transpiled_gate_count"],
        "success_probability": success_probability,
        "error_rate": error_rate,
        "counts": counts,
        "job_id": job.job_id()
    })

df = pd.DataFrame(results)

output_file = "ibm_hardware_results.csv"

df.to_csv(
    output_file,
    index=False
)

print("\nExperiment complete.")
print(f"Results saved to: {output_file}")

print("\nSummary:")
print(df[
    [
        "qubits",
        "depth",
        "repetition",
        "success_probability",
        "error_rate"
    ]
])