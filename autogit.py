import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

class OnMyWatch:
    # Set the directory on watch
    watchDirectory = "."

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(
            event_handler, self.watchDirectory, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod # a static method can be called without an object for that class. This also means that static methods cannot modify the state of an object as they are not bound to it
    def on_any_event(event):
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            # Event is created, you can process it now
            print(f"Watchdog received created event - {event.src_path}")
            os.system(f"git commit -m '{event.src_path} created'")
            os.system("git push origin master")
        elif event.event_type == 'modified':
            # Event is modified, you can process it now
            print(f"Watchdog received modified event - {event.src_path}")
            os.system(f"git commit -m '{event.src_path} modified'")
            os.system("git push origin master")
        elif event.event_type == 'deleted':
            print(f"Watchdog received deleted event - {event.src_path}")
            os.system(f"git commit -m 'delete {event.src_path}'")
            os.system("git push origin master")



if __name__ == '__main__':
    watch = OnMyWatch()
    watch.run()
