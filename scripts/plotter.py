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

default_params = {
    "experiments": ["sae1", "sae2", "sae3", "sae4"],
    "fitted_species": {
        "pH": {
            "sigma": 0.2,
            "n_drop": 3,
            "flag": "pH"
        },
        "SiO2": {
            "sigma": 1e-4,
            "n_drop": 3,
            "flag": "Total_SiO2(aq)"
        },
        "Ca": {
            "sigma": 1e-4,
            "n_drop": 3,
            "flag": "Total_Ca++"
        }
    }
}


def plot_figures(run_params):
    
    if run_params == None:
        run_params = default_params
    
    plot_correlation_matrix()
    for species in run_params["fitted_species"]:
        if run_params["fitted_species"][species]["type"] == "aq":
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
    
    flag = run_params["fitted_species"][species]["flag"]
    fig, axes = best_subplots(len(run_params["experiments"]))
    
    colors = plt.cm.tab10.colors
    ymins, ymaxs = [], []

    for expt, ax, color in zip(run_params["experiments"], axes, colors):

        avg, data = pull_expt_data(expt, species)
        
        ax.plot([0, 31], [avg, avg], linestyle='-', marker='',
                color=color)
      
        ax.plot(range(len(data)), data,
                marker='o', mfc=color, mew=0.5, mec='w',
                linestyle='')
        
        model = pull_model_data(expt, flag)
        
        ax.plot(range(len(model)), model,
                marker='', linestyle='--', color=color)
        
        ax.set_title(expt)
        
        ymins.append(min(avg, data.min()))
        ymaxs.append(max(avg, data.max()))
        
    for ax in axes:
        ax.set_ylim(min(ymins)*0.9, max(ymaxs)*1.1)
        
        if max(ymaxs)/min(ymins) > 10:
            ax.set_yscale("log")
        
    fig.savefig(f"figures/{species}_plot.png")
    plt.show()

def pull_expt_data(expt, species):
    df = pd.read_csv(f"../../data/raw_data/{expt}.csv")
    avg = df[df["ID"].str.contains("Average")][species].iloc[0]
    data = df[df["ID"].str.contains("Average|Blank") == False][species].astype(float)
    
    return avg, data

def pull_model_data(expt, flag):
    
    with open(f"{expt}/results_{expt}.txt") as file:
        lines = file.readlines()
    
    for i,line in enumerate(lines):
        if line.startswith(flag):
            idx = i+1
    
    model_data = []
    for line in lines[idx:]:
        if line.lstrip()[0].isalpha():
            break
        else:
            model_data.append(float(line))
    
    return model_data
    
    
    
def read_model_parameters():
    
    with open("pest_control.rec") as model_file:
        lines = model_file.readlines()
        
    for i, line in enumerate(lines):
        if line.startswith("Parameter information"):
            parameter_line = i+2
    
    for line in lines[parameter_line:]:
        if not line.strip():
            break
        par_name = line.split()[0]
        
    if lines[parameter_line].strip():
        None

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
    
    if n == 1:
        axes = [axes]
    else:
        axes = axes.flatten()
    # Remove extra axes
    for ax in axes[n:]:
        fig.delaxes(ax)

    return fig, axes[:n]

#%%