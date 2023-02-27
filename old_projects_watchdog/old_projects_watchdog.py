"""
The 'old_alternative_projects' is a directory for code that can be reused.
When sending a package to this directory, all package related files are
not needed anymore and should be deleted.'
"""
import os
import subprocess
from time import sleep

import isort
import snoop
from snoop import pp
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])


class WatchOldAlternative:
    """
    Set 'old_alternative_projects' as the directory
    to watch.
    """

    watchDirectory = "/home/mic/python/old_alternative_projects"

    def __init__(self):
        self.observer = Observer()

    # @snoop
    def run(self):
        """
        Runs the handler class.
        """
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDirectory, recursive=True)
        self.observer.start()
        try:
            while True:
                sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()


class Handler(FileSystemEventHandler):
    """
    Defines event to be monitored and
    what to do when it happens.
    """

    @staticmethod
    def on_created(event):
        if event.is_directory:
            pth = event.src_path
            tail = os.path.basename(os.path.normpath(pth))
            del_dir = [".git", "logs", "build", "__pycache__"]
            if tail in del_dir:
                cmd = f"/usr/bin/trash-put {pth}"
                subprocess.run(cmd, shell=True)
            if tail.endswith("egg-info"):
                subprocess.run(cmd, shell=True)
        if event.is_file:
            path = event.src_path
            tail = os.path.basename(os.path.normpath(path))
            del_file = [".gitignore", ".gitconfig", "LICENSE", "MANIFEST.in", "pyproject.toml", "setup.py", "setup.cfg", "__init__.py"]
            cmd = f"/usr/bin/trash-put {path}"
            if tail in del_file:
                subprocess.run(cmd, shell=True)


if __name__ == "__main__":
    watch = WatchOldAlternative()
    watch.run()
