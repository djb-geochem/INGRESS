#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 15 22:56:56 2025

@author: user
"""
import subprocess
import sys
import yaml
import os



def run_pflotran(expt):
    
    exe = "pflotran"

    cmd = [exe, "-input_prefix", f"{expt}"]

    print(f"[INFO] Running PFLOTRAN: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"[ERROR] PFLOTRAN failed for {expt}")
        print(result.stderr)
        sys.exit(result.returncode)

    print(f"[INFO] Finished {expt}")
    return result.stdout

def process_results(cfg, expt):
    
    result_steps = range(1, 32)
    
    flags = cfg["output_flags"]
    
    processed_results = {}
    
    for flag in flags:
        processed_results[flag["name"]] = []
        
    
    for step in result_steps:
        label = step*4 + 1
        vtkname = f"{expt}-{label:03d}.vtk"
        with open(vtkname) as vtkfile:
            lines = vtkfile.readlines()
            for flag in flags:
                result = lines[flag["line"]].split()[0]
                processed_results[flag["name"]].append(result)
    
    resultsfile = f"results_{expt}.txt"
    
    with open(resultsfile, 'w') as f:
        for flag, values in processed_results.items():
            f.write(f"{flag}\n")
            for v in values:
                f.write(f"{v}\n")
        
if __name__ == "__main__":
    
    with open("../../config.yaml") as config_file:
        cfg = yaml.safe_load(config_file)
    
    expt_list = sys.argv[1:]
    
    for expt in expt_list:
        # cmd = ["cp", "../../hanford.dat", expt]
        # subprocess.run(cmd)
        os.chdir(expt)
        run_pflotran(expt)
        process_results(cfg, expt)
        os.chdir("..")