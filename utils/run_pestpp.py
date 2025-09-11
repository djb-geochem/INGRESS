#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 02:03:57 2025

@author: user
"""

import subprocess

def run_pestpp():
    glm_exe = "pestpp-glm"
    sen_exe = "pestpp-sen"
    input_file = "pest_control.pst"
    
    glm_cmd = [glm_exe, input_file]
    sen_cmd = [sen_exe, input_file]
    
    subprocess.run(glm_cmd, text=True)
    # subprocess.run(sen_cmd, text=True)
    
    print_optimal_parameter_values()

def print_optimal_parameter_values():
    
    with open("pest_control.rec") as resultsfile:
        lines = resultsfile.readlines()
    
    for i, line in enumerate(lines):
        if line.startswith("FINAL OPTIMISATION RESULTS"):
            idx = i
    
    for line in lines[idx:idx+7]:
        print(line)
    
    for line in lines[idx+7:]:
        if not line.strip():
            break
        else:
            print(line)
    
if __name__ == "__main__":
    run_pestpp()
