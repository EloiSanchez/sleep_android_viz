import sqlite3
import os

# Get the database directory independent of the path where the script executes
file_path = os.path.realpath(__file__)
db_dir = os.path.os.path.join(file_path, "../../../database/")

SCHEMAS = ("staging", "intermediate", "final")

for schema in SCHEMAS:
    con = sqlite3.connect(os.path.join(db_dir, schema + ".db"))
    cur = con.cursor()

    res = cur.execute(
        """SELECT type, name FROM sqlite_schema
           WHERE type in ('table', 'view')
           AND name NOT LIKE 'sqlite_%';"""
    )

    for obj_type, name in res.fetchall():
        cur.execute(f"""DROP {obj_type} {name}""")

    con.commit()
    con.close()
