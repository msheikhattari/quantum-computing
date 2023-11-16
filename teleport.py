from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer
from qiskit.quantum_info import random_statevector
from qiskit.extensions import Initialize
from qiskit.visualization import plot_bloch_multivector


def teleport(psi):
    #First we visualize psi so we can see what state is being teleported
    #saved to input_state.png
    plot_bloch_multivector(psi, filename="input_state")
    
    #Setup circuit and states
    states = QuantumRegister(3, name = "p")
    z = ClassicalRegister(1, name = "z")
    x = ClassicalRegister(1, name = "x")
    circuit = QuantumCircuit(states,z,x)
    
    #Initializing first qubit to psi, the state being teleported
    init_gate = Initialize(psi)
    init_gate.label = "Initialize"
    circuit.append(init_gate, [0])
    
    
    #Create the shared bell state in quantum registers 1 and 2
    #Add a H gate on qubit 1
    circuit.h(1)
    #Add a CX (CNOT) gate on control qubit 1 and target qubit 2
    circuit.cx(1, 2)
    
    
    #Sender applies Bell-basis measurement
    #CNOT is applied on control qubit 0 and target qubit 1
    circuit.cx(0, 1)
    #Hadamard is applied to qubit 0
    circuit.h(0)
    #The measurement is then made
    circuit.measure(0,0)
    circuit.measure(1,1)
    
    
    #Recipient then applies gates to their qubit based on measurment information
    circuit.x(2).c_if(x,1)
    circuit.z(2).c_if(z,1)
    
    print(circuit)
    
    
    #We then convert the circuit back into a statevector and visualize the qubits
    sim = Aer.get_backend('aer_simulator')
    circuit.save_statevector()
    out = sim.run(circuit).result().get_statevector()
    plot_bloch_multivector(out, filename="output_state")
    
psi = random_statevector(2)
teleport(psi)