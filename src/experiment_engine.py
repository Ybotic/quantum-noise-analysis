import pandas as pd

from src.circuits import create_circuit

from src.simulator import run_circuit

from src.metrics import calculate_metrics

from src.noise_models import (
    create_bit_flip_noise,
    create_phase_flip_noise,
    create_depolarizing_noise,
    create_readout_noise,
    create_thermal_relaxation_noise
)

def get_noise_model(noise_model, probability):
    if noise_model == "bit_flip":
        return create_bit_flip_noise(probability)

    if noise_model == "phase_flip":
        return create_phase_flip_noise(probability)

    if noise_model == "depolarizing":
        return create_depolarizing_noise(probability)

    if noise_model == "readout":
        return create_readout_noise(probability)

    if noise_model == "thermal":
        return create_thermal_relaxation_noise(probability)

    raise ValueError(f"Unknown noise model: {noise_model}")


def run_experiment(
    num_qubits,
    depth,
    noise_model,
    noise_probability,
    shots=1000,
    seed=None
):
    circuit = create_circuit(
        num_qubits,
        depth
    )

    gate_count = circuit.size()

    ideal_counts = run_circuit(
        circuit,
        shots
    )

    expected_state = max(
        ideal_counts,
        key=ideal_counts.get
    )

    noise = get_noise_model(
        noise_model,
        noise_probability
    )

    noisy_counts = run_circuit(
        circuit,
        shots,
        noise,
        seed=seed
    )

    metrics = calculate_metrics(
        ideal_counts,
        noisy_counts,
        expected_state
    )

    return {
        "qubits": num_qubits,
        "depth": depth,
        "noise_model": noise_model,
        "gate_count": gate_count,
        "noise_probability": noise_probability,
        "shots": shots,
        "seed": seed,
        "success_probability": metrics["success_probability"],
        "error_rate": metrics["error_rate"],
        "fidelity": metrics["fidelity"]
    }


def run_repeated_experiment(
    num_qubits,
    depth,
    noise_model,
    noise_probability,
    shots=1000,
    repetitions=5
):
    results = []

    for repetition in range(repetitions):

        result = run_experiment(
            num_qubits=num_qubits,
            depth=depth,
            noise_model=noise_model,
            noise_probability=noise_probability,
            shots=shots,
            seed=repetition
        )

        result["repetition"] = repetition

        results.append(result)

    return pd.DataFrame(results)