# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 13:35:15 2022

@author: danhu
"""
import numpy as np

from qiskit import *





class Qmath(n):
    def __init__(self, n):
        self.circuit = QuantumCircuit(n)
        self.SUM = self.SUM()
        self.CARRY = self.CARRY()
    
    def SUM(self):
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
        
        
    
    def multiplication():
        pass
    
    def mod_addition():
        pass 