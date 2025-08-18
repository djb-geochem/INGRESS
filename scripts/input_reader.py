#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 11 19:57:17 2025

@author: user
"""
import os
from pathlib import Path

def prepare_inputs(cfg, run_params):
    calculate_derived_params(cfg, run_params)
    write_prerun_logs(cfg, run_params)


def calculate_derived_params(cfg, run_params):
    active_pargp = set([i["pargp"] for i in run_params["tuned_parameters"].values()])
    npargp = len(active_pargp)
    npar = len(run_params["tuned_parameters"])
    nobsgp = len(run_params["fitted_species"])
    nsamp = sum(cfg["expt_conditions"][expt]["duration"] for expt in run_params["experiments"])
    nobs = nsamp * nobsgp
    ntplfle = len(run_params["experiments"])
    ninsfle = nsamp * ntplfle
    
    control_data = {
        "npargp": npargp,
        "npar": npar,
        "nobsgp": nobsgp,
        "nsamp": nsamp,
        "nobs": nobs,
        "ntplfle": ntplfle,
        "ninsfle": ninsfle
    }
    
    run_params["control_data"] = control_data
    
    run_params["obsgps"] = [
        f"{species}_{expt}"
        for expt in run_params["experiments"]
        for species in run_params["fitted_species"]
    ]
    
    for pargp in run_params["parameter_groups"]:
        run_params["parameter_groups"][pargp]["active"] = pargp in active_pargp
        
def write_prerun_logs(cfg, run_params):
    None
        