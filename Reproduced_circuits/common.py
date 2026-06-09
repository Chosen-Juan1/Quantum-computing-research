from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import Statevector
from qiskit.primitives import StatevectorSampler
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime import SamplerV2
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.circuit.library import HalfAdderGate
from dotenv import load_dotenv
import os
load_dotenv()
os.getenv("IBM_QUANTUM_API_KEY")

QiskitRuntimeService.save_account(
    token=os.getenv("IBM_QUANTUM_API_KEY"),
    overwrite=True
)

from qiskit.transpiler import generate_preset_pass_manager

service = QiskitRuntimeService()
backend = service.least_busy(simulator=False, operational=True)
pm = generate_preset_pass_manager(backend=backend, optimization_level=1)

sv_sampler = StatevectorSampler()
backend_sampler = SamplerV2(mode=backend)

def extract_state(qc) -> str:
    state = Statevector.from_instruction(qc)
    return str(list(state.probabilities_dict().keys())[0]) # Simulation is exact

# Test rigurously
def get_answer(circuit, a_val, a_reg, b_val, b_reg, all_regs, qubits, answer_ranges):
    qc = QuantumCircuit(*all_regs)
    for i in range(4):
        if (a_val >> i) & 1:
            qc.x(a_reg[i])
        if (b_val >> i) & 1:
            qc.x(b_reg[i])
    print(f"Initial state: {extract_state(qc)}")
    qc.append(circuit, qubits)
    bitstr = extract_state(qc)
    print(f"Final state:   {bitstr}")
    return tuple(int(bitstr[a_range[0]:a_range[1]], 2) for a_range in answer_ranges)

def debug_circuit(qc):
    state = Statevector.from_instruction(qc)
    for instr in qc.data:
        # Stop before the measurement instruction
        if instr.name == 'measure':
            break
        
        print("Applying instruction:", instr)

        # Evolve the state with the current gate
        state = state.evolve(instr.operation, qargs=[qc.qubits.index(qubit) for qubit in instr.qubits])
        print(f"State after {instr.name}: {state}")
        print(f"Probabilities: {state.probabilities_dict()}\n")

    # --- 4. The 'state' variable now holds the intermediate state ---
    print("\nFinal Intermediate Statevector:")
    print(state)
    print("Probabilities:")
    for basis_state, amplitude in state.probabilities_dict().items():
        print(f"{basis_state}: {amplitude:.4f}")