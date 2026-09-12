from qiskit_aer.noise import (
    NoiseModel,
    pauli_error,
    depolarizing_error,
    ReadoutError,
    thermal_relaxation_error
)

def create_bit_flip_noise(probability):

    noise_model = NoiseModel()

    single_qubit_error = pauli_error([
        ("X", probability),
        ("I", 1 - probability)
    ])

    noise_model.add_all_qubit_quantum_error(
        single_qubit_error,
        ["h", "x"]
    )

    two_qubit_error = single_qubit_error.tensor(
        single_qubit_error
    )

    noise_model.add_all_qubit_quantum_error(
        two_qubit_error,
        ["cx"]
    )

    return noise_model


def create_phase_flip_noise(probability):

    noise_model = NoiseModel()

    single_qubit_error = pauli_error([
        ("Z", probability),
        ("I", 1 - probability)
    ])

    noise_model.add_all_qubit_quantum_error(
        single_qubit_error,
        ["h", "x"]
    )

    two_qubit_error = single_qubit_error.tensor(
        single_qubit_error
    )

    noise_model.add_all_qubit_quantum_error(
        two_qubit_error,
        ["cx"]
    )

    return noise_model

def create_depolarizing_noise(probability):

    noise_model = NoiseModel()

    single_qubit_error = depolarizing_error(
        probability,
        1
    )

    two_qubit_error = depolarizing_error(
        probability,
        2
    )

    noise_model.add_all_qubit_quantum_error(
        single_qubit_error,
        ["h", "x"]
    )

    noise_model.add_all_qubit_quantum_error(
        two_qubit_error,
        ["cx"]
    )

    return noise_model

def create_thermal_relaxation_noise(
    noise_strength,
    t1=50e-6,
    t2=70e-6
):
    noise_model = NoiseModel()

    gate_time = noise_strength * 1e-6

    if noise_strength == 0:
        gate_time = 0

    single_qubit_error = thermal_relaxation_error(
        t1,
        t2,
        gate_time
    )

    two_qubit_error = (
        single_qubit_error.tensor(single_qubit_error)
    )

    noise_model.add_all_qubit_quantum_error(
        single_qubit_error,
        ["h", "x"]
    )

    noise_model.add_all_qubit_quantum_error(
        two_qubit_error,
        ["cx"]
    )

    return noise_model