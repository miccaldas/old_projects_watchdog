from time import sleep

import requests
import snoop
from snoop import pp
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])


class WatchCronlog:
    """
    Set 'cronlogs' as the directory
    to watch.
    """

    watchDirectory = "/home/mic/cronlogs"

    def __init__(self):
        self.observer = Observer()

    # @snoop
    def run(self):
        """
        Runs the handler class.
        """
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDirectory, recursive=False)
        self.observer.start()
        try:
            while True:
                sleep(10)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()


class Handler(FileSystemEventHandler):
    """
    Defines event to be monitord and what
    to do when it happens.
    """

    def __init__(self):
        self.path = "/home/mic/cronlogs/old_watchdog.txt"

    @snoop
    def on_modified(self, event):
        """
        Sends the output of the watchdog cronlog as a attachment
        to my phone via ntfy.
        """
        if self.path == event.src_path:
            requests.put(
                "https://ntfy.sh/mic",
                data=open("/home/mic/cronlogs/old_watchdog.txt", "r"),
                headers={
                    "Title": "Old Projects watchdog has run.",
                    "Filename": "old_watchdog.txt",
                },
            )


if __name__ == "__main__":
    watch = WatchCronlog()
    watch.run()
