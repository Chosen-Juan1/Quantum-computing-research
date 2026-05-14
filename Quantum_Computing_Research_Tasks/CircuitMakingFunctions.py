def makeFullAdder():
    from qiskit import QuantumCircuit
    # from qiskit.primitives import StatevectorSampler
    from qiskit.circuit import QuantumRegister, ClassicalRegister
    from qiskit.visualization import plot_histogram
    from qiskit.circuit.library import CCXGate, XGate, HGate, Reset, swap
    from qiskit.primitives import StatevectorSampler
    from IPython.display import display
    sampler = StatevectorSampler()

        
    #since these operations are from right to left, we iterate backwards:
        
    # cr = ClassicalRegister(5,"classicalRegister")

    qr0 = QuantumRegister(1,"Control 1")
    qr1 = QuantumRegister(1,"Control 2")
    qr2 = QuantumRegister(1,"A")
    qr3 = QuantumRegister(1,"B")
    qr4 = QuantumRegister(1,"Carry_in")
    qr5 = QuantumRegister(1,"Carry_out")
    qr6 = QuantumRegister(1,"Sum")
    qr7 = QuantumRegister(1,"Temp1")
    qr8 = QuantumRegister(1,"Temp2")
    qr9 = QuantumRegister(1,"Temp3")
    qr10 = QuantumRegister(1,"Sub?")
    qc = QuantumCircuit(qr0, qr1, qr2, qr3, qr4, qr5, qr6, qr7, qr8, qr9, qr10, name='Full-adder circuit')

    control_1 = 0
    control_2 = 1
    A = 2
    B = 3
    Carry_in = 4
    Carry_out = 5
    Sum = 6
    Temp1 = 7
    Temp2 = 8
    Temp3 = 9
    sub = 10
    #set up the SUM of the LSBs (least signigicant bits)
    #solve the sub(Control XOR B) into T2)
    qc.append(CCXGate(), [control_1, B, Temp3]) #*********
    qc.append(CCXGate(), [control_1, sub, Temp3]) #*********

    #First XOR (sum):
    #XOR A4 and T3 to fill T1
    qc.append(CCXGate(), [control_2,A,Temp1])
    #
    qc.append(CCXGate(), [control_2,Temp3,Temp1])

    #Perform XOR between the T1 and the carry to get the sum
        #Xor with T1
    qc.append(CCXGate(), [control_2,Temp1,Sum])

        #Xor with carry **** (unecessary?) *****************************************
    qc.append(CCXGate(), [control_2,Carry_in,Sum])

    #Sum between A4 and T3 is done


    #Carry for A4 and T3
        #AND between T1 and C-IN dumped into T2 ****
    qc.append(CCXGate(),[Carry_in,Temp1,Temp2])


        #now we clean T1 from the A4 XOR T3 operation
    qc.append(CCXGate(), [control_2,Temp3,Temp1])
    qc.append(CCXGate(), [control_2,A,Temp1])

        #AND between A4 and T3 into T1
    qc.append(CCXGate(),[A,Temp3,Temp1])

    #OR T1 and T2:
        #First, Not(T2)
    qc.append(CCXGate(), [control_1,control_2,Temp2])
        #Second, Not(T1)
    qc.append(CCXGate(), [control_1, control_2, Temp1])
    #And both T1 and T2 into carry bit 2 
    qc.append(CCXGate(), [Temp1, Temp2, Carry_out])
    #Finally, invert carry bit
    qc.append(CCXGate(), [control_1, control_2, Carry_out])

    #Or finished and Carry computed, clean T1 and T2
    # Since T2 was calculated using T1, we are going to have to rebuild that sucker back to the state it held before T2 was filled 

    #reverse the NOT and AND
        #the NOT
    qc.append(CCXGate(), [control_1, control_2, Temp1])

        #the and
    qc.append(CCXGate(), [A, Temp3, Temp1])

    #T1 should be back into its OG state, so now we recompute A XOR B
    qc.append(CCXGate(), [control_2,A,Temp1])
    qc.append(CCXGate(), [control_2,Temp3, Temp1])

    #undo NOT T2
    qc.append(CCXGate(), [control_1,control_2,Temp2])

    #UNDO T1 AND C_In
    qc.append(CCXGate(),[Carry_in,Temp1,Temp2])

    #T2 is now back to its og state, now clean T1 again
    qc.append(CCXGate(), [control_2,Temp3,Temp1])
    qc.append(CCXGate(), [control_2,A,Temp1])

    #undo carry_in XOR T3
    qc.append(CCXGate(), [control_1, sub, Temp3])
    qc.append(CCXGate(), [control_1, B, Temp3])

    adder_qc = qc.to_gate(label="4-bit Full adder/substractor")
    return adder_qc

def makeHalfAdder():
    from qiskit import QuantumCircuit
    from qiskit.circuit import QuantumRegister
    from qiskit.circuit.library import CCXGate
    #qiskit initializes qbits to |0>
    #qubits 0 and 1 are the so called ancellary(?) qbits, as in, they don't change
    qr = QuantumRegister(5,"q")
    control_1 = 0
    A = 1
    B = 2
    Sum = 3
    Carry = 4

    qc = QuantumCircuit(qr, name='half-adder circuit')

    #XOR (sum):

    qc.append(CCXGate(), [control_1,A,Sum])
    qc.append(CCXGate(), [control_1,B,Sum])


    #AND (Carry11):
    qc.append(CCXGate(), [A,B,Carry])

    half_adder_qc = qc.to_gate(label="Half-adder")
    return half_adder_qc
