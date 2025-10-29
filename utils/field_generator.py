#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 18:03:49 2025

@author: user
"""

import numpy as np
import gstools as gs
import matplotlib.pyplot as plt

x = y = np.arange(100)

model_1 = gs.Exponential(dim=2, var=1, len_scale=1e3, anis=1e-2)
model_2 = gs.Gaussian(dim=2, var=1, len_scale=1e2, anis=1e-2)

model_3 = model_1 + model_2

fig = plt.figure(figsize=[10, 4])

ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

srf_1 = gs.SRF(model_1, seed=19921026)
srf_1.structured([x,y])
srf_1.plot(fig=fig, ax=ax1)

srf_2 = gs.SRF(model_2, seed=19921026)
srf_2.structured([x,y])
srf_2.plot(fig=fig, ax=ax2)

srf_1.vtk_export(filename="porosity_field.vtk")

