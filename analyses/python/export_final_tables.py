import pandas as pd
import sqlite3
import os


def main():
    SCRIPT_DIR = os.path.dirname(__file__)
    TABLES_DIR = os.path.join(SCRIPT_DIR, "../../models/main/sql/")
    EXPORT_DIR = os.path.join(SCRIPT_DIR, "../../data/final_tables/")

    tables = [x.split(".")[0] for x in os.listdir(TABLES_DIR)]

    for table in tables:
        con = sqlite3.connect("database/final.db")
        df = pd.read_sql(f"select * from {table}", con)

        df.to_csv(os.path.join(EXPORT_DIR, f"{table}.csv"), index=False)


if __name__ == "__main__":
    main()
