import pandas as pd
from zipfile import ZipFile
import sqlite3
from python_utils import DATA_DIR, DB_DIR
import os


def get_sleeps(data: list[str]) -> list[list[str]]:
    while len(data) > 0:
        i = 2 if data[2].startswith("Id") else 3

        sleep, data = data[:i], data[i:]
        yield [
            list(map(lambda y: y.replace('"', "").replace("\n", ""), x.split(",")))
            for x in sleep
        ]


save_to_db = True

with ZipFile(os.path.join(DATA_DIR, "sleep-export.zip")) as my_zip:
    with my_zip.open("sleep-export.csv", "r") as f:
        lines = list(map(lambda x: x.decode("utf-8"), f.readlines()))

sleep_data = []
event_data = []
for sleep in get_sleeps(lines):
    sleep_data.append(sleep[1][:15])

    for time, mov_value in zip(sleep[0][15:], sleep[1][15:]):
        event_data.append([sleep[1][0], time, mov_value])


headers = sleep[0][:15]

sleep_df = pd.DataFrame(sleep_data, columns=headers)
event_df = pd.DataFrame(event_data, columns=["Id", "Time", "Value"])
movement_df = event_df[event_df["Time"] != "Event"]
event_df = event_df[event_df["Time"] == "Event"][["Id", "Value"]].rename(
    columns={"Value": "Event"}
)

for col in ("From", "To", "Sched"):
    sleep_df[col] = pd.to_datetime(sleep_df[col], format="%d. %m. %Y %H:%M")

for col in (
    "Id",
    "Hours",
    "Rating",
    "DeepSleep",
    "Framerate",
    "Snore",
    "Noise",
    "Cycles",
    "LenAdjust",
):
    sleep_df[col] = pd.to_numeric(sleep_df[col])

sleep_df = sleep_df.rename(columns={old: old.lower() for old in sleep_df.columns})
sleep_df = sleep_df.rename(columns={"from": "sleep_from", "to": "sleep_to"})

# Parse tags in comments
sleep_df["tags"] = sleep_df["comment"].str.findall(r"#([a-z0-9]*)").str.join(",")

for col in ("Id", "Value"):
    movement_df[col] = pd.to_numeric(movement_df[col])

movement_df["Time"] = pd.to_datetime(movement_df["Time"], format="%H:%M").dt.time

movement_df = movement_df.rename(
    columns={old: old.lower() for old in movement_df.columns}
)

event_df["Id"] = pd.to_numeric(event_df["Id"])

event_df = event_df.rename(columns={old: old.lower() for old in event_df.columns})

sleep_df.to_csv(os.path.join(DATA_DIR, "clean/sleeps.csv"), index=False)
movement_df.to_csv(os.path.join(DATA_DIR, "clean/movements.csv"), index=False)
event_df.to_csv(os.path.join(DATA_DIR, "clean/events.csv"), index=False)

con = sqlite3.connect(os.path.join(DB_DIR, "raw.db"))

con.execute("DROP TABLE IF EXISTS sleeps;")
con.execute("DROP TABLE IF EXISTS movements;")
con.execute("DROP TABLE IF EXISTS events;")

sleep_df.to_sql("sleeps", con, index=False)
movement_df.to_sql("movements", con, index=False)
event_df.to_sql("events", con, index=False)
