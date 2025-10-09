import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def read_vtk_scalar(filename, scalar_name, shape=(10,20)):
    data = []
    capture = False
    
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
                    numbers = [float(x) for x in line.split()]
                    data.extend(numbers)

    if not data:
        raise ValueError(f"Scalar '{scalar_name}' not found in {filename}")

    return np.array(data).reshape(shape)


def animate_vtk_series(expt_list, scalar_name, nfiles=129, shape=(20,10)):
    """
    Loads scalar arrays from multiple vtk files and animates them.
    Saves to MP4 using ffmpeg.
    """
    
    outfile = f"figures/{scalar_name}.mp4"
    # Load all frames
    frames = []
    for expt in expt_list:
        expt_frames = []
        for i in range(nfiles):
            fname = f"{expt}/{expt}-{i:03d}.vtk"
            arr = read_vtk_scalar(fname, scalar_name, shape)
            expt_frames.append(arr)
        frames.append(np.array(expt_frames))
    
    frames = np.array(frames)

    # Set up figure
    vmin = frames.min()
    vmax = frames.max()
    fig, axes = plt.subplots(nrows=1, ncols=4, figsize=(8,4))
    images = []

    for ax, expt_frames, expt in zip(axes.flatten(), frames, expt_list):
        im = ax.imshow(expt_frames[0], cmap="viridis", origin="lower", aspect="auto",
                       vmin=vmin, vmax=vmax)
        images.append(im)
        ax.set_title(f"{expt}")
        ax.set_xticks([])
        ax.set_yticks([])
    cbar = fig.colorbar(im, ax=axes.ravel().tolist(),
                        orientation="horizontal",
                        fraction=0.05, pad=0.2, label=scalar_name)

    def update(frame_idx):
        for im, expt_frames in zip(images, frames):
            im.set_data(expt_frames[frame_idx])
        fig.suptitle(f"{scalar_name} timestep {frame_idx}")
        return images

    ani = animation.FuncAnimation(fig, update, frames=len(frames[0]), interval=200, blit=True)

    # Save as mp4
    ani.save(outfile, writer="ffmpeg", fps=5)
    plt.close(fig)
    print(f"Animation saved to {outfile}")

    return outfile


# Example usage:
    
expt_list = ["sae1", "sae2", "sae3", "sae4"]

variable_list = ["Porosity", "Calcite_VF", "SiO2(am)_VF",
                 "Kaolinite_VF", "Total_Al+++"]

for var in variable_list:
    animate_vtk_series(expt_list, var)
