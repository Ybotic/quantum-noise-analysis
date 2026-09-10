import pandas as pd

from src.circuits import create_circuit
from src.simulator import run_circuit
from src.metrics import (
    calculate_success_probability,
    calculate_distribution_fidelity
)

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

    elif noise_model == "phase_flip":
        return create_phase_flip_noise(probability)

    elif noise_model == "depolarizing":
        return create_depolarizing_noise(probability)

    elif noise_model == "readout":
        return create_readout_noise(probability)

    elif noise_model == "thermal":
        return create_thermal_relaxation_noise(probability)

    else:
        raise ValueError(f"Unknown noise model: {noise_model}")
    
def run_noise_sweep(
    num_qubits,
    depth,
    noise_probabilities,
    noise_model,
    shots=1000,
    repetitions=5
):
    circuit = create_circuit(num_qubits, depth)
    gate_count = circuit.size()

    # Ideal simulation
    ideal_counts = run_circuit(circuit, shots)

    # Most likely ideal state
    expected_state = max(ideal_counts, key=ideal_counts.get)

    results = []

    for probability in noise_probabilities:

        for repetition in range(repetitions):

            seed = repetition

            noise = get_noise_model(
                noise_model,
                probability
            )

            noisy_counts = run_circuit(
                circuit,
                shots,
                noise,
                seed=seed
            )

            success_probability = calculate_success_probability(
                noisy_counts,
                expected_state
            )

            fidelity = calculate_distribution_fidelity(
                ideal_counts,
                noisy_counts
            )

            results.append({
                "qubits": num_qubits,
                "depth": depth,
                "noise_model": noise_model,
                "gate_count": gate_count,
                "noise_probability": probability,
                "shots": shots,
                "repetition": repetition,
                "seed": seed,
                "success_probability": success_probability,
                "fidelity": fidelity
            })

    return pd.DataFrame(results)


if __name__ == "__main__":

    noise_probabilities = [
        0.000,
        0.001,
        0.002,
        0.005,
        0.010,
        0.020,
        0.050,
        0.100
    ]

    depths = [1, 2, 4, 8, 16, 32]

    noise_models = [
        "bit_flip",
        "phase_flip",
        "depolarizing",
        "readout",
        "thermal"
    ]

    all_results = []

    for noise_model in noise_models:

        print(f"\nRunning {noise_model} noise...")

        for num_qubits in [2, 3, 4, 5, 6]:

            for depth in depths:

                df = run_noise_sweep(
                    num_qubits=num_qubits,
                    depth=depth,
                    noise_probabilities=noise_probabilities,
                    noise_model=noise_model,
                    shots=1000,
                    repetitions=5
                )

                all_results.append(df)

    final_df = pd.concat(
        all_results,
        ignore_index=True
    )

    print("\nFinal dataset:")
    print(final_df)

    final_df.to_csv(
        "noise_experiment.csv",
        index=False
    )

    print("\nResults saved to noise_experiment.csv")
    print(f"Total rows: {len(final_df)}")