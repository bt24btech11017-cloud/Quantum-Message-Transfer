<img width="1446" height="735" alt="image" src="https://github.com/user-attachments/assets/d63679ad-4926-44c5-8272-2492c353ef98" />
# ⚛️ Quantum Message Transfer

An interactive **Superdense Coding Simulator** built with Python, Qiskit, Qiskit Aer, and Streamlit.

The project demonstrates how **2 classical bits can be transmitted using only 1 qubit**, provided Alice and Bob share a pre-entangled Bell pair. It also simulates the effect of different types of quantum noise on the communication process.

---

## 🚀 Features

- Superdense coding simulation
- Bell-state generation
- Quantum superposition and entanglement
- Message encoding using X and Z gates
- CNOT and Hadamard-based decoding
- 1024-shot measurement simulation
- Measurement probability visualization
- Bit-flip noise simulation
- Phase-flip noise simulation
- Depolarizing noise simulation
- Ideal vs noisy result comparison
- Communication success and error rate calculation
- Interactive Streamlit interface

---

## 🧠 How Superdense Coding Works

Superdense coding allows Alice to send **2 classical bits using 1 qubit**, assuming Alice and Bob initially share an entangled Bell pair.

The protocol consists of four main stages:

```text
Create Bell State
      ↓
Alice Encodes Message
      ↓
Bob Decodes Message
      ↓
Measurement
