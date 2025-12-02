#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 20 13:11:45 2025

@author: user
"""
import sys
import os
import pathlib
import subprocess

#change sys.path to project root
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(PROJECT_ROOT)

from utils import load_yaml
from utils.animate_vtk_series import animate_vtk_series
from utils.inj_decline_plotter import plot_inj_decline
from scripts.build_reservoir_model import build_reservoir_model

def main():
    
    res_params = load_yaml("reservoir_model_parameters")[0]
    res_params["template_dir"] = PROJECT_ROOT / "templates"
    res_params["output_dir"] = PROJECT_ROOT / "reservoir"
    res_params["cell_count"] = res_params["nx"] * res_params["nz"]
    
    
    build_reservoir_model(res_params)
       
    os.chdir(res_params["output_dir"])
    os.makedirs("figures", exist_ok=True)
    
    cmd = ["mpirun", "-n", "4", "pflotran", "-input_prefix", "reservoir"]
    
    print(f"[INFO] Running PFLOTRAN reservoir model - \
          cell count = {res_params['cell_count']}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    print("[INFO] PFLOTRAN run complete")
    
    plot_inj_decline("reservoir")
    
    for var in res_params["plot"]:
        None
        animate_vtk_series(var)


if __name__ == "__main__":
    main()