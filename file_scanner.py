import os
import datetime

def get_file_metadata(file_path):
    
    return {
        'name': os.path.basename(file_path),
        'size': os.path.getsize(file_path),
        'modified': datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
        'path': file_path,
        'extension': os.path.splitext(file_path)[1].lower(),

    }

def scan_directory(directory_path):
    all_files_metadata = []

    for dirpath, _, filenames in os.walk(directory_path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            try:
                metadata = get_file_metadata(full_path)
                all_files_metadata.append(metadata)
            except Exception as e:
                print(f"[ERROR] {full_path}: {e}")

    return all_files_metadata

if __name__ == "__main__":
    import json
    directory = input("Enter the directory path to scan: ").strip()
    if not os.path.isdir(directory):
        print("Invalid directory path.")
    else:
        metadata_list = scan_directory(directory) 
        print(metadata_list)
