def runQCTests_and_metrics(qc, mode, title = "Simulated data vs real data", retain_previous_job = False):
    from IPython.display import display
    from qiskit.visualization import plot_histogram
    from qiskit import transpile
    from qiskit_ibm_runtime import QiskitRuntimeService
    # from qiskit.converters import circuit_to_dag
    from qiskit.primitives import StatevectorSampler
    from qiskit_ibm_runtime import Sampler

    import sys
    sys.path.insert(1, '../Reproduced_circuits')
    from common import print_metrics

    import os
    from time import sleep

    print("Quantum circuit being evaluated:  ")
    display(qc.draw("mpl"))


    #Simulation

    samplerSim = StatevectorSampler()
    # result = samplerSim.run([qc], shots=(1024*4)).result()
    result = samplerSim.run([qc], shots=(2**11)).result()

    counts = result[0].data.classicalRegister.get_counts()
    pretty_sim_counts = {}

    for bitstring, count in counts.items():
        carry = bitstring[0]
        sum_bits = bitstring[1:]
        if(mode == "add"):
            sum = int(bitstring, 2)

            label = f"carry={carry}, sum bits={sum_bits}, sum result={sum}"
            pretty_sim_counts[label] = count
        elif(mode == "sub"):
            sub = int(bitstring[1:], 2)

            label = f"carry={carry}, sub bits={sum_bits}, sub result={sub}"
            pretty_sim_counts[label] = count
        else:
            prod_bits = bitstring
            label = f"product bits={prod_bits}, Product={int(bitstring,2)}"
            pretty_sim_counts[label] = count


        #comment if its in dist. mode
        # print(bitstring, "→",
        #     "carry =",     bitstring[0],
        #     "sum bits =", bitstring[1:],
        #     "Result =", int(bitstring, 2))
    
    #Hardware
    backUp = f"Latest_{title}_job_id.txt" #prepping this in the case that i want to rerun a circuit without having to make a new job


    service = QiskitRuntimeService()
    backend_name = "ibm_kingston"
    backend = service.backend(backend_name)


    try:
        print("Searching for retained job ID...\n")
        with open(backUp, "r") as file:
            job_id = file.read()
            job = service.job(job_id) 
            print("Found job ID\n")

    except:
        print("Retained job ID not found, launching a new one...\n")
        # backend_name = "ibm_marrakesh"


        qc_transpiled = transpile(qc, backend=backend, optimization_level=0)
        print("Transpiled the qc and got the backend")


        # print("Transpiled qc: ")
        # display(qc_transpiled.draw("mpl"))
        #DO NOT DO THIS^^^^^. MY COMPUTER COULD NOT HANDLE IT



        sampler = Sampler(mode=backend)
        sampler.options.default_shots = 2**11
        job = sampler.run([qc_transpiled])
        # job = sampler.job("d9bojpu6hjac73fg0cpg")
        print(f"job_id: {job.job_id()}")
        with open(backUp, "x", encoding="utf-8") as f:
            f.write(job.job_id())


        #check if there is a func that tells you if the job is done
        # not needed, job.result() will wait until the job is done
        while(job.status() != "DONE"):
            print(job.status(), flush=True)
            sleep(30)
            continue
    print(f"Job metrics: {job.metrics()}\n")
    print(f"Job duration: {job.metrics()["usage"]}")

    real_result = job.result()
    Real_counts = real_result[0].data.classicalRegister.get_counts()

    pretty_real_counts = {}

    for bitstring, count in Real_counts.items():
        carry = bitstring[0]
        sum_bits = bitstring[1:]
        if(mode == "add"):
            sum = int(bitstring, 2)

            label = f"carry={carry}, sum bits={sum_bits}, sum result={sum}"
            pretty_real_counts[label] = count
        elif(mode == "sub"):
            sub = int(bitstring[1:], 2)

            label = f"carry={carry}, sub bits={sum_bits}, sub result={sub}"
            pretty_real_counts[label] = count
        else:
            prod_bits = bitstring
            label = f"product bits={prod_bits}, Product={int(bitstring,2)}"
            pretty_real_counts[label] = count

        #comment if its in dist. mode
        # print(bitstring, "→",
        #     "carry =",     bitstring[0],
        #     "sum bits =", bitstring[1:],
        #     "Result =", int(bitstring, 2))
        

    SimData = plot_histogram(pretty_sim_counts, title="Simulated quantum cirucit'")

    RealData = plot_histogram(pretty_real_counts, title="Experimental quantum cirucit", color= "red")

    bothDatas = plot_histogram([pretty_sim_counts, pretty_real_counts], legend=["Simulated data", "Real data"], title = title, color=["blue", "red"],bar_labels=False)

    display(SimData, RealData, bothDatas)
    print("\n")


    # print("\nQuantum Circuit metric vs transpiled quantum circuit's metrics")

    # print(f"og quantum cirucit's depth: {qc.depth()}")
    # print(f"transpiled 4-bit quantum cirucit''s depth: {qc_transpiled.depth()}\n")
    # print("Meassuring quantum circuit's T-depth")
    # decomposed = transpile(qc, basis_gates=['cx', 'h', 't', 'tdg', 's', 'sdg'])


    # dag = circuit_to_dag(decomposed)

    # t_depth = 0
    # for layer in dag.layers():
    #     if any(node.name in ['t', 'tdg'] for node in layer['graph'].op_nodes()):
    #         t_depth += 1

    print("Quantum cicuit's metrics:\n")
    print_metrics(qc)

    print("\nHardware metrics:\n")

    dic = (backend.properties().qubits[0][0].to_dict())

    for metric in backend.properties().qubits[0]:
        dic = metric.to_dict()

        print(f"Name of metric: {dic["name"]}")
        if(dic["unit"] != ""):
            print(f"Name of unit used for metric: {dic["unit"]}")
        print(f"Value of metric: {dic["value"]}\n")
        print("-"*40,"\n")
    if(retain_previous_job == False):
        os.remove(backUp) #remove in the end if we are not retaining 
