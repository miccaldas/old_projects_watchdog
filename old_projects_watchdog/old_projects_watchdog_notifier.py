"""
Sends notification when old_projects_watchdogs runs.
"""

import inspect
import os
import pickle

import requests
import snoop
from snoop import pp


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(out="snoop.log", overwrite=True, watch_extras=[type_watch])


@snoop
def notifier():
    """
    Sends a ntfy notification to my phone
    everytime the watchdog cronlog is
    altered.
    """

    path = "/home/mic/cronlogs/old_watchdog.txt"
    # This os command registers when the file was last altered.
    last_alt = os.path.getmtime(path)
    pick_folder = "/home/mic/cronlogs/last_alterations_files/"
    file_paths = [f"{pick_folder}{i.strip()}" for i in os.listdir(pick_folder)]
    alt_file = f"{pick_folder}watchdog_last_at.bin"
    if alt_file in file_paths:
        with open(alt_file, "rb") as f:
            altf = pickle.load(f)
            if altf != last_alt:
                requests.put(
                    "https://ntfy.sh/mic",
                    data=open(path, "r"),
                    headers={"title": "Watchdog", "filename": "watchdog.py"},
                )
                with open(alt_file, "wb") as f:
                    pickle.dump(last_alt, f)
    else:
        with open(alt_file, "wb") as f:
            pickle.dump(last_alt, f)
    print(f"{inspect.currentframe().f_code.co_name} has run.")


if __name__ == "__main__":
    notifier()
