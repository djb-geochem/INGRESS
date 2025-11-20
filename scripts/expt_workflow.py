#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 11 18:09:57 2025

@author: David Byrne
"""
import sys
import os
import pathlib



#change sys.path to project root
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(PROJECT_ROOT)

from scripts.input_reader import preprocess
from scripts.template_writer import write_templates
from utils import load_yaml, run_pestpp
from scripts.plotter import plot_figures
from scripts.postprocessing import postprocess

def initialize():

    cfg, run_params, state = load_yaml(
        "config", "run_parameters", "project_state")
    run_params["project_root"] = PROJECT_ROOT
    
    return cfg, run_params, state
    

def main():
       
    # start work
    cfg, run_params, state = initialize()
    preprocess(cfg, run_params, state)
    write_templates(cfg, run_params)
    os.chdir(run_params["run_dir"])
    run_pestpp()
    plot_figures(run_params)
    postprocess()
    
    
    
if __name__ == "__main__":
    main()