#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 15:14:41 2025

@author: user
"""

import numpy as np

x = np.logspace(-1, np.log10(20e3), 101)

dx = np.diff(x)

with open("grid.txt", 'w') as writefile:
    
    for n, i in enumerate(dx):
        writefile.write(np.format_float_scientific(i, precision=8))
        writefile.write(" ")
        if (n+1)%5 == 0:
            writefile.write("\\")
            writefile.write("\n")
        
