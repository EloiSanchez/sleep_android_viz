import sqlite3
import os

from python_utils import DB_DIR

SCHEMAS = ("seeds", "staging", "intermediate", "final")

for schema in SCHEMAS:
    con = sqlite3.connect(os.path.join(DB_DIR, schema + ".db"))
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
