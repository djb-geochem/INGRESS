#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 20 14:28:07 2025

@author: user
"""
import matplotlib.pyplot as plt
import pyvista as pv
import numpy as np



def plot_inj_decline():
    
    fig, ax = plt.subplots()
    
    


def extract_inlet_flux(vtk_file, tol=1e-6):
    grid = pv.read(vtk_file)

    # Compute centroid of each cell
    centroids = grid.cell_centers().points  # shape (n_cells, 3)
    xs = centroids[:, 0]
    
    

    xmin = xs.min()
    mask = np.abs(xs - xmin) < tol
    
    cell_ids = np.where(mask)[0]
    
    velocities = grid.cell_data["Vlx"]
    
    return sum(velocities[cell_ids])

def plot_inj_decline(expt, nfiles=438):
    
    fig, ax = plt.subplots()
    fluxes = []
    
    for i in range(1, nfiles):
        
        filename = f"{expt}-vel-{i:03}.vtk"
        
        fluxes.append(extract_inlet_flux(filename))

    ax.plot(range(len(fluxes)), fluxes, 'r-')
    
    fig.savefig("figures/inj_decline.png")
    

