from typing import Callable
from dotenv import load_dotenv
import os
from IPython.display import display
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.quantum_info import Statevector
from qiskit.primitives import StatevectorSampler
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime import SamplerV2
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.circuit.library import CCXGate
import networkx as nx

load_dotenv()
QiskitRuntimeService.save_account(
    token=os.getenv("IBM_QUANTUM_API_KEY"),
    overwrite=True,
    instance="crn:v1:bluemix:public:quantum-computing:us-east:a/84cc656cc21646d2a0c535460b576f20:ae6b1949-8eb9-4aaf-9212-f71fef3141d3::"
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

def test_circuit(qc: QuantumCircuit, a_values: list[int], a_register: QuantumRegister, b_values: list[int], b_register: QuantumRegister, all_registers: list[QuantumRegister], expected_answer: Callable[[int, int], int], answer_range: tuple[int, int]):
    count_wrong = 0
    count_total = 0
    wrongs = []
    for a_value in a_values:
        for b_value in b_values:
            count_total += 1
            answer = get_answer(qc, a_value, a_register, b_value, b_register, all_registers, qc.qubits, [answer_range])[0]
            expected = expected_answer(a_value, b_value)
            if answer != expected:
                count_wrong += 1
                wrongs.append((a_value, b_value, answer, expected))
                print(f"Error: {a_value}, {b_value}: got {answer}, expected {expected}")
    print("Total wrongs:", count_wrong)
    print("Total tests:", count_total)
    for a_value, b_value, answer, expected in wrongs:
        print(f"  {a_value}, {b_value}: got {answer}, expected {expected}")

def debug_circuit(qc):
    state = Statevector([1] + [0] * (2 ** qc.num_qubits - 1))
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
    print("\nFinal Statevector:")
    print(state)
    print("Probabilities:")
    for basis_state, amplitude in state.probabilities_dict().items():
        print(f"{basis_state}: {amplitude:.4f}")

basis_gates = ["h", "s", "cx", "t"]
is_toffoli = lambda inst: inst.name == "ccx" or isinstance(inst, CCXGate)
is_t_gate = lambda inst: inst.name == "t"
is_cz_gate = lambda inst: inst.name == "cz"

def multi_qubit_interaction_graph(circuit):
    import networkx as nx

    G = nx.Graph()

    for i in range(circuit.num_qubits):
        G.add_node(i)

    for inst in circuit.data:
        if len(inst.qubits) < 2:
            continue

        indices = [circuit.find_bit(q).index for q in inst.qubits]

        for i in range(len(indices)):
            for j in range(i + 1, len(indices)):
                G.add_edge(indices[i], indices[j])

    return G

def print_metrics(qc: QuantumCircuit):
    isa_qc = pm.run(qc)
    graph = multi_qubit_interaction_graph(qc)
    clifford_t_qc = transpile(
        qc,
        basis_gates=["h", "s", "cx", "t"],
        optimization_level=3
    )
    print("Size:", qc.size())
    print("Toffoli count:", qc.size(is_toffoli))
    print("CZ count:", isa_qc.size(is_cz_gate))
    print("T count:", clifford_t_qc.size(is_t_gate))
    print("Depth:", qc.depth())
    print("Toffoli depth:", qc.depth(is_toffoli))
    print("CZ depth:", isa_qc.depth(is_cz_gate))
    print("T depth:", clifford_t_qc.depth(is_t_gate))
    print("Width:", qc.width())
    print("Algebraic connectivity:", nx.algebraic_connectivity(graph))

def inspect_results(job, expected):
    result = job.result()[0]
    counts = result.data.meas.get_counts()
    num_top_results = 10
    print(f"Top {num_top_results} results:")
    top = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True)[:num_top_results])
    print(top)
    num_shots = sum(counts.values())
    print("Number of keys:", len(counts))
    print("Number of shots:", num_shots)
    print(f"Expected result {expected}: {counts[expected]}")
    print(f"Probability: {counts[expected] / num_shots:.4f}")
    display(plot_histogram(counts, title=f"Top {num_top_results} results"))