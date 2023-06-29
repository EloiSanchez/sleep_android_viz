import os
from python_utils import PROJECT_DIR, SCRIPT_DIR

# Go to parent directory
os.chdir(PROJECT_DIR)

# Clean database
print("Cleaning database")
os.system(f"python {os.path.join(SCRIPT_DIR, 'drop_all.py')}")

# Build database
os.system(f"dbt build")

# Export final tables to csv
print("Exporting final tables")
os.system(f"python {os.path.join(SCRIPT_DIR, 'export_final_tables.py')}")

# Build plots
print("Building plots")
os.system(f"python {os.path.join(SCRIPT_DIR, 'make_plots.py')}")
