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
    
if __name__ == "__main__":
    run_pestpp()
