#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 16:42:01 2025

@author: user
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import math

def plot_figures(run_params):
    
    plot_correlation_matrix()
    for species in run_params["fitted_species"]:
        plot_model_fit(run_params, species)

def plot_correlation_matrix():
    
    with open("pest_control.post.cov") as f:
        lines = f.readlines()
    n = int(lines[0].split()[0])
       
    cov_matrix = np.array([line.split() for line in lines[1:n+1]]).astype(float)
    
    stdev = np.sqrt(np.diag(cov_matrix))
    cor_matrix = cov_matrix / np.outer(stdev, stdev)    
    
    params = [i[:-1] for i in lines[n+2:2*n+2]]
    
    cor_df = pd.DataFrame(cor_matrix, index=params, columns=params)
    
    fig = plt.figure()
    sns.heatmap(cor_df, annot=True, cmap="coolwarm", center=0, fmt=".2f")  
    plt.tight_layout()
    fig.savefig("figures/cor_plot.png")

def plot_model_fit(run_params, species):
    
    
    fig, axes = best_subplots(len(run_params["experiments"]))
    plt.show()
    for expt in run_params["experiments"]:
        df = pd.read_csv(f"../../data/raw_data/{expt}.csv")
        
    

def best_subplots(n, figsize_scale=3):
    """
    Create a figure with `n` subplots arranged as neatly as possible.
    Prefers nrows > ncols (portrait-like).
    Removes unused axes automatically.
    
    Returns
    -------
    fig, axes_flat : (Figure, list of Axes)
    """
    # Start with square-ish guess
    nrows = math.ceil(math.sqrt(n))
    ncols = math.ceil(n / nrows)

    # Flip to prefer more rows than cols if possible
    if ncols > nrows:
        nrows, ncols = ncols, nrows

    fig, axes = plt.subplots(nrows, ncols,
                             figsize=(figsize_scale*ncols, figsize_scale*nrows))
    axes = axes.flatten()

    # Remove extra axes
    for ax in axes[n:]:
        fig.delaxes(ax)

    return fig, axes[:n]
