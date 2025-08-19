#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 02:03:57 2025

@author: user
"""

import subprocess

def run_pestpp():
    exe = "pestpp-glm"
    
    input_file = "pest_control.pst"
    
    cmd = [exe, input_file]
    
    subprocess.run(cmd, text=True)
