#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 20:53:46 2025

@author: user
"""

from jinja2 import Environment, FileSystemLoader
from utils.grid_generator import generate_grid, format_grid
from utils.field_generator import write_reservoir_dataset

def build_reservoir_model(res_params):
    
    
    res_params["dx"] = generate_grid(res_params["nx"],
                                     res_params["len_x"])
    
    res_params["formatted_grid"] = format_grid(res_params["dx"])
    
    #write reservoir_dataset
    write_reservoir_dataset(res_params["nx"], res_params["nz"])
    
    #load template
    env = Environment(loader=FileSystemLoader(res_params["template_dir"]))
    template = env.get_template("reservoir.master")
    
    #write template
    
    rendered_template = template.render(res_params)

    
    output_file = res_params["output_dir"] / "reservoir.in"
    
    with open(output_file, "w") as f:
        f.write(rendered_template)