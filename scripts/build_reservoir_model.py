#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 20:53:46 2025

@author: user
"""
import sys
import os
import pathlib
from jinja2 import Environment, FileSystemLoader

#change sys.path to project root
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(PROJECT_ROOT)

from utils.grid_generator import generate_grid, format_grid
from utils.field_generator import write_reservoir_dataset
from utils import load_yaml


if __name__ == "__main__":
    
    res_params = load_yaml("reservoir_model_parameters")[0]
    
    res_params["dx"] = generate_grid(res_params["nx"],
                                     res_params["len_x"])
    
    res_params["formatted_grid"] = format_grid(res_params["dx"])
    
    #write reservoir_dataset
    write_reservoir_dataset(res_params["nx"], res_params["nz"])
    
    #load template
    template_dir = PROJECT_ROOT / "templates"
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("reservoir.master")
    
    #write template
    
    rendered_template = template.render(res_params)

    output_dir = PROJECT_ROOT / "reservoir"
    output_file = output_dir / "reservoir.in"
    
    with open(output_file, "w") as f:
        f.write(rendered_template)