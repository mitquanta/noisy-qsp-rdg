import numpy as np
import matplotlib.pyplot as plt
import matplotlib

font = {'size': 18}
matplotlib.rc('font', **font)

def generate_data(func, xmin = 0, ymin = 0, xmax = 0.5001, ymax = 0.5001, dx = 0.01, dy = 0.01):
    '''
    Generate the 2-D array of data applying func to a grid

    Args:
        func: Function to be applied
        xmin: Lower limit for x-axis
        ymin: Lower limit for y-axis
        xmax: Upper limit for x-axis, not inclusive
        ymax: Upper limit for y-axis, not inclusive
        dx: Increment for x-axis
        dy: Increment for y-axis

    Returns:
        2-dimensional numpy array
    '''
    data = []
    for y in np.arange(ymin, ymax, dy):
        row = []
        for x in np.arange(xmin, xmax, dx):
            row.append(func(np.round(x, 3), y))
        data.append(row)
    return np.array(data)

def load_data(filename, empty={}):
    '''
    Wrapper for loading numpy data from a textfile

    Args: 
        fielname: Name of file to load
        empty: What to return if the file fails to load

    Returns:
        np.ndarray of the data, or empty if it fails to load
    '''
    try:
        return np.loadtxt(filename)
    except:
        return empty
    
# Plotting functions

def rdg_plot(data, xmin = 0, ymin = 0, xmax = 0.5001, ymax = 0.5001, dx = 0.01, dy = 0.01, scalemin=0.5, scalemax=1, colors="RdBu", scalelabel="Success probability", title="", filename=None, show=False):
    '''
    Two-dimensional color plot of data for a rotation discrimination game

    Args:
        data: Dataset to be plotted
        xmin: Lower limit for x-axis
        xmax: Upper limit for x-axis
        ymin: Lower limit for y-axis
        ymax: Upper limit for y-axis
        dx: Increment for x-axis
        dy: Increment for y-axis
        scalemin: Lower limit for color scale
        scalemax: Upper limit for color scale
        colors: Colorset for cmap
        scalelabel: Label of color scale
        title: Title of graph
        filename: Name of file to save image, or None to not save
        show: Whether to show the plot via plt.show()

    Returns:
        None
    '''
    y, x = np.mgrid[slice(ymin, ymax, dy), slice(xmin, xmax, dx)]
    plt.pcolormesh(x, y, data, cmap=colors, vmin=scalemin, vmax=scalemax)
    plt.colorbar(label=scalelabel)
    plt.xlabel(r"$\delta/\pi$")
    plt.ylabel(r"$\sigma/\pi$")
    plt.title(title)
    if filename:
        plt.savefig(filename, bbox_inches="tight")
    if show:
        plt.show()

def compare_plots(data1, data2, xmin = 0, ymin = 0, xmax = 0.5001, ymax = 0.5001, dx = 0.01, dy = 0.01, scalemin = -0.1, scalemax = 0.1, colors="RdBu", scalelabel="Log success ratio", title="", filename=None, show=False):
    '''
    Log ratio plot comparing data1 and data2

    Returns:
        Numpy matrix with log ratio dataset
    '''
    log_ratio = np.log(data2/data1)
    rdg_plot(log_ratio, xmin, ymin, xmax, ymax, dx, dy, scalemin, scalemax, colors, scalelabel, title, filename, show)
    return log_ratio
