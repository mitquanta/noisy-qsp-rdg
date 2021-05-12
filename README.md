# noisy-qsp-rdg

### Code Structure

* `qsp.py` is the main module with the QSP simulation and optimization methods
* `plots.py` contains assorted data handling and plot generation methods
* `classical.py` calculates the single-shot Helstrom probabilities
* `sample-angles.py` generates a set of optimal QSP-3 angles for a 0.001 by 0.001 grid, calculates the probabilities, and saves the results
* `sample-plots.py` loads all the data and produces quantum advantage plots

### Usage

The workflow for any QSP strategy is to first generate optimal angles and calculate probabilities (e.g. `sample-angles.py`), then plot the results (e.g. `sample-plots.py`). Because optimization is slow due to many iterations of calling `qsp_simul`, it is typical to do the optimization using a smaller number of trials, and then calculate the probabilities more precisely using a larger number of trials with set angles. One can also run the same optimization many times with different randomization or initial conditions, and then take the supremum of the results.

For the sample code, the order of files to run is
* `python classical.py` 
* `python sample-angles.py` (can optionally be swapped with the prior step)
* `python sample-plots.py`

One may wish to modify the loops to a coarser or smaller grid on a first go. The procedure is embarrassingly parallel, as the optimization and calculations can be performed on different regions of the grid in parallel.
