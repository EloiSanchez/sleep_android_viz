import pandas as pd
import sqlite3
import os

from python_utils import FINAL_TABLES_EXPORT_DIR, FINAL_TABLES_DIR


def main():
    tables = [x.split(".")[0] for x in os.listdir(FINAL_TABLES_DIR)]

    for table in tables:
        con = sqlite3.connect("database/final.db")
        df = pd.read_sql(f"select * from {table}", con)

        df.to_csv(os.path.join(FINAL_TABLES_EXPORT_DIR, f"{table}.csv"), index=False)


if __name__ == "__main__":
    main()
