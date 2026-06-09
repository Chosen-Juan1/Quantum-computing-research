# RESULTS
## Explanation
- \# Accurate circuits: When testing all possible inputs, how many outputs from the circuit are the expected result.
- Test run: Experimental run with some test input
	- Input: Input 1 and Input 2 = Expected output
	- Accuracy: How many shots resulted in the expected output
	- Fidelity: If the correct output was the most common one, how it compares with the second most common one. If not, its rank among all common outputs.
- Requested metrics
	- Layer Fidelity
	- Coherence times
	- Connectivity
	- T-count
	- T-depth
	- Logical error rate

## Addition
- \# Accurate circuits: 232 / 256 (91%)
- Test run
	- Input: 0001 + 0001 = 0010
	- Accuracy: 772 / 2048 (38%)
	- Fidelity: 226 2nd / 772 1st (29%)
## Subtraction
- \# Accurate circuits:
- Test run
	- Input: 0010 - 0001 = 0010
	- Accuracy: 417 / 2048 (20%)
	- Fidelity: 250 2nd / 417 1st (60%)
## Multiplication
- \# Accurate circuits:
	- Input: 011 × 011 = 001001
	- Accuracy: 601 / 32768 (1.8%)
	- Fidelity: 15th place
## Division
- \# Accurate circuits: 100%
- Test run
	- Garbage results