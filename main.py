from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler


def superdense_coding(message):
    qc = QuantumCircuit(2)

    # Step 1: Create Bell state
    qc.h(0)
    qc.cx(0, 1)

    # Step 2: Alice encodes the message
    if message == "01":
        qc.z(0)

    elif message == "10":
        qc.x(0)

    elif message == "11":
        qc.x(0)
        qc.z(0)

    if message == "00":

        st.latex(
            r"I|\Phi^+\rangle = |\Phi^+\rangle"
        )

    elif message == "01":

        st.latex(
            r"X|\Phi^+\rangle = |\Psi^+\rangle"
        )

    elif message == "10":

        st.latex(
            r"Z|\Phi^+\rangle = |\Phi^-\rangle"
        )

    elif message == "11":

        st.latex(
            r"XZ|\Phi^+\rangle = |\Psi^-\rangle"
        )

    # Step 3: Bob decodes
    qc.cx(0, 1)
    qc.h(0)

    # Step 4: Measure
    qc.measure_all()

    return qc


def run_test(message):
    circuit = superdense_coding(message)

    sampler = StatevectorSampler()

    result = sampler.run(
        [circuit],
        shots=1024
    ).result()

    counts = result[0].data.meas.get_counts()

    # Find the measurement result with the highest count
    received = max(counts, key=counts.get)

    return received, counts


# Test all possible 2-bit messages
messages = ["00", "01", "10", "11"]

print("\n===== SUPERDENSE CODING TEST =====\n")

all_passed = True

for message in messages:

    received, counts = run_test(message)

    if received == message:
        status = "PASS ✓"
    else:
        status = "FAIL ✗"
        all_passed = False

    print(f"Alice sent : {message}")
    print(f"Bob received: {received}")
    print(f"Results     : {counts}")
    print(f"Status      : {status}")
    print("-" * 40)


if all_passed:
    print("\n🎉 ALL TESTS PASSED!")
else:
    print("\n❌ SOME TESTS FAILED!")