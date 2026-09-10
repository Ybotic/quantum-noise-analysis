from qiskit import QuantumCircuit


def create_circuit(num_qubits: int, depth: int) -> QuantumCircuit:
    """
    Create a deterministic quantum benchmark circuit.

    The circuit creates superposition and entanglement,
    performs repeated work layers, and then uncomputes
    the state so the ideal final measurement is deterministic.
    """

    circuit = QuantumCircuit(num_qubits)

    # Create superposition
    for qubit in range(num_qubits):
        circuit.h(qubit)

    # Repeated computational layers
    for _ in range(depth):

        # Entanglement
        for qubit in range(num_qubits - 1):
            circuit.cx(qubit, qubit + 1)

        # Additional basis changes
        for qubit in range(num_qubits):
            circuit.h(qubit)

    # Reverse the computational layers
    for _ in range(depth):

        for qubit in range(num_qubits):
            circuit.h(qubit)

        for qubit in reversed(range(num_qubits - 1)):
            circuit.cx(qubit, qubit + 1)

    # Undo initial superposition
    for qubit in range(num_qubits):
        circuit.h(qubit)

    return circuit