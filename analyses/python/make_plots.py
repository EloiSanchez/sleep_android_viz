import os
import importlib

from python_utils import PLOTS_DIR

import sys

# TODO: This is super weird for me. Is there a better solution?
# Let me know at eloisanchez16@gmail.com
sys.path.append(".")
sys.path.append("./plots")

dirlist = os.listdir(PLOTS_DIR)

for plot in [
    x
    for x in dirlist
    if (not os.path.isdir(os.path.join(PLOTS_DIR, x)) and x != "utils.py")
]:
    module = importlib.import_module(plot.split(".")[0])
    print(f"Plotting from {module=}")
    module.make_plot()
