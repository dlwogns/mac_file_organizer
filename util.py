import os
import time

def is_download_complete(file_path, check_interval=1, stable_count=2):
    prev_size = -1
    same_count = 0

    while same_count < stable_count:
        try:
            current_size = os.path.getsize(file_path)
        except OSError:
            return False # File might not exist or be accessible

        if current_size == prev_size:
            same_count += 1
        else:
            same_count = 0

        prev_size = current_size
        time.sleep(check_interval)

    return True  # File size is stable, indicating download completion