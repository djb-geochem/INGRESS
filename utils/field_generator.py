#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 18:03:49 2025

@author: user
"""
import sys
import numpy as np
import gstools as gs
import matplotlib.pyplot as plt

def variogram(nx, nz, var=1, len_scale=1e3, anis=1e-2):
    
    model = gs.Exponential(dim=2, var=var,
                           len_scale=len_scale, anis=anis) 
    
    x = range(nx)
    z = range(nz)
    
    field = gs.SRF(model)#, seed=19921026)
    
    Y = field((x, z), mesh_type="structured")
    
    return Y

def porosity_field(Y, avg_phi=0.05):
    
    phi = avg_phi * np.exp(Y)
    
    return phi

def calcite_field(Y, avg_calc=0.01, alpha=0.05, noise=0.01):
    
    calc = avg_calc + alpha * (-Y) + noise*np.random.randn(*Y.shape)
    
    return calc

def main(nx, nz):
    
    vgm = variogram(nx, nz)
    
    phi = porosity_field(vgm)
    
    calc = calcite_field(vgm)
    
    return phi.transpose(), calc.transpose()

if __name__ == "__main__":
    
    nx = sys.argv[1]
    nz = sys.argv[2]
    
    main(nx, nz)
#%%
phi, calc = main(100, 100)

fig = plt.figure()

ax1 = fig.add_subplot(121)

ax1.imshow(phi)

ax2 = fig.add_subplot(122)

ax2.imshow(calc)

    
    
    
