#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 15:28:31 2025

@author: user
"""
import yaml
import sys

def load_yaml(*files):
    
    loaded = []
    for f in files:
        with open(f"{f}.yaml") as stream:
            loaded.append(yaml.safe_load(stream))
    return tuple(loaded)

if __name__ == "__main__":
    _, *args = sys.argv
    load_yaml(*args)