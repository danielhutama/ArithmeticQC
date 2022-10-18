# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 13:35:15 2022

When I started writing this in March 2022, only God and myself knew how this uncommented code was structured.
Now, when you are reading this, only God knows and I have bareley an inkling of an idea. 
This works is based off of Vlatko Vedral's paper on quantum arithmetic circuits.

@author: Daniel Hutama

"""
import numpy as np

from qiskit import *

from qiskit import Aer, transpile



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


    


def ADDER(a, b, classical=True):
    #2n+1 qubit needed
    
    # initialize registers for addition gate
    A = QuantumRegister(n, 'a')
    B = QuantumRegister(n+1, 'b')
    C = QuantumRegister(n, 'c')
    QR_circ = QuantumCircuit(A, B, C, name='ADDER')
    

    if classical == True:
        #classical == True sets the registers to be in certain 0/1 states
        # i.e. I use Pauli X gates to set the states rather than any kind of partial phase rotations
        # encode a and b into LSB-first binary 
        if type(a) == str:
            pass
        else:
            a_bin = get_binary_LSB_to_MSB(a, n)
            for i in range(len(a_bin)):
                if a_bin[i] == '1':
                    QR_circ.x(A[i]) #only for testing (decimal argument passed)
        if type(b) == str:
            pass
        else:
            b_bin = get_binary_LSB_to_MSB(b, n+1)
            for i in range(len(b_bin)):
                if b_bin[i] == '1':
                    QR_circ.x(B[i])


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
