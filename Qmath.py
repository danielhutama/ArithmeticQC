# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 13:35:15 2022

@author: Daniel Hutama
"""
import numpy as np

from qiskit import *





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


def get_binary_LSB_to_MSB(num):
    return np.binary_repr(num)[::-1]

######### example n=10 ##########

def run_example():
    # initialize 10 qubit system
    # QR = QuantumRegister(10)
    A = QuantumRegister(3, 'a')
    B = QuantumRegister(3, 'b')
    C = QuantumRegister(4, 'c')
    
    QR_circ = QuantumCircuit(A, B, C)
    
    QR_circ.append(CARRY, [C[0], A[0], B[0], C[1]])
    QR_circ.append(CARRY, [C[1], A[1], B[1], C[2]])
    QR_circ.append(CARRY, [C[2], A[2], B[2], C[3]])
    QR_circ.cx(A[2], B[2])
    QR_circ.append(SUM, [C[2], A[2], B[2]])
    QR_circ.append(rCARRY, [C[1], A[1], B[1], C[2]])
    QR_circ.append(SUM, [C[1], A[1], B[1]])
    QR_circ.append(rCARRY, [C[0], A[0], B[0], C[1]])
    QR_circ.append(SUM, [C[0], A[0], B[0]])
        
    
    # QR_circ.append(CARRY, [QR[0], QR[1], QR[2], QR[3]])
    # QR_circ.append(CARRY, [QR[3], QR[4], QR[5], QR[6]])
    # QR_circ.append(CARRY, [QR[6], QR[7], QR[8], QR[9]])
    # QR_circ.cx(QR[7], QR[8])
    # QR_circ.append(SUM, [QR[6], QR[7], QR[8]])
    # QR_circ.append(rCARRY, [QR[3], QR[4], QR[5], QR[6]])
    # QR_circ.append(SUM, [QR[3], QR[4], QR[5]])
    # QR_circ.append(rCARRY, [QR[0], QR[1], QR[2], QR[3]])
    # QR_circ.append(SUM, [QR[0], QR[1], QR[2]])
    
    return QR_circ.draw(fold=-1)

