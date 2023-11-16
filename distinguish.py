import numpy as np
import cmath

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.providers.aer import QasmSimulator

def distinguish(state):
    #Initialize the circuit
    states = QuantumRegister(3, name = "p")
    classical = ClassicalRegister(3, name = "b")
    circuit = QuantumCircuit(states,classical)
    #qubits initialized to passed in state
    circuit.initialize(state,states)

    #This is the inverse of the circuit that gets you to the W state, with 
    #added phase on the |010> and |001> states
    circuit.rz(-2.0*np.pi/3.0,1)
    circuit.rz(-4.0*np.pi/3.0,2)
    circuit.x(0)
    circuit.cx(0,1)
    circuit.cx(1,2)
    circuit.ch(0,1)
    circuit.ry(-2.0*np.arccos(1.0/np.sqrt(3.0)), 0)
    

    #Measurement results will tell us which state we were in.
    #If we had psi_0 this will return us to |000> with probability 1 since
    #it's the inverse of the the circuit used to get from |000> to psi_0
    circuit.measure(states,classical)
    
    #We perform 1000 simulations of the measurement to verify the consistency of
    #the results.
    simulator = QasmSimulator()
    compiled_circuit = transpile(circuit, simulator)
    job = simulator.run(compiled_circuit, shots=1000)
    result = job.result()
    counts = result.get_counts(compiled_circuit)
    
    #If we had psi_0 we are guaranteed to have only 1 measurment result even in 1000
    #iterations: |000>. Any other state will have a non-deterministic measurement outcome.
    #Note: The evaluation could be done in different ways, ex. checking whether outcome 
    #|000> was measured.
    
    if(len(counts) == 1):
        return 0
    else:
        return 1 

#psi_0 and psi_1 are prepared and passed in. We expect a result of 0 and 1 to be returned, respectively.
psi_0 = [0,cmath.exp(complex(0,2.0*np.pi/3.0))/np.sqrt(3),cmath.exp(complex(0,4.0*np.pi/3.0))/np.sqrt(3), 0, 1.0/np.sqrt(3),0,0,0 ]
psi_1 = [0,cmath.exp(complex(0,4.0*np.pi/3.0))/np.sqrt(3),cmath.exp(complex(0,2.0*np.pi/3.0))/np.sqrt(3), 0, 1.0/np.sqrt(3),0,0,0 ]

#We indeed returned 0, and then 1 as expected.
print(distinguish(psi_0) == 0)
print(distinguish(psi_1) == 1)

#As a final check, we repeat the process 100 more times and if we ever observe 
#results deviating from our expectations, we indicate this by printing "FAIL".
#This does not occur once in 100 iterations.
for i in range(100):
    if(distinguish(psi_0) != 0 or distinguish(psi_1) != 1):
        print("FAIL")