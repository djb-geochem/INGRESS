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

def variogram(nx, nz, var=0.1, len_scale=1e3, anis=1e-2):
    
    model = gs.Exponential(dim=2, var=var,
                           len_scale=len_scale, anis=anis) 
    
    x = range(nx)
    z = range(nz)
    
    field = gs.SRF(model)#, seed=19921026)
    
    Y = field((x, z), mesh_type="structured")
    
    return Y

def porosity_field(Y, avg_phi=0.05):
    
    phi = avg_phi * np.exp(Y)
    
    return np.clip(phi, 0.001, 0.2)

def calcite_field(Y, avg_calc=0.02, alpha=0.0005, len_scale_noise=200, anis=1e-2):
    # large-scale relation to Y (e.g. inverse correlation)
    base = avg_calc + alpha * (-Y)
    
    # small-scale correlated "noise"
    model_noise = gs.Exponential(dim=2, var=0.0001, len_scale=len_scale_noise, anis=anis)
    field_noise = gs.SRF(model_noise)
    
    nx, nz = Y.shape
    x = range(nx)
    z = range(nz)
    noise_field = field_noise((x, z), mesh_type="structured")
    
    calc = base + noise_field
    return np.clip(calc, 0, None)  # no negative calcite

def main(nx, nz):
    
    vgm = variogram(nx, nz)
    
    phi = porosity_field(vgm)
    
    calc = calcite_field(vgm)
    
    return phi.transpose(), calc.transpose()

#%%
if __name__ == "__main__":
    
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <nx> <nz>")
        sys.exit(1)
    
    nx, nz = sys.argv[1], sys.argv[2]
    
    main(nx, nz)
#%%
phi, calc = main(200, 100)

fig = plt.figure()

ax1 = fig.add_subplot(121)

ax1.imshow(phi)

ax2 = fig.add_subplot(122)

ax2.imshow(calc)

#%%

plt.hist(phi.flatten(), bins=50)    

plt.show()
    
    
