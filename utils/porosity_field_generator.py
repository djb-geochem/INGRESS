#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 13:37:15 2025

@author: user
"""

import numpy as np
import gstools as gs
import matplotlib.pyplot as plt

def lognormal_params_from_mean_std(m, s):
    """Return (mu, sigma) for underlying normal given desired mean m and std s of lognormal."""
    sigma2 = np.log(1.0 + (s**2) / (m**2))
    sigma = np.sqrt(sigma2)
    mu = np.log(m) - 0.5 * sigma2
    return mu, sigma

def make_fields(nx, nz,
                poro_mean=0.05, poro_std=0.01,
                calc_mean=0.01, calc_std=0.005,
                rho=-0.6,  # gaussian-space correlation between Y and Cg
                vgm_len=200.0, vgm_var=1.0, anis=1e-2,
                noise_len=50.0, noise_var=1.0):
    """
    Returns (porosity, calcite, Y, Cg) arrays shaped (nx, nz).
    rho is correlation in Gaussian space (rho<0 => anticorrelation).
    Note: both SRFs use the same covariance model here, but you can use different models.
    """
    # Covariance model (standardized)
    model = gs.Exponential(dim=2, var=vgm_var, len_scale=vgm_len, anis=anis)
    srf_Y = gs.SRF(model, seed=42)

    # independent SRF for mixing
    model2 = gs.Exponential(dim=2, var=noise_var, len_scale=noise_len, anis=anis)
    srf_E = gs.SRF(model2, seed=99)

    x = range(nx)
    z = range(nz)
    # Gaussian fields with (approx) zero mean; var depends on model.var
    Y = srf_Y.structured([x, z], mesh_type="structured")  # base field for poro
    E = srf_E.structured([x, z], mesh_type="structured")  # independent field

    # Standardize to zero mean unit variance (so transforms formulas are safe)
    Y = (Y - np.mean(Y)) / np.std(Y)
    E = (E - np.mean(E)) / np.std(E)

    # correlated Gaussian field for calcite (Cg)
    rho = float(rho)
    assert -1.0 <= rho <= 1.0
    Cg = rho * Y + np.sqrt(max(0.0, 1.0 - rho**2)) * E
    Cg = (Cg - np.mean(Cg)) / np.std(Cg)  # normalize if desired

    # compute lognormal transform parameters
    mu_p, sigma_p = lognormal_params_from_mean_std(poro_mean, poro_std)
    mu_c, sigma_c = lognormal_params_from_mean_std(calc_mean, calc_std)

    # generate positive lognormal fields
    porosity = np.exp(mu_p + sigma_p * Y)
    calcite = np.exp(mu_c + sigma_c * Cg)

    return porosity, calcite, Y, Cg

# Example usage
nx, nz = 200, 50
poro, calc, Y, Cg = make_fields(nx, nz,
                               poro_mean=0.05, poro_std=0.01,
                               calc_mean=0.01, calc_std=0.005,
                               rho=-0.6,
                               vgm_len=300.0, noise_len=70.0)

# quick checks
print("porosity mean/std:", poro.mean(), poro.std())
print("calcite mean/std  :", calc.mean(), calc.std())
print("empirical corr (porosity, calcite):", np.corrcoef(poro.flatten(), calc.flatten())[0,1])

# quick plots
plt.figure(figsize=(10,4))
plt.subplot(1,3,1); plt.imshow(poro.T, origin='lower'); plt.title('Porosity')
plt.subplot(1,3,2); plt.imshow(calc.T, origin='lower'); plt.title('Calcite')
plt.subplot(1,3,3); plt.scatter(poro.flatten(), calc.flatten(), s=2); plt.xlabel('phi'); plt.ylabel('calc'); plt.title('scatter')
plt.tight_layout()
plt.show()
