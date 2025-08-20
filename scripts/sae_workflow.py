#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 11 18:09:57 2025

@author: David Byrne
"""
import sys
import os
import pathlib
from datetime import datetime
import subprocess
import yaml

#change sys.path to project root
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(PROJECT_ROOT)

from scripts.input_reader import preprocess
from scripts.template_writer import write_templates
from utils import load_yaml, run_pestpp
from scripts.plotter import plot_figures
# from scripts.cleanup import cleanup



def main():

    cfg, run_params, state = load_yaml(
        "config", "run_parameters", "project_state")
    # update and dump project state
    state["run_count"] += 0 #change to 1 when project is live!
    run_num = 20 #state["run_count"]
    
    run_info = {
        "run id": f"run_{run_num:03d}",
        "timestamp_start": datetime.now().isoformat()
            }
    
    state["run_history"].append(run_info)
    
    with open("project_state.yaml", "w") as state_file:
        yaml.safe_dump(state, state_file, sort_keys=False)
    
    # set runid and directory for outputs
    run_params["runid"] = f"run_{run_num:03d}"
    run_params["rundir"] = "models/" + str(run_params["runid"])
           
    # start work
    preprocess(cfg, run_params)
    write_templates(cfg, run_params)
    subprocess.run(["cp", "hanford.dat", run_params["rundir"]])
    os.chdir(run_params["rundir"])
    # run_pestpp()
    # os.mkdir("figures")
    plot_figures(run_params)
    
if __name__ == "__main__":
    main()