from qiskit import QuantumCircuit, transpile
from qiskit.primitives import StatevectorSampler
from qiskit_aer import AerSimulator
from qiskit_aer.noise import (
    NoiseModel,
    pauli_error,
    depolarizing_error
)


def create_superdense_circuit(message, measure=False):

    if message not in ["00", "01", "10", "11"]:
        raise ValueError(
            "Message must be 00, 01, 10, or 11."
        )

    qc = QuantumCircuit(2)

    # Create Bell state
    qc.h(0)
    qc.cx(0, 1)

    # Alice encodes
    if message == "01":
        qc.x(0)

    elif message == "10":
        qc.z(0)

    elif message == "11":
        qc.x(0)
        qc.z(0)

    qc.barrier()

    # Bob decodes
    qc.cx(0, 1)
    qc.h(0)

    if measure:
        qc.measure_all()

    return qc


def convert_counts(counts):

    logical_counts = {}

    for state, count in counts.items():

        logical_state = state[::-1]

        logical_counts[logical_state] = (
            logical_counts.get(logical_state, 0)
            + count
        )

    return logical_counts


def add_all_states(counts):

    states = ["00", "01", "10", "11"]

    return {
        state: counts.get(state, 0)
        for state in states
    }


def run_circuit(circuit, shots=1024):

    sampler = StatevectorSampler()

    result = sampler.run(
        [circuit],
        shots=shots
    ).result()

    raw_counts = result[0].data.meas.get_counts()

    counts = convert_counts(raw_counts)

    return add_all_states(counts)


def create_noise_model(
    noise_type,
    probability
):

    noise_model = NoiseModel()

    if probability <= 0:
        return noise_model

    if noise_type == "Bit Flip":

        error = pauli_error([
            ("I", 1 - probability),
            ("X", probability)
        ])

        noise_model.add_all_qubit_quantum_error(
            error,
            ["h", "x", "z"]
        )

    elif noise_type == "Phase Flip":

        error = pauli_error([
            ("I", 1 - probability),
            ("Z", probability)
        ])

        noise_model.add_all_qubit_quantum_error(
            error,
            ["h", "x", "z"]
        )

    elif noise_type == "Depolarizing":

        single_error = depolarizing_error(
            probability,
            1
        )

        two_qubit_error = depolarizing_error(
            probability,
            2
        )

        noise_model.add_all_qubit_quantum_error(
            single_error,
            ["h", "x", "z"]
        )

        noise_model.add_all_qubit_quantum_error(
            two_qubit_error,
            ["cx"]
        )

    return noise_model


def run_noisy_circuit(
    circuit,
    noise_type,
    probability,
    shots=1024
):

    # Start with an unmeasured circuit
    noisy_circuit = circuit.copy()

    # Create noise
    noise_model = create_noise_model(
        noise_type,
        probability
    )

    # Measurement is added only once
    noisy_circuit.measure_all()

    simulator = AerSimulator(
        noise_model=noise_model
    )

    compiled_circuit = transpile(
        noisy_circuit,
        simulator
    )

    result = simulator.run(
        compiled_circuit,
        shots=shots
    ).result()

    raw_counts = result.get_counts()

    counts = convert_counts(raw_counts)

    return add_all_states(counts)


def transmit_message(
    message,
    shots=1024
):

    # Keep this circuit unmeasured
    circuit = create_superdense_circuit(
        message,
        measure=False
    )

    # Determine encoding operation
    if message == "00":

        operation = "I (No operation)"

    elif message == "01":

        operation = "X gate"

    elif message == "10":

        operation = "Z gate"

    elif message == "11":

        operation = "X + Z gates"

    else:

        raise ValueError(
            "Message must be 00, 01, 10, or 11."
        )

    # Create separate circuit for ideal measurement
    measured_circuit = circuit.copy()

    measured_circuit.measure_all()

    counts = run_circuit(
        measured_circuit,
        shots
    )

    received_message = max(
        counts,
        key=counts.get
    )

    return (
        circuit,
        counts,
        received_message,
        operation
    )