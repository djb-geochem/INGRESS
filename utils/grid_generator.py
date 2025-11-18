#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 15:14:41 2025

@author: user
"""

import numpy as np

def generate_grid(nx, len_x=20e3):

    x = np.logspace(-1, np.log10(len_x), nx+1)
    
    dx = np.diff(x)
    
    return dx

def format_grid(dx):
    
    output = ["    "]
    
    for n, i in enumerate(dx):
        output.append(np.format_float_scientific(i, precision=8))
        output.append(" ")
        if (n+1)%5 == 0 and (n+1) != len(dx):
            output.append("\\\n    ")
    
    return ''.join(output)

