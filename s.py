import tkinter as tk
from qiskit import QuantumCircuit, Aer, transpile
from qiskit.visualization import plot_histogram
from qiskit.providers.aer import AerSimulator
import random

# Constants
MIN_QUTRITS = 1
MAX_QUTRITS = 134

# Utility Functions
def initialize_circuit(num_qutrits):
    return QuantumCircuit(num_qutrits, num_qutrits)

def apply_random_gates(circuit, num_qutrits):
    gates = ['h', 's', 'y', 'cx', 'rng']
    for i in range(num_qutrits):
        gate = random.choice(gates)
        if gate == 'cx':
            target_qubits = random.sample(range(num_qutrits), 2)
            circuit.cx(target_qubits[0], target_qubits[1])
        elif gate == 'rng':
            circuit.rx(random.uniform(0, 2*3.14159), i)
        else:
            getattr(circuit, gate)(i)

def simulate_circuit(circuit):
    circuit.measure_all()  # Adds measurements to all qubits
    simulator = AerSimulator()
    compiled_circuit = transpile(circuit, simulator)
    result = simulator.run(compiled_circuit).result()
    counts = result.get_counts()
    plot_histogram(counts).show()


# GUI Functions
def run_simulation():
    num_qutrits = int(qutrit_entry.get())
    circuit = initialize_circuit(num_qutrits)
    apply_random_gates(circuit, num_qutrits)
    simulate_circuit(circuit)

# GUI Setup
root = tk.Tk()
root.title("Quantum Sandbox")

qutrit_label = tk.Label(root, text="Number of Qutrits:")
qutrit_label.pack()

qutrit_entry = tk.Entry(root)
qutrit_entry.insert(0, "1")
qutrit_entry.pack()

simulate_button = tk.Button(root, text="Simulate", command=run_simulation)
simulate_button.pack()

# Main Loop
root.mainloop()
