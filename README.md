# Sleep Android Vizualization

Open [dashboard](http://revolutionarypingu.pythonanywhere.com/)!

## Summary

This is a learning project on [dbt Core](https://www.getdbt.com/). It was made while working at [Nimbus Intelligence](https://nimbusintelligence.com/) as an Analytics Engineer. The end result can be seen in the following dashboard.

The data comes from the [Sleep as Android](https://sleep.urbandroid.org/) app. Check the [usage](#usage) section to see how you can visualize your data. After an initial parsing of the csv file, the data is stored in a local [SQLite](https://www.sqlite.org/index.html) database and transformed using dbt Core, from raw tables to end tables.

The end tables are queried using [Pandas](https://pandas.pydata.org/) and the graphs and dashboard were built using [Plotly](https://plotly.com/) and [Dash](https://dash.plotly.com/).

A more detailed description can be seen in the [tools](#tools) section, and **the end result** can be seen in this [dashboard](http://revolutionarypingu.pythonanywhere.com/).

## Usage

### Set up

Create a new environment (using venv, conda, pyenv...) and activate it. For instance, using conda

```bash
conda create -n sleep_dash python=3.11
conda activate sleep_dash
```

Install the dependencies

```bash
pip install -r requirements.txt
```

Put your [zip file](https://docs.sleep.urbandroid.org/devs/csv.html) exported from the app in the `data` folder with the name `sleep-export.zip`.

#### For developers

Install pre-commit and set it up

```bash
pip install pre-commit
pre-commit install
```


### Commands

Run everything executes several commands that takes the raw csv data and transforms it until it gets to final tables that are used by plotly to create plots and a dashboard.

```bash
python analyses/python/run_all.py
```

Parses raw csv file from `data/sleep-export.zip` and stores clean csv files in `data/clean` and in tables in `database/raw.db`.

```bash
python analyses/python/parse_csv.py
```

Transform data from `database/raw.db` until it gets to final clean and usable tables for plots.

```bash
dbt build
```

Export final tables from the `final.db` schema into csv files in `data/final_tables/`

```bash
python analyses/python/export_final_tables.py
```

Creates plots from the final tables in `final.db` and stores them as html and png in `plots/figures/`.

```bash
python analyses/python/make_plots.py
```

Remove all data from the database

```bash
python analyses/python/drop_all.py
```

Run pytest

```bash
pytest tests/pytest/
```

## Tools

### Sleep as Android

The data is provided by [Sleep as Android](https://sleep.urbandroid.org/), an Android app that I have used since 2019. Currently, it has data up until June of 2023.

### Database

I decided to use [sqlite3](https://docs.python.org/3/library/sqlite3.html) for several reasons:

- It is a free and lightweight database with an easy out-of-the-box implementation in Python. My focus on this project was not on database management, but on the transformation of data from raw to processed.
- A community connector exists that allows it to make it work with dbt.
- Since the amount of data is not massive I would rather have it saved locally than in a cloud environment. It is easier and I do not have to worry about anything breaking in the future. The database will forever be stored in the GitHub repository together with the rest of scripts and files.

### Orchestration / Data transformation

As an Analytics Engineer at Nimbus Intelligence, we use [dbt](https://www.getdbt.com/) as an orchestration tool on top of the Snowflake database. Our training was solely on dbt Cloud, which includes lots of interesting functionalities but removes the flexibility a developer has on its own machine.

I decided to use dbt Core, the local and open source version of dbt, in order to exploit the extra capabilites that a developer has when setting up a development environment. At that time, I was recently introduce to [pre-commits](https://pre-commit.com/) and I decided to implement them on the CI pipeline. Since I found them quite useful, I decided to introduce them to my co-workers in a [presentation](https://docs.google.com/presentation/d/1e-bOI0T_V2jqbS6qpqiwXyaFyK4DCZ_HCYw1GKAxOHI/edit#slide=id.g253778cc31b_0_484)

### Data Cleaning and Plots

I am not super good with data visualization. At Nimbus Intelligence we received some minor introduction on Tableau, but mainly to understand how the people in the data analysis team worked to better adapt our work to them. I stuck with [Python](https://www.python.org/) for these two processes because it is the tool I am most comfortable with.

I wanted to create some nice and somewhat interactive plots which could then maybe be extended to a cute little dashboard. Since I did not want just plain png pictures, I decided to go with [plotly](https://plotly.com/) for the visualizations. One of the nice features of plotly is that it allows exporting to html, which retains some minor interactivity in the plots by default. Also, the [Plotly Express API](https://plotly.com/python/plotly-express/) is called in a way that reminds me to the [ggplot2](https://ggplot2.tidyverse.org/) Grammar of Graphics, which I really like.

The data cleaning process was relatively straightforward. A csv file can be exported from the app itself, thought this csv file cannot be read by the usual csv parsers because of the unique way of providing data that Sleep as Android use. Therefore, a Python script to read and store the data to the raw schema in the database was created.

### Dashboard

I have previously used Streamlit in some projects in order to create front-ends for visualizations, but since I was using Plotly for this project, I decided to try out Plotly Dash.

The result is a [dashboard](http://revolutionarypingu.pythonanywhere.com/) that includes some of the plots I built with plotly.
