import os
import shutil

def rename_file(old_path, new_name):
    """Rename a file."""
    try:
        dirname = os.path.dirname(old_path)
        new_path = os.path.join(dirname, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed '{old_path}' to '{new_path}'")
        return new_path
    except Exception as e:
        print(f"Error renaming file: {e}")
        return None

def delete_file(file_path):
    """Delete a file."""
    try:
        os.remove(file_path)
        print(f"Deleted '{file_path}'")
    except Exception as e:
        print(f"Error deleting file: {e}")

def move_file(file_path, dest_dir):
    """Move a file to another directory."""
    try:
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        
        filename = os.path.basename(file_path)
        dest_path = os.path.join(dest_dir, filename)
        
        # Handle name conflicts
        counter = 1
        while os.path.exists(dest_path):
            name, ext = os.path.splitext(filename)
            dest_path = os.path.join(dest_dir, f"{name}_{counter}{ext}")
            counter += 1
        
        shutil.move(file_path, dest_path)
        print(f"Moved '{file_path}' to '{dest_path}'")
        return dest_path
    except Exception as e:
        print(f"Error moving file: {e}")
        return None

def cross_directory_duplicate_check(main_files, other_files):
    """Check for duplicates between two file lists."""
    from hasher import compute_file_hash
    
    # Create hash map for main files
    main_hashes = {}
    for file in main_files:
        file_hash = compute_file_hash(file['path'])
        if file_hash:
            main_hashes[file_hash] = file
    
    # Check other files against main hashes
    duplicates = []
    for file in other_files:
        file_hash = compute_file_hash(file['path'])
        if file_hash in main_hashes:
            duplicates.append((main_hashes[file_hash], file))
    
    return duplicates