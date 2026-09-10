from src.circuits import create_circuit
from src.simulator import run_circuit
from src.metrics import calculate_success_probability
from src.noise_models import create_bit_flip_noise


def main():
    num_qubits = 3
    depth = 4
    shots = 1000
    expected_state = "101"

    circuit = create_circuit(num_qubits, depth)

    # Ideal simulation
    ideal_counts = run_circuit(circuit, shots)

    ideal_success = calculate_success_probability(
        ideal_counts,
        expected_state
    )

    # Noisy simulation
    noise_model = create_bit_flip_noise(0.01)

    noisy_counts = run_circuit(
        circuit,
        shots,
        noise_model
    )

    noisy_success = calculate_success_probability(
        noisy_counts,
        expected_state
    )

    print("===== IDEAL =====")
    print(ideal_counts)
    print(f"Success Probability: {ideal_success:.2%}")

    print("\n===== 1% BIT-FLIP NOISE =====")
    print(noisy_counts)
    print(f"Success Probability: {noisy_success:.2%}")


if __name__ == "__main__":
    main()