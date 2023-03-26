"""
This module will check the 'old_alternative_projects' folder
hourly to see if there are new files or folders. If there are
and they're part of a blacklist of spurious files, mainly git
and logs, cache, that sort of thing, they'll be deleted.
"""
import os
import pickle
from os import walk

import snoop
from db_decorator.db_information import db_information

# import subprocess
from rocketry import Rocketry
from rocketry.conds import hourly
from snoop import pp


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])

app = Rocketry()


# @app.task(hourly)
@db_information
@snoop
def file_checker():
    """"""
    del_dir = [".git", "logs", "build", "__pycache__"]
    del_file = [
        ".gitignore",
        ".gitconfig",
        "LICENSE",
        "MANIFEST.in",
        "pyproject.toml",
        "setup.py",
        "setup.cfg",
        "__init__.py",
    ]
    pth = "/home/mic/python/old_alternative_projects"

    folder_content = []
    for root, dirs, files in walk(pth):
        for file in files:
            folder_content.append(os.path.join(root, file))

    with open("snapshot.bin", "wb") as f:
        pickle.dump(folder_content, f)


if __name__ == "__main__":
    file_checker()
    # app.run()
