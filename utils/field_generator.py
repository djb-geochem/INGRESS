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
import h5py

def variogram(nx, nz, var=0.1, len_scale=1e3, anis=1e-2):
    
    model = gs.Exponential(dim=2, var=var,
                           len_scale=len_scale, anis=anis) 
    
    x = range(nx)
    z = range(nz)
    
    field = gs.SRF(model, seed=19921026)
    
    Y = field((x, z), mesh_type="structured")
    
    return Y

def porosity_field(Y, avg_phi=0.05):
    
    phi = avg_phi * np.exp(Y)
    
    return np.clip(phi, 0.001, 0.2)

def calcite_field(Y, avg_calc=0.01, alpha=0.0005, len_scale_noise=200, anis=1e-2):
    # large-scale relation to Y (e.g. inverse correlation)
    base = avg_calc + alpha * (-Y)
    
    # small-scale correlated "noise"
    model_noise = gs.Exponential(dim=2, var=0.0001, len_scale=len_scale_noise, anis=anis)
    field_noise = gs.SRF(model_noise, seed=19921026)
    
    nx, nz = Y.shape
    x = range(nx)
    z = range(nz)
    noise_field = field_noise((x, z), mesh_type="structured")
    
    calc = base + noise_field
    return np.clip(calc, 0, None)  # no negative calcite

def create_h5_file(nx, nz):
    
    #create reservoir.h5 file with index Cell ID array
    
    filename = "reservoir/reservoir.h5"
    h5file = h5py.File(filename, mode='w')
    
    n = nx * nz
    
    iarray = np.arange(n, dtype='i4')
    # convert to 1-based
    iarray[:] += 1
    h5file.create_dataset("Cell Ids", data=iarray)
    
    return h5file

def add_h5_dataset(file, name, array):
    
    array = array.transpose()
    
    file.create_dataset(name, data=array.flatten(), dtype='float64')

def plot_initial_distribution(nx, nz, name, array):
    
    fig = plt.figure(figsize=(6, 5))
    ax = fig.add_subplot(111)

    # Plot the array
    im = ax.imshow(array.transpose()[::-1, :], aspect='auto')

    # Add a horizontal colorbar at the bottom
    cbar = fig.colorbar(im, ax=ax, orientation='horizontal', pad=0.15)
    cbar.set_label('Value', fontsize=10)

    fig.tight_layout()

    fig.savefig(f"reservoir/figures/{name}_initial.png", dpi=100)
    plt.close(fig)

def write_reservoir_dataset(nx, nz, avg_phi=0.05, avg_calc=0.01,
                            calc_is=0.00226853):
    
    vgm = variogram(nx, nz)
    phi = porosity_field(vgm, avg_phi=avg_phi)   
    calc = calcite_field(vgm, avg_calc=avg_calc)
      
    qtz = 1 - phi - calc - calc_is
    
    perm_x = 1e-12 * phi**3 / (1- phi)**2
    perm_z = 0.1 * perm_x
    
    reservoir_file = create_h5_file(nx, nz)
    
    datasets = [phi, calc, qtz, perm_x, perm_x, perm_z]
    
    names = ["Porosity", "Calcite_VF", "Quartz_VF",
             "PermX", "PermY", "PermZ"]
    
    for dataset, name in zip(datasets, names):
        
        plot_initial_distribution(nx, nz, name, dataset)
        add_h5_dataset(reservoir_file, name, dataset)
    
    reservoir_file.close()


"""
#%%
if __name__ == "__main__":
    
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <nx> <nz>")
        sys.exit(1)
    
    nx, nz = sys.argv[1], sys.argv[2]
    
    main(nx, nz)
#%%
phi, calc = main(100, 20)

write_h5_file("Porosity", phi)

fig = plt.figure()

ax1 = fig.add_subplot(121)

ax1.imshow(phi)

ax2 = fig.add_subplot(122)

ax2.imshow(calc)

#%%

plt.hist(phi.flatten(), bins=50)    

plt.show()
"""
    
