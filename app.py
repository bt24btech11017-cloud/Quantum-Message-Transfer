import streamlit as st

from quantum.superdense import (
    transmit_message,
    run_noisy_circuit
)


st.set_page_config(
    page_title="Quantum Message Transfer",
    page_icon="⚛️",
    layout="wide"
)


st.title("⚛️ Quantum Message Transfer")

st.markdown(
    """
### Superdense Coding Simulator

Send **2 classical bits using 1 qubit** and a pre-shared
entangled pair.
"""
)

st.divider()

st.subheader("📨 Alice's Message")

message = st.radio(
    "Select a 2-bit message:",
    ["00", "01", "10", "11"],
    horizontal=True
)


# Create circuit
circuit, ideal_counts, ideal_received, operation = transmit_message(
    message
)


st.divider()


if st.button(
    "🚀 Transmit Message",
    use_container_width=True
):

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Alice Sent",
            message
        )

    with col2:
        st.metric(
            "Bob Received",
            ideal_received
        )

    with col3:

        if message == ideal_received:
            st.success("✓ Successful")
        else:
            st.error("✗ Failed")


    st.divider()

    st.subheader("🔬 Quantum Circuit")

    st.code(
        str(circuit.draw(output="text")),
        language="text"
    )


    st.divider()

    st.subheader("📊 Measurement Results")

    all_states = ["00", "01", "10", "11"]

    measurement_results = {
        state: ideal_counts.get(state, 0)
        for state in all_states
    }

    st.bar_chart(measurement_results)

    st.write(
        f"Total measurements: **{sum(measurement_results.values())}**"
    )

    total = sum(
        ideal_counts.values()
    )

    st.write(
        f"Total measurements: **{total}**"
    )


    st.divider()

    st.subheader("🧠 Quantum State Evolution")

    st.write(
        "The protocol creates entanglement, encodes the "
        "message, and then decodes it."
    )


    st.markdown("### Step 1 — Initial State")

    st.latex(
        r"|00\rangle"
    )

    st.write(
        "Both qubits start in the state |00⟩."
    )


    st.markdown("### Step 2 — Superposition")

    st.latex(
        r"\frac{|00\rangle + |10\rangle}{\sqrt{2}}"
    )

    st.write(
        "Hadamard H is applied to Alice's qubit."
    )


    st.markdown("### Step 3 — Entanglement")

    st.latex(
        r"\frac{|00\rangle + |11\rangle}{\sqrt{2}}"
    )

    st.write(
        "CNOT creates the Bell state |Φ⁺⟩."
    )

    st.latex(
        r"|\Phi^+\rangle = "
        r"\frac{|00\rangle + |11\rangle}{\sqrt{2}}"
    )


    st.markdown("### Step 4 — Alice Encodes")

    st.write(
        f"Alice wants to send: **{message}**"
    )

    st.write(
        f"Alice applies: **{operation}**"
    )

    st.markdown(
        """
| Message | Operation | Bell State |
|:---:|:---:|:---:|
| `00` | I | Φ⁺ |
| `01` | X | Ψ⁺ |
| `10` | Z | Φ⁻ |
| `11` | X + Z | Ψ⁻ |
"""
    )


    if message == "00":

        st.latex(
            r"I|\Phi^+\rangle = |\Phi^+\rangle"
        )

        st.latex(
            r"\frac{|00\rangle + |11\rangle}{\sqrt{2}}"
        )


    elif message == "01":

        st.latex(
            r"X|\Phi^+\rangle = |\Psi^+\rangle"
        )

        st.latex(
            r"\frac{|01\rangle + |10\rangle}{\sqrt{2}}"
        )


    elif message == "10":

        st.latex(
            r"Z|\Phi^+\rangle = |\Phi^-\rangle"
        )

        st.latex(
            r"\frac{|00\rangle - |11\rangle}{\sqrt{2}}"
        )


    elif message == "11":

        st.latex(
            r"XZ|\Phi^+\rangle = |\Psi^-\rangle"
        )

        st.latex(
            r"\frac{|01\rangle - |10\rangle}{\sqrt{2}}"
        )


    st.markdown("### Step 5 — Bob Decodes")

    st.write(
        "Alice sends her qubit to Bob. Bob now has both qubits."
    )

    st.latex(
        r"CNOT \rightarrow H"
    )

    st.write(
        "These operations convert the Bell state back into "
        "a computational basis state."
    )


    st.markdown("### Step 6 — Measurement")

    st.write(
        f"Bob measures the qubits and receives: "
        f"**{ideal_received}**"
    )

    if message == ideal_received:

        st.success(
            f"✓ Alice's message {message} was successfully "
            f"decoded as {ideal_received}."
        )

    else:

        st.error(
            f"✗ Alice sent {message}, but Bob received "
            f"{ideal_received}."
        )


st.divider()


# Noise Analysis

st.header("⚠️ Noise Analysis")

st.write(
    "Real quantum computers are affected by noise. "
    "This simulation shows how noise changes the "
    "measurement results."
)


col1, col2 = st.columns(2)


with col1:

    noise_type = st.selectbox(
        "Select noise model:",
        [
            "Bit Flip",
            "Phase Flip",
            "Depolarizing"
        ]
    )


with col2:

    noise_probability_percent = st.slider(
        "Noise probability:",
        min_value=0,
        max_value=30,
        value=5,
        step=1,
        format="%d%%"
    )


noise_probability = (
    noise_probability_percent / 100
)


shots = st.number_input(
    "Number of noisy measurements:",
    min_value=100,
    max_value=5000,
    value=1024,
    step=100
)


if st.button(
    "🔬 Run Noise Analysis",
    use_container_width=True
):

    noisy_counts = run_noisy_circuit(
        circuit,
        noise_type,
        noise_probability,
        shots
    )


    st.subheader("📊 Noisy Measurement Results")

    st.bar_chart(noisy_counts)


    total_noisy = sum(
        noisy_counts.values()
    )


    correct_count = noisy_counts.get(
        message,
        0
    )


    success_rate = (
        correct_count / total_noisy
    ) * 100


    error_rate = (
        100 - success_rate
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Expected Result",
            message
        )


    with col2:

        st.metric(
            "Success Rate",
            f"{success_rate:.2f}%"
        )


    with col3:

        st.metric(
            "Error Rate",
            f"{error_rate:.2f}%"
        )


    st.divider()


    st.subheader("📈 Ideal vs Noisy")


    comparison = {
        "Ideal": ideal_counts.get(
            message,
            0
        ),
        "Noisy": noisy_counts.get(
            message,
            0
        )
    }


    st.bar_chart(comparison)


    st.write(
        f"With **{noise_probability_percent}% "
        f"{noise_type.lower()} noise**, Bob correctly "
        f"received `{message}` in **{correct_count} "
        f"out of {total_noisy} measurements**."
    )


    st.info(
        "Increasing the noise probability generally "
        "increases the probability of an incorrect "
        "measurement."
    )