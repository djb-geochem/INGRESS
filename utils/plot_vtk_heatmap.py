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


def animate_vtk_series(scalar_name, nfiles=129, shape=(20,10), outfile="animation.mp4"):
    """
    Loads scalar arrays from multiple vtk files and animates them.
    Saves to MP4 using ffmpeg.
    """
    # Load all frames
    frames = []
    for i in range(nfiles):
        fname = f"sae1-{i:03d}.vtk"
        arr = read_vtk_scalar(fname, scalar_name, shape)
        frames.append(arr)
    
    frames = np.array(frames)

    # Set up figure
    vmin = frames.min()
    vmax = frames.max()
    fig, ax = plt.subplots(figsize=(8,4))
    im = ax.imshow(frames[0], cmap="viridis", origin="lower", aspect="auto",
                   vmin=vmin, vmax=vmax)
    cbar = plt.colorbar(im, ax=ax, label=scalar_name)
    ax.set_xlabel("Index (20)")
    ax.set_ylabel("Index (5)")

    def update(frame_idx):
        im.set_data(frames[frame_idx])
        ax.set_title(f"{scalar_name} timestep {frame_idx}")
        return [im]

    ani = animation.FuncAnimation(fig, update, frames=len(frames), interval=200, blit=True)

    # Save as mp4
    ani.save(outfile, writer="ffmpeg", fps=5)
    plt.close(fig)
    print(f"Animation saved to {outfile}")

    return outfile


# Example usage:
animate_vtk_series("pH")
