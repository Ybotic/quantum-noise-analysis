from qiskit_aer import AerSimulator


def run_circuit(circuit, shots=1000, noise_model=None, seed=None):
    """Run a quantum circuit with an optional noise model."""

    simulator = AerSimulator(noise_model=noise_model)

    measured_circuit = circuit.copy()
    measured_circuit.measure_all()

    result = simulator.run(
        measured_circuit,
        shots=shots,
        seed_simulator=seed
    ).result()

    return result.get_counts()