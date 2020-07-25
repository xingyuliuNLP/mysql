import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import os


def on_created(event):
    print(f"{event.src_path} has been created")
    os.system(f"git add {event.src_path}")
    os.system(f"git commit -m '{event.src_path} created'")
    os.system("git push origin master")


def on_deleted(event):
    print(f"Delete {event.src_path}!")
    os.system(f"git commit -m '{event.src_path} modified'")
    os.system("git push origin master")


def on_modified(event):
    print(f"{event.src_path} has been modified")
    os.system(f"git commit -m '{event.src_path} deleted'")
    os.system("git push origin master")


# create the event handler
if __name__ == "__main__":
    patterns = ""
    # ignore_patterns = ".git"
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(ignore_patterns=[".git"])
    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted
    my_event_handler.on_modified = on_modified

# create an observer
    path = "."
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)

    my_observer.start()
    try:
        while True:
            time.sleep(5)
    except:
        my_observer.stop()
    my_observer.join()
