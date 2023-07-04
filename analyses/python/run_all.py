import os
from python_utils import PROJECT_DIR, SCRIPT_DIR, PLOTS_DIR


# Go to parent directory
os.chdir(PROJECT_DIR)


# Clean database
print("Parsing data")
error = os.system(f"python {os.path.join(SCRIPT_DIR, 'parse_csv.py')}")

if error != 0:
    raise SystemError(f"Error while parsing csv file. Exit code {error}")


# Build database
error = os.system(f"dbt build")

if error != 0:
    raise SystemError(f"Error while building dbt. Exit code {error}")


# Export final tables to csv
print("Exporting final tables")
error = os.system(f"python {os.path.join(SCRIPT_DIR, 'export_final_tables.py')}")

if error != 0:
    raise SystemError(f"Error while exporting final tables to csv. Exit code {error}")


# Build plots
print("Building plots")
error = os.system(f"python {os.path.join(SCRIPT_DIR, 'make_plots.py')}")

if error != 0:
    raise SystemError(f"Error while building plots. Exit code {error}")

print("Opening Dashboard")
error = os.system(f"python {os.path.join(PLOTS_DIR, 'dashboards/main.py')}")

if error != 0:
    raise SystemError(f"Error while opening the dashboard. Exit code {error}")
