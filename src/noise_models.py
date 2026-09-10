from qiskit_aer.noise import (
    NoiseModel,
    pauli_error,
    depolarizing_error,
    ReadoutError,
    thermal_relaxation_error
)

def create_bit_flip_noise(probability):
    """Create a bit-flip noise model."""

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
    """Create a phase-flip noise model."""

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
    """Create a depolarizing noise model."""

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

def create_readout_noise(probability):
    """Create a readout error noise model."""

    noise_model = NoiseModel()

    readout_error = ReadoutError([
        [1 - probability, probability],
        [probability, 1 - probability]
    ])

    noise_model.add_all_qubit_readout_error(
        readout_error
    )

    return noise_model

def create_thermal_relaxation_noise(
    probability,
    t1=50e-6,
    t2=70e-6
):
    """Create a thermal relaxation noise model."""

    noise_model = NoiseModel()

    # Use probability to scale the effective gate exposure time.
    gate_time = probability * 1e-6

    # Avoid zero-time thermal error at probability = 0.
    if probability == 0:
        gate_time = 0

    single_qubit_error = thermal_relaxation_error(
        t1,
        t2,
        gate_time
    )

    two_qubit_error = single_qubit_error.tensor(
        single_qubit_error
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