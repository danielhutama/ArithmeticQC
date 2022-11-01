# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 08:38:36 2022


This work is based off of Vlatko Vedral's paper on quantum arithmetic circuits. There is also a nice paper on my Github. 
The idea is to package the quantum ADDER into a module that dynamically adjust based on the input size.
This dynamic adjustability is necessary to stack multiple ADDERs together for the creation of a MOD ADDER.


@author: Daniel Hutama
email: dhuta087@uottawa.ca
"""
import numpy as np

from qiskit import *

from qiskit import Aer, transpile

from qiskit.providers.aer import QasmSimulator
from qiskit.visualization import plot_histogram

def SUM():
    qSum = QuantumRegister(3)
    qSum_circ = QuantumCircuit(qSum, name = 'SUM')
    qSum_circ.cx(qSum[1], qSum[2])
    qSum_circ.cx(qSum[0], qSum[2])
    return qSum_circ.to_instruction()

def CARRY():
    qCarry = QuantumRegister(4)
    qCarry_circ = QuantumCircuit(qCarry, name = 'CARRY')
    qCarry_circ.ccx(qCarry[1], qCarry[2], qCarry[3])
    qCarry_circ.cx(qCarry[1], qCarry[2])
    qCarry_circ.ccx(qCarry[0], qCarry[2], qCarry[3])
    return qCarry_circ.to_instruction()

def rCARRY():
    qrCarry = QuantumRegister(4)
    qrCarry_circ = QuantumCircuit(qrCarry, name = 'rCARRY')
    qrCarry_circ.ccx(qrCarry[0], qrCarry[2], qrCarry[3])    
    qrCarry_circ.cx(qrCarry[1], qrCarry[2])
    qrCarry_circ.ccx(qrCarry[1], qrCarry[2], qrCarry[3])
    return qrCarry_circ.to_instruction()
    
SUM = SUM()
CARRY = CARRY()
rCARRY = rCARRY()


def get_binary_LSB_to_MSB(num, size):
    return np.binary_repr(num, size)[::-1]



def ADDER(n):
    #2n+1 qubit needed
    
    # initialize registers for addition gate
    A = QuantumRegister(n, 'a')
    B = QuantumRegister(n+1, 'b')
    C = QuantumRegister(n, 'c')
    QR_circ = QuantumCircuit(A, B, C, name='ADDER')
    


    # cascaded CARRY gates
    for i in range(n-1):
        QR_circ.append(CARRY, [C[i], A[i], B[i], C[i+1]]) 
    # final CARRY gate
    QR_circ.append(CARRY, [C[n-1], A[n-1], B[n-1], B[n]]) 
    # single CNOT in ADDER system
    QR_circ.cx(A[n-1], B[n-1])
    
    # cascaded SUM and rCARRY
    for i in range(n-1):
        QR_circ.append(SUM, [C[n-1-i], A[n-1-i], B[n-1-i]])
        QR_circ.append(rCARRY, [C[n-2-i], A[n-2-i], B[n-2-i], C[n-1-i]])
    # final SUM
    QR_circ.append(SUM, [C[0], A[0], B[0]])
    return QR_circ.to_instruction()

 


n = 2
ADDER = ADDER(n)

# generate dictionaries - keys are the state buckets, values are the probabilities
a_dict = {}
a_dict_adj = {}
b_dict = {}
c_dict = {}

for i in range(2**n):
    a_dict[i] = 0
    c_dict[i] = 0

for i in range(2**(n+1)):
    b_dict[i] = 0
    a_dict_adj[i] = 0

# this should allow me to set initialization values by adjusting the keyed value based on the decimal representation of the bin.
a_dict[0] = np.sqrt(1/4)
a_dict[1] = np.sqrt(1/2)
a_dict[2] = np.sqrt(1/4)
a_dict[3] = 0
# a_dict[4] = 0
# a_dict[5] = 0
# a_dict[6] = 0
# a_dict[7] = 0

#for input state plot
a_dict_adj[0] = np.sqrt(1/4)
a_dict_adj[1] = np.sqrt(1/2)
a_dict_adj[2] = np.sqrt(1/4)
a_dict_adj[3] = 0
# a_dict_adj[4] = 0
# a_dict_adj[5] = 0
# a_dict_adj[6] = 0
# a_dict_adj[7] = 0

b_dict[0] = 0
b_dict[1] = np.sqrt(1/4)
b_dict[2] = np.sqrt(1/2)
b_dict[3] = np.sqrt(1/4)
b_dict[4] = 0
b_dict[5] = 0
b_dict[6] = 0
b_dict[7] = 0



a_init = list(a_dict.values())
b_init = list(b_dict.values())
c_init = list(c_dict.values())


execute = 1
trials = 10000
if execute == 1:
    
    # # initialize 10 qubit system
     A = QuantumRegister(n, 'a')        
     B = QuantumRegister(n+1, 'b')
     C = QuantumRegister(n, 'c')
    
     QR_circ = QuantumCircuit(A, B, C)
     c = QR_circ
     c.initialize(a_init, A)
     c.initialize(b_init, B)
     # c.initialize(c_init, C)
     
     enumerated_qbits = []
     # build list of target qbits for append function
     for i in range(n):
         enumerated_qbits.append(A[i])
     for i in range(n+1):
         enumerated_qbits.append(B[i])
     for i in range(n):
         enumerated_qbits.append(C[i])
     
     c.append(ADDER, enumerated_qbits)
     c.draw(fold=-1)
     
     c.measure_all()
    
     
     
     simulator = Aer.get_backend('aer_simulator')
     # simulator = QasmSimulator()
     c = transpile(c, simulator)
     result = simulator.run(c, shots = trials).result()
     counts = result.get_counts(c)
     # out = list(counts.keys())[0][::-1]
     
     counts_binary = {}
     for i in list(b_dict.keys()):
         counts_binary[np.binary_repr(i, n+1)] = 0
         
         
     for badkey in list(counts.keys()):
        counts_binary[badkey[n:2*n+1]] += counts[badkey]

counts_binary


plot_histogram(a_dict_adj)

plot_histogram(b_dict)

plot_histogram(counts_binary)



