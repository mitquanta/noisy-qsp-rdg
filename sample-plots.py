from plots import *

# Load exact classical data
classical_data = load_data("classical-exact.txt")
rdg_plot(classical_data, dx=0.001, dy=0.001, show=True)

# Calculate majority vote probabilities
maj3_data = classical_data**3 + 3*classical_data**2 * (1-classical_data)
rdg_plot(maj3_data, dx=0.001, dy=0.001, show=True)

# See how much majority vote performs better than single-shot measurement
compare_plots(classical_data, maj3_data, dx=0.001, dy=0.001, filename="compare.png", show=True)
# Comparison using error probabilities
compare_plots(1-maj3_data, 1-classical_data, dx=0.001, dy=0.001, scalelabel="Log error ratio", show=True)

# Load QSP-3 data
qsp3_data = load_data("qsp-3-data.txt")
rdg_plot(qsp3_data, dx=0.001, dy=0.001, show=True)

# Compare QSP-3 with MAJ-3
compare_plots(maj3_data, qsp3_data, dx=0.001, dy=0.001, filename="advantage-success.png", show=True)
compare_plots(1-qsp3_data, 1-maj3_data, dx=0.001, dy=0.001, filename="advantage-error.png", show=True)
