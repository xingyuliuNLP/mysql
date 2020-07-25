import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os


class _Handler(FileSystemEventHandler):
    def on_any_event(self, event):
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


if __name__ == "__main__":
    ## create the event handler
    my_event_handler = _Handler()

    ## create an observer
    path = "."
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=True)


    my_observer.start()
    try:
        while True:
            time.sleep(5)
    except:
        my_observer.stop()
    my_observer.join()