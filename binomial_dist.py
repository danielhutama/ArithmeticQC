# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 21:28:21 2022

@author: danhu
"""

import numpy as np 
import matplotlib.pyplot as plt
from scipy.stats import binom


# number of qubits
t = 3 

#bitspan
n = 2**t

#sharpness variable
p = 0.7

bin_vals = list(range(n))

dist = [binom.pmf(r,n,p) for r in bin_vals]

plt.bar(bin_vals, dist)
plt.show()