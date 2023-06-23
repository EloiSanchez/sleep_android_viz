import os
import sys

import plotly

import importlib

# TODO: This is super weird for me. Is there a better solution?
# Let me know at eloisanchez16@gmail.com
sys.path.append(".")
sys.path.append("./plots")


TEST_DIR = os.path.dirname(__file__)
PLOT_DIR = os.path.os.path.join(TEST_DIR, "../../plots/")

# get name of all python plots in the plots directory
modules = [
    x.split(".")[0]
    for x in filter(
        lambda module: module != "utils.py"
        and not os.path.isdir(os.path.join(PLOT_DIR, module)),
        os.listdir(PLOT_DIR),
    )
]

# import al python plots found
plots = []
for module in modules:
    plots.append(importlib.import_module(module))


def test_plot_dir() -> None:
    assert os.path.exists(PLOT_DIR)


def test_plots() -> None:
    for plot in plots:
        assert type(plot.make_plot(testing=True)) == plotly.graph_objs.Figure
