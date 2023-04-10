"""
This module will check the 'old_alternative_projects' folder
hourly to see if there are new files or folders. If there are
and they're part of a blacklist of spurious files, mainly git
and logs, cache, that sort of thing, they'll be deleted.
"""
import os
import shutil

# import snoop
# from snoop import pp


# def type_watch(source, value):
#   return "type({})".format(source), type(value)


# snoop.install(watch_extras=[type_watch])


# @snoop
def file_checker():
    """
    Checks if folder has files or subfolders in to delete lists.
    Is called hourly by a cron job with root permissions.
    """

    del_dir = [".git", "logs", "build", "__pycache__"]
    del_file = [
        ".gitignore",
        ".gitconfig",
        "LICENSE",
        "MANIFEST.in",
        "pyproject.toml",
        "setup.py",
        "__init__.py",
    ]
    pth = "/home/mic/python/old_alternative_projects"

    folder_content = []
    # os.walk will look in all sublevels of the dir tree for files or folders.
    for root, dirs, files in os.walk(pth):
        folder_content.extend(os.path.join(root, file) for file in files + dirs)
    # 'del_dir' and 'del_files' list only names not paths. As folder_content collects paths,
    # we have to use 'os.path.basename(os.path.normpath())' to get only the names of files and folders.
    deletes = [i for i in folder_content if os.path.basename(os.path.normpath(i)) in del_dir or os.path.basename(os.path.normpath(i)) in del_file]

    if deletes != []:
        for d in deletes:
            if os.path.isdir(d):
                # Only 'shutil.rmtree()', in python, deletes folders with files in it.
                shutil.rmtree(d)
            else:
                os.remove(d)


if __name__ == "__main__":
    file_checker()
