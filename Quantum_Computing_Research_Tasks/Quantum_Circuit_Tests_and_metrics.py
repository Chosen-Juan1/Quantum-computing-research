def runQCTests_and_metrics(qc, title = "Simulated data vs real data"):
    from IPython.display import display
    from qiskit.visualization import plot_histogram
    from qiskit import transpile
    from qiskit_ibm_runtime import QiskitRuntimeService
    from qiskit.converters import circuit_to_dag
    from qiskit.primitives import StatevectorSampler
    from qiskit_ibm_runtime import Sampler



    print("Quantum circuit (QC) being evaluated:  ")
    display(qc.draw("mpl"))


    #Simulation

    samplerSim = StatevectorSampler()
    result = samplerSim.run([qc], shots=(1024*4)).result()
    counts = result[0].data.classicalRegister.get_counts()
    pretty_sim_counts = {}

    for bitstring, count in counts.items():
        carry = bitstring[0]
        sum_bits = bitstring[1:]

        label = f"carry={carry}, sum={sum_bits}"
        pretty_sim_counts[label] = count

        #comment if its in dist. mode
        # print(bitstring, "→",
        #     "carry =",     bitstring[0],
        #     "sum bits =", bitstring[1:],
        #     "Result =", int(bitstring, 2))
    
    #Hardware

    backend_name = "ibm_kingston"
    service = QiskitRuntimeService()
    backend = service.backend(backend_name)

    qc_transpiled = transpile(qc, backend=backend, optimization_level=0)
    print("Transpiled qc and got the backend")


    # print("Transpiled qc: ")
    # display(qc_transpiled.draw("mpl"))
    #DO NOT DO THIS^^^^^. MY COMPUTER COULD NOT HANDLE IT



    sampler = Sampler(mode=backend)

    job = sampler.run([qc_transpiled])

    print(f"job_id: {job.job_id()}")
    #check if there is a func that tells you if the job is done

    while(job.status() != "DONE"):
        continue
    print(f"Job metrics: {job.metrics()}\n")
    print(f"Job duration {job.metrics()["usage"]}")

    real_result = job.result()
    Real_counts = real_result[0].data.classicalRegister.get_counts()

    pretty_real_counts = {}

    for bitstring, count in Real_counts.items():
        carry = bitstring[0]
        sum_bits = bitstring[1:]

        label = f"carry={carry}, sum={sum_bits}"
        pretty_real_counts[label] = count

        #comment if its in dist. mode
        # print(bitstring, "→",
        #     "carry =",     bitstring[0],
        #     "sum bits =", bitstring[1:],
        #     "Result =", int(bitstring, 2))
        

    SimData = plot_histogram(pretty_sim_counts, title="Simulated qc")

    RealData = plot_histogram(pretty_real_counts, title="Experimental qc", color= "red")

    bothDatas = plot_histogram([pretty_sim_counts, pretty_real_counts], legend=["Simulated data", "Real data"], title = title, color=["blue", "red"])

    display(SimData, RealData,bothDatas )
    print("\n")


    print("\nSimualted quantum ciruit depth vs transpiled quantum circuit's depth")

    print(f"og circuit's depth: {qc.depth()}")
    print(f"transpiled circuit's depth: {qc_transpiled.depth()}\n")
    print("Meassuring quantum circuit's T-depth")
    decomposed = transpile(qc, basis_gates=['cx', 'h', 't', 'tdg', 's', 'sdg'])


    dag = circuit_to_dag(decomposed)

    t_depth = 0
    for layer in dag.layers():
        if any(node.name in ['t', 'tdg'] for node in layer['graph'].op_nodes()):
            t_depth += 1

    print("T-depth:", t_depth)

    print("Hardware metrics\n")

    dic = (backend.properties().qubits[0][0].to_dict())

    for metric in backend.properties().qubits[0]:
        dic = metric.to_dict()

        print(f"Name of metric: {dic["name"]}")
        if(dic["unit"] != ""):
            print(f"Name of unit used for metric: {dic["unit"]}")
        print(f"Value of metric: {dic["value"]}\n")
        print("-"*40,"\n")
