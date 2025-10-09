#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 11 20:28:01 2025

@author: user
"""
from jinja2 import Environment, FileSystemLoader
import pandas as pd
from collections import defaultdict
from pathlib import Path

def write_templates(cfg, run_params):
    obsdata = build_obs_data(run_params)
    write_pest_control(cfg, run_params, obsdata)
    for expt in run_params["experiments"]:
        write_pflotran_in(cfg, run_params, expt)
        write_instructions(cfg, run_params, expt, obsdata)
    
    
def write_pest_control(cfg, run_params, obsdata):
    template_dir = cfg["paths"]["templates"]
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("pest_control.master")
    
    context = {
        **run_params,
        "obsdata": obsdata
    }
    
    rendered_text = template.render(context)
    
    output_dir = run_params["run_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "pest_control.pst"
    
    with open(output_file, "w") as f:
        f.write(rendered_text)

def write_pflotran_in(cfg, run_params, expt):
    template_dir = cfg["paths"]["templates"]
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("pflotran.master")
    
    expt_CO2 = cfg["expt_conditions"][expt]["CO2"] * 44 / 1e6
    
    expt_phi = cfg["expt_conditions"][expt]["porosity"]/100.0
    
    expt_bulk = 1-expt_phi
    
    expt_calc = expt_bulk * cfg["expt_conditions"][expt]["calcite"]

    expt_qtz = expt_bulk - expt_calc
    
    expt_sio2 = cfg["expt_conditions"][expt]["sio2"]
    
    context = {
        **run_params,
        "expt_calc": expt_calc,
        "expt_CO2": expt_CO2,
        "expt_qtz": expt_qtz,
        "expt_sio2": expt_sio2
    }
    
    
    
    rendered_text = template.render(context)
    
    output_filename = str(expt) + ".in.tpl"
    output_dir = run_params["run_dir"] / f"{expt}"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / output_filename
    
    with open(output_file, "w") as f:
        f.write(rendered_text)    
    
def write_instructions(cfg, run_params, expt, obsdata):
    
    ins_filename = run_params['run_dir'] / f"{expt}/instr_{expt}.ins"
    with open(ins_filename, 'w') as f:
        f.write("pif *\n")
        for species in run_params["fitted_species"]:
            if run_params["fitted_species"][species]["type"] == "aq":
                flag = run_params["fitted_species"][species]["flag"]
                f.write(f"*{flag}*\n")
                species_obs = [
                    obs_name
                    for obs_name, data in obsdata.items()
                    if data["expt"] == expt 
                    and obs_name.split("_")[0] == species
                ]
                for obs in species_obs:
                    f.write(f"l1 !{obs}!\n")
        # for mineral in run_params["fitted_minerals"]:
        #     if expt in run_params["fitted_minerals"][mineral]["active_for"]:
        #         flag = run_params["fitted_minerals"][mineral]["flag"]
        #         f.write(f"*{flag}*\n")
        #         f.write(f"l1 !{mineral}_{expt}!")
            

def pull_expt_data(expt, species_list):
    df = pd.read_csv("data/raw_data/" + str(expt) + ".csv")
    df = df[df["ID"].str.contains("Average|Blank") == False]
    cols = ["ID"] + species_list
    df = df[cols]
    return df

def build_obs_data(run_params):
    obs_data = defaultdict(dict)           
    species_list = list(run_params["fitted_species"].keys())
        
    for expt in run_params["experiments"]:
        df = pull_expt_data(expt, species_list)
        
        for species in species_list:
            species_params = run_params["fitted_species"][species]
            if species_params["type"] == "aq":
                w = 1/float(species_params["sigma"])
                for _, row in df.iterrows():
                    obs_name = f"{species}_{row['ID']}"
                    obs_data[obs_name] = {
                        "val": row[species],  # get species value dynamically
                        "w": w,
                        "expt": expt,
                        "species": species,
                        "ID": row["ID"]
                    }
                    if int(row["ID"][-2:]) <= species_params["n_drop"]:
                        obs_data[obs_name]["w"] = w/1000
                    if obs_name in run_params["drop_obs"]:
                        obs_data[obs_name]["w"] = w/1000
            
    return dict(obs_data)
        
        
    

    
    
    
