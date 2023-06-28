import os


SCRIPT_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))
DB_DIR = os.path.os.path.join(PROJECT_DIR, "database/")
FINAL_TABLES_DIR = os.path.join(PROJECT_DIR, "models/main/sql/")
FINAL_TABLES_EXPORT_DIR = os.path.join(PROJECT_DIR, "data/final_tables/")
PLOTS_DIR = os.path.join(PROJECT_DIR, "plots/")
