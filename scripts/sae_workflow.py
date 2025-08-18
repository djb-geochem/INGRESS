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

#change sys.path to project root
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(PROJECT_ROOT)

import yaml
from scripts.input_reader import prepare_inputs
from scripts.template_writer import write_templates
# from scripts.model_runner import run_pestpp
# from scripts.plotter import plot_figures
# from scripts.cleanup import cleanup



    
# load .yaml files for config, run_params and project state
with open("config.yaml") as config_file:
    cfg = yaml.safe_load(config_file)

with open("run_parameters.yaml") as run_file:
    run_params = yaml.safe_load(run_file)

with open("project_state.yaml") as state_file:
    state = yaml.safe_load(state_file)

# update and dump project state
state["run_count"] += 0 #change to 1 when project is live!
run_num = state["run_count"]

run_info = {
    "run id": f"run_{run_num:03d}",
    "timestamp": datetime.now()
        }

state["run_history"].append(run_info)

with open("project_state.yaml", "w") as state_file:
    yaml.safe_dump(state, state_file, sort_keys=False)

# set runid and directory for outputs
run_params["runid"] = f"run_{run_num:03d}"
run_params["rundir"] = "models/" + str(run_params["runid"])



# start work
prepare_inputs(cfg, run_params)
write_templates(cfg, run_params)


