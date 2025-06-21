import os
import shutil
from hasher import compute_hash

def rename_file(file_path, new_name):
    directory = os.path.dirname(file_path)
    new_path = os.path.join(directory, new_name)
    try:
        os.rename(file_path, new_path)
        print(f"Renamed: {file_path} -> {new_path}")
        return new_path
    except Exception as e:
        print(f"[ERROR] Rename failed: {e}")
        return None

def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"Deleted: {file_path}")
    except Exception as e:
        print(f"[ERROR] Delete failed: {e}")

def move_file(file_path, destination_dir):
    try:
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        new_path = os.path.join(destination_dir, os.path.basename(file_path))
        shutil.move(file_path, new_path)
        print(f"Moved: {file_path} -> {new_path}")
        return new_path
    except Exception as e:
        print(f"[ERROR] Move failed: {e}")
        return None

def mark_duplicate(file_path):
    directory, filename = os.path.split(file_path)
    name, ext = os.path.splitext(filename)
    new_name = f"{name}_DUPLICATE{ext}"
    return rename_file(file_path, new_name)

def cross_directory_duplicate_check(main_files, other_directory):
    from file_scanner import scan_directory
    other_files = scan_directory(other_directory)
    other_hashes = {compute_hash(f['path']): f for f in other_files if compute_hash(f['path'])}

    duplicates = []
    for f in main_files:
        f_hash = compute_hash(f['path'])
        if f_hash in other_hashes:
            duplicates.append((f, other_hashes[f_hash]))
    return duplicates
