#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 16:35:39 2025

@author: user
"""
import subprocess


def postprocess():
    subprocess.run(["rm", "-rf", "../lastrun/*"])
    subprocess.run("cp -rf * ../lastrun/", shell=True, check=True)
    

if __name__ == "__main__":
    postprocess()