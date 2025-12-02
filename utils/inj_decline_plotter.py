#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 20 14:28:07 2025

@author: user
"""
import matplotlib.pyplot as plt
import pyvista as pv
import numpy as np




def extract_inlet_flux(vtk_file, tol=1e-6):
    grid = pv.read(vtk_file)

    # Compute centroid of each cell
    centroids = grid.cell_centers().points  # shape (n_cells, 3)
    xs = centroids[:, 0]
    
    

    xmin = xs.min()
    mask = np.abs(xs - xmin) < tol
    
    cell_ids = np.where(mask)[0]
    
    velocities = grid.cell_data["Vlx"]
    
    inlet_velocities = velocities[cell_ids]
    
    avg_velocity = sum(inlet_velocities)/len(inlet_velocities)
          
    return avg_velocity

def plot_inj_decline(expt, nfiles=438):
    
    fig, ax = plt.subplots()
    fluxes = []
    
    area = 2*3.14*0.1*300
        
    for i in range(1, nfiles):
        
        filename = f"{expt}-vel-{i:03}.vtk"
        
        avg_vel = extract_inlet_flux(filename)
        
        flux = avg_vel * area #m^3/s
        
        flux_t_hr = flux*60*60
        
        fluxes.append(flux_t_hr)
        
    x = np.array(range(len(fluxes))) * 100/24
    
    ax.plot(x, fluxes, 'r-')
    
    ax.set_ylabel(r"$Injectivity\,\,(t/hr)$")
    ax.set_xlabel(r"$Time\,\,(d)$")    
    fig.savefig("figures/inj_decline.png")

def test():
    fig, ax = plt.subplots()
    
    vels = extract_inlet_flux("reservoir-vel-001.vtk")
    
    print(vels)
    
    avg_vel = sum(vels)/len(vels)
    
    inlet_area = 2 * 3.14 * 0.1 * 300
    
    vol_flux = avg_vel * inlet_area #m^3/s
    
    
    print(len(vels))
    print(vol_flux)
    
    ax.plot(range(len(vels)), vels)


# plot_inj_decline("reservoir")