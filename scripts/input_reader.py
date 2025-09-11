#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 11 19:57:17 2025

@author: user
"""

import yaml
from datetime import datetime

def preprocess(cfg, run_params, state):
    build_dirs(run_params, state)
    calculate_derived_params(cfg, run_params)
    write_prerun_logs(cfg, run_params)

def build_dirs(run_params, state):
    
    # update and dump project state
    state["run_count"] += 1 #change to 1 when project is live!
    run_num = state["run_count"]
    
    run_info = {
        "run id": f"run_{run_num:03d}",
        "timestamp_start": datetime.now().isoformat()
            }
    
    state["run_history"].append(run_info)
    
    with open("project_state.yaml", "w") as state_file:
        yaml.safe_dump(state, state_file, sort_keys=False)
    
    # set runid and directory for outputs
    run_params["run_id"] = f"run{run_num:03d}"
    
    run_params["run_dir"] = run_params["project_root"] / "models" / run_params["run_id"]
    run_params["fig_dir"] = run_params["run_dir"] / "figures"
    
    for d in [run_params["run_dir"], run_params["fig_dir"]]:
        d.mkdir(parents=True, exist_ok=True)
    
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
        