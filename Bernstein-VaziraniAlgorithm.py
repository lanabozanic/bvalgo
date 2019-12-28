#Import Libraries
from qiskit import *
from qiskit.visualization import plot_histogram

get_ipython().run_line_magic('matplotlib', 'inline')

#Secret bitstring we're trying to find
secret = '10001101'

circuit = QuantumCircuit(len(secret)+1, len(secret))

#put a hadamard on every gate (except the last one)
circuit.h(range(len(secret)))
  
#apply a Pauil X (quantum NOT) and a hadamard on the last qubit (for phase kickback)
circuit.x(len(secret))          
circuit.h(len(secret))

circuit.barrier()

#for ever 1 in the bitstring, apply a CNOT
for i, x in enumerate(reversed(secret)):
    if x == '1':
        circuit.cx(i, len(secret))

#for visualization purposes
circuit.barrier()

#re-hadamard all the gates. Every superposition |- > becomes 1 and everyone |+ > becomes 0
circuit.h(range(len(secret)))

#for visualization purposes
circuit.barrier()

#measure and store results
circuit.measure(range(len(secret)), range(len(secret)))

#draw the circuit
circuit.draw(output='mpl')

#run the code on a simulator
sim = Aer.get_backend('qasm_simulator')
results = execute(circuit, backend=sim, shots=1).result()
counts = results.get_counts()
print(counts)
