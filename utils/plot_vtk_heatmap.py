import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import re

def fix_fortran_float(s):
    """
    Convert Fortran-like numbers such as 3.101497-319 → 3.101497E-319
    """
    # Match patterns without 'E' but with a trailing exponent
    if re.match(r'^[+-]?\d*\.\d+[+-]\d+$', s):
        # Insert E before the final sign
        return float(re.sub(r'([0-9])([+-]\d+)$', r'\1E\2', s))
    return float(s)

def find_resolution(expt):
    
    filename = f"{expt}.in"
    
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith("  NXYZ"):
                parts = line.split()
                nx, nz = int(parts[1]), int(parts[3])
                return nx, nz
    
    raise ValueError("NXYZ not found in input file")

def read_vtk_scalar(filename, scalar_name, nx, nz):
    data = []
    capture = False
    shape = (nx, nz)
    with open(filename, "r") as f:
        for line in f:
            if line.startswith("SCALARS") and scalar_name in line:
                capture = True
                continue
            if capture:
                if line.startswith("LOOKUP_TABLE"):
                    continue
                elif line.strip() == "" or line.startswith("SCALARS"):
                    break
                else:
                    numbers = [fix_fortran_float(x) for x in line.split()]
                    data.extend(numbers)

    if not data:
        raise ValueError(f"Scalar '{scalar_name}' not found in {filename}")

    return np.array(data).reshape(shape)


def animate_vtk_series(scalar_name, expt="reservoir", nfiles=400):
    """
    Loads scalar arrays from multiple vtk files and animates them.
    Saves to MP4 using ffmpeg.
    """
    
    nx, nz = find_resolution(expt)
    
    outfile = f"figures/{scalar_name}.mp4"

    expt_frames = []
    for i in range(nfiles):
        if scalar_name in velocities:
            vel = "vel-"
        else:
            vel = ""
        fname = f"{expt}-{vel}{i:03d}.vtk"
        arr = read_vtk_scalar(fname, scalar_name, nz, nx)
        expt_frames.append(arr)
    
    expt_frames = np.array(expt_frames)
    # Set up figure
    vmin = expt_frames.min()
    vmax = expt_frames.max()
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8,4))

    im = ax.imshow(expt_frames[0], cmap="viridis", origin="lower", aspect="equal",
                   vmin=vmin, vmax=vmax)
    ax.set_title(f"{expt}")
    ax.set_xticks([])
    ax.set_yticks([])
    cbar = fig.colorbar(im, ax=ax,
                        orientation="horizontal",
                        fraction=0.05, pad=0.2, label=scalar_name)

    def update(frame_idx):
        im.set_data(expt_frames[frame_idx])
        fig.suptitle(f"{scalar_name} timestep {frame_idx}")
        return [im]

    ani = animation.FuncAnimation(fig, update, frames=len(expt_frames), interval=200, blit=True)

    # Save as mp4
    ani.save(outfile, writer="ffmpeg", fps=5)
    plt.close(fig)
    print(f"Animation saved to {outfile}")

    return outfile

velocities = ["Vlx", "Vlz"]
# Example usage:
    
expt_list = ["reservoir"]

variable_list = ["Liquid_Pressure", "Calcite_VF", "SiO2(am)_VF", "pH",
                 "Total_Tracer", "Porosity", "Permeability", "Vlx", "Vlz",
                 "Temperature"]

for var in variable_list:
    animate_vtk_series(var)
