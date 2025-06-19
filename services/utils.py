import time
import os


def clean_old_files(folder_path: str, max_age_seconds: int = 86400):
    now = time.time()
    for fname in os.listdir(folder_path):
        fpath = os.path.join(folder_path, fname)
        if os.path.isfile(fpath):
            file_age = now - os.path.getmtime(fpath)
            if file_age > max_age_seconds:
                print(f"Removing {fname} (age: {file_age} sec)")
                try:
                    os.remove(fpath)
                except Exception as e:
                    print(f"Error removing file {fpath}: {e}")
