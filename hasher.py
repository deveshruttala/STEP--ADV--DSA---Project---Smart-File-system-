import hashlib
import os

def compute_file_hash(file_path, chunk_size=8192):
    """Compute SHA-256 hash of a file's contents."""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        print(f"Error hashing {file_path}: {e}")
        return None

def find_duplicates(file_list):
    """Find duplicate files based on content hash."""
    hash_groups = {}
    for file in file_list:
        file_hash = compute_file_hash(file['path'])
        if file_hash:
            if file_hash not in hash_groups:
                hash_groups[file_hash] = []
            hash_groups[file_hash].append(file)
    
    # Filter to only groups with duplicates
    return {h: files for h, files in hash_groups.items() if len(files) > 1}

def mark_duplicates(duplicates):
    """Mark duplicate files by adding '_dup' to their names."""
    marked_files = []
    for files in duplicates.values():
        # Keep the first file as original, mark others
        for file in files[1:]:
            try:
                dirname, filename = os.path.split(file['path'])
                name, ext = os.path.splitext(filename)
                new_path = os.path.join(dirname, f"{name}_dup{ext}")
                os.rename(file['path'], new_path)
                marked_files.append(new_path)
            except Exception as e:
                print(f"Error marking {file['path']}: {e}")
    return marked_files