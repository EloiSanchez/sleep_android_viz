import os
import sys

import plotly

# TODO: This is super weird for me. Is there a better solution?
# Let me know at eloisanchez16@gmail.com
sys.path.append(".")
sys.path.append("./plots")

from plots import schedule_by_year_month, duration_by_month


TEST_DIR = os.path.dirname(__file__)
PLOT_DIR = os.path.os.path.join(TEST_DIR, "../../plots/")


def test_plot_dir() -> None:
    assert os.path.exists(PLOT_DIR)


def test_plots() -> None:
    plots = [duration_by_month, schedule_by_year_month]
    for plot in plots:
        assert type(plot.make_plot(testing=True)) == plotly.graph_objs.Figure
