# RESULTS
## Explanation
Hardware specific circuits:
- Requested metrics
	- Layer Fidelity / Layered Gate Error
		- Fidelity
			- A measure of distance between quantum states (Mike & Ike)
			- Randomized benchmarking
				- Apply random clifford gates, apply their inverse, check how close to original state result is
			- Perform it with x = number of layers and y = error rate and fit exponential decay
			- A measurement of quality of some quantum computer
			- [Updating how we measure quantum quality and speed | IBM Quantum Computing Blog](https://www.ibm.com/quantum/blog/quantum-metric-layer-fidelity)
		- EPLG
			- Evaluates a quantum device
			- Similar or equal to fidelity
			- [EPLG - QuantumBenchmarkZoo](https://quantumbenchmarkzoo.org/content/system-level-benchmark/randomized-benchmarking/eplg)
	- Coherence times
		- Energy relaxation and dephasing time
		- Measure of device's qubit
	- Logical error rate
		- [IQM Academy - Learn Quantum Computing Online](https://www.iqmacademy.com/learn/qec2/04-logical-error-rate/)
		- Applied to an error correction code

Circuit specific metrics:
- \# Accurate circuits: When testing all possible inputs, how many outputs from the circuit are the expected result.
- Test run: Experimental run with some test input
	- Input: Input 1 and Input 2 = Expected output
	- Logical accuracy: How many shots resulted in the expected output
	- Logical fidelity: If the correct output was the most common one, how it compares with the second most common one. If not, its rank among all common outputs.
- Requested metrics
	- Algebraic connectivity
		- "Returns the algebraic connectivity of an undirected graph. The algebraic connectivity of a connected undirected graph is the second smallest eigenvalue of its Laplacian matrix." ([NetworkX](https://networkx.org/documentation/stable/reference/generated/networkx.linalg.algebraicconnectivity.algebraic_connectivity.html))
		- Refers to connectivity between qubits in a circuit
		- The graph that defines which qubits connect to which other qubits
		- [Definitions of a quantum circuit's depth and connectivity - Quantum Computing Stack Exchange](https://quantumcomputing.stackexchange.com/questions/26804/definitions-of-a-quantum-circuits-depth-and-connectivity)
	- T-count
		- Amount of T gates in the circuit as *as transpiled to the Clifford+T basis*, {H, S, CNOT, T}. Transpiled with optimization level 3.
		- T gate
			- Phase shift gate, rotates by pi/4
			- "T gates are complex and costly" (Wang)
		- "\[Toffoli-Count] can be converted to T-count using specific decomposition methods for standardized comparisons." (Wang)
	- T-depth
		- Depth when only considering T-gates in the circuit as *as transpiled to the Clifford+T basis*, {H, S, CNOT, T}. Transpiled with optimization level 3.
		- "The depth of a circuit is the length of the longest [directed path](https://en.wikipedia.org/wiki/Directed_path "Directed path") from an input node to the output node." (Wikipedia)
		- "Toffoli-Depth can be converted to T-depth using specific decomposition methods" (Wang)
		- [QuantumCircuit (latest version) \| IBM Quantum Documentation](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.QuantumCircuit#depth)
- Other metrics
	- Depth
		- Circuit depth, as given by `.depth()`
	- Toffoli depth
		- Depth when only counting Toffoli gates ([Wang](https://arxiv.org/html/2406.03867v1))
	- CZ-count
		- Depth when only considering CZ gates in the circuit *as transpiled to the Heron r2 QPU*, in other words, circuit built using the {SX, RZ, CZ} basis.
	- Count
		- Amount of gates in circuit, as given by `.size()`
	- Toffoli count
		- Amount of Toffoli gates
	- CZ-count
		- Amount of CZ gates in the circuit *as transpiled to the Heron r2 QPU*, in other words, circuit built using the {SX, RZ, CZ} basis.
	- Width
		- Amount of qubits used, including inputs and ancillas, as given by `.width()`

## Addition
### Without input carry
- \# Accurate circuits: 232 / 256 (91%)
- Test run
	- Input: 0001 + 0001 = 0010
	- Accuracy: 772 / 2048 (38%)
	- Fidelity: 226 2nd / 772 1st (29%)
- Requested metrics
	- Algebraic connectivity: 0.262
	- T-count: 84
	- T-depth: 20
- Other metrics
	- Depth: 9
	- Toffoli depth: 5
	- CZ-depth: 87
	- Count: 28
	- Toffoli count: 12
	- CZ-count: 195
	- Width: 17

### With input carry
- \# Accurate circuits: 112 / 256 (44%)

## Subtraction
- \# Accurate circuits: 128 / 136 (94%) **MIGHT BE A BUG IN TESTER**
- Test run
	- Input: 0010 - 0001 = 0010
	- Accuracy: 417 / 2048 (20%)
	- Fidelity: 250 2nd / 417 1st (60%)
- Requested metrics
	- Algebraic connectivity: 0.262
	- T-count: 84
	- T-depth: 20
- Other metrics
	- Depth: 11
	- Toffoli depth: 5
	- CZ-depth: 81
	- Count: 37
	- Toffoli count: 12
	- CZ-count: 201
	- Width: 17

## Multiplication
- \# Accurate circuits: Unavailable, couldn't run test to completion. To do: take a statistically representative sample.
- Test run
	- Input: 011 × 011 = 001001
	- Accuracy: 601 / 32768 (1.8%)
	- Fidelity: 15th place
- Requested metrics
	- Algebraic connectivity: 0.423
	- T-count: 231
	- T-depth: 100
- Other metrics
	- Depth: 27
	- Toffoli depth: 5
	- CZ-depth: 470
	- Count: 35
	- Toffoli count: 9
	- CZ-count: 668
	- Width: 26

## Division
- \# Accurate circuits: 100%
- Test run
	- Garbage results
- Requested metrics
	- Algebraic connectivity: 3.452
	- T-count: 504
	- T-depth: 280
- Other metrics
	- Depth: 87
	- Toffoli depth: 40
	- CZ-depth: 1005
	- Count: 152
	- Toffoli count: 40
	- CZ-count: 1281
	- Width: 13