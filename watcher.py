import os
import shutil
import threading
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FolderEventHandler(FileSystemEventHandler):
    def __init__(self, log_callback, bracket_rule, ignore_exts):
        super().__init__()
        self.log_callback = log_callback
        self.bracket_rule = bracket_rule
        self.ignore_exts = ignore_exts

    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        filename = os.path.basename(file_path)
        ext = os.path.splitext(filename)[1].lower()

        if ext in self.ignore_exts:
            self.log_callback(f"❌ 무시됨: {filename}")
            return

        if self.bracket_rule and filename.startswith('['):
            try:
                folder_name = filename.split(']')[0][1:]
                rest_name = filename.split(']')[1]
                dest_dir = os.path.expanduser(f"~/Desktop/{folder_name}")
                os.makedirs(dest_dir, exist_ok=True)
                dest_path = os.path.join(dest_dir, rest_name)
                shutil.move(file_path, dest_path)
                self.log_callback(f"✅ {filename} → {dest_dir}")
            except Exception as e:
                self.log_callback(f"⚠️ 이동 실패: {filename} ({e})")
        else:
            self.log_callback(f"ℹ️ 감지됨: {filename}")


class FolderWatcherThread(threading.Thread):
    def __init__(self, folder_list, log_callback, bracket_rule, ignore_exts):
        super().__init__()
        self.folder_list = folder_list
        self.log_callback = log_callback
        self.bracket_rule = bracket_rule
        self.ignore_exts = ignore_exts
        self.stop_flag = threading.Event()
        self.observers = []

    def run(self):
        event_handler = FolderEventHandler(
            self.log_callback, self.bracket_rule, self.ignore_exts)
        for folder in self.folder_list:
            observer = Observer()
            observer.schedule(event_handler, folder, recursive=False)
            observer.start()
            self.observers.append(observer)
            self.log_callback(f"👀 감시 시작: {folder}")

        try:
            while not self.stop_flag.is_set():
                time.sleep(1)
        finally:
            for observer in self.observers:
                observer.stop()
                observer.join()
            self.log_callback("🛑 감시 종료")

    def stop(self):
        self.stop_flag.set()
