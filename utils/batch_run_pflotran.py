#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 19:45:27 2025

@author: user
"""
import sys
import subprocess

def main():
    
    expt_list = sys.argv[1:]

    commands = [["python", "../../utils/run_pflotran.py", f"{expt}"] for expt in expt_list]
    
    cpus = 4
    
    while commands:
        batch = commands[:cpus]
        commands = commands[cpus:]
        procs = [subprocess.Popen(i) for i in batch]
        for p in procs:
            p.wait()

if __name__ == "__main__":
    
    main()