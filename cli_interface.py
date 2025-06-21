import os
from file_scanner import scan_directory
from sorter import sort_files
from hasher import find_duplicates, mark_duplicates
from searcher import search_files
from file_operations import (
    rename_file, delete_file, move_file,
    cross_directory_duplicate_check
)
from batcher import batch_files_by_extension, batch_files_by_size


def display_menu():
    print("\n==== Smart File Organizer CLI ====")
    print("1. Sort files")
    print("2. Find duplicate files")
    print("3. Manage duplicates")
    print("4. Search files")
    print("5. File operations")
    print("6. Batch files by extension")
    print("7. Batch files by size")
    print("8. List all files")
    print("9. Check duplicates across directories")
    print("10. Rescan directory")
    print("0. Exit")
    print("===================================")

def get_sort_key():
    print("\nSort by:")
    print("1. Name")
    print("2. Size")
    print("3. Date modified")
    print("4. Extension")
    choice = input("Select sort key (1-4): ").strip()
    return {
        '1': 'name',
        '2': 'size',
        '3': 'date',
        '4': 'extension'
    }.get(choice, 'name')

def handle_sorting(file_list):
    sort_key = get_sort_key()
    sorted_files = sort_files(file_list, [sort_key])
    print(f"\n[SORTED BY {sort_key.upper()}]")
    for f in sorted_files:
        print(f"{f['name']} ({f['size']} bytes) - {f['date']}")

def handle_duplicates(file_list, directory):
    duplicates = find_duplicates(file_list)
    if not duplicates:
        print("No duplicates found.")
        return {}
    
    print("\n[DUPLICATE FILES]")
    for i, (hash_val, files) in enumerate(duplicates.items(), 1):
        print(f"\nDuplicate Set #{i} (Hash: {hash_val[:8]}...)")
        for j, file in enumerate(files, 1):
            print(f"{j}. {file['path']}")

    return duplicates

def handle_duplicate_management(duplicates, file_list, directory):
    if not duplicates:
        print("No duplicates to manage.")
        return file_list
        
    print("\nDuplicate Management Options:")
    print("1. Mark duplicates for later action")
    print("2. Delete all duplicates")
    print("3. Move duplicates to another directory")
    choice = input("Select action (1-3): ").strip()

    if choice == "1":
        marked_files = mark_duplicates(duplicates)
        print(f"{len(marked_files)} files marked as duplicates.")
    elif choice == "2":
        confirm = input("Delete ALL duplicates? This cannot be undone! (y/N): ").lower()
        if confirm == 'y':
            deleted = 0
            for files in duplicates.values():
                # Keep first file, delete others
                for file in files[1:]:
                    try:
                        delete_file(file['path'])
                        deleted += 1
                    except Exception as e:
                        print(f"Error deleting {file['path']}: {e}")
            print(f"Deleted {deleted} duplicate files.")
            return scan_directory(directory)
    elif choice == "3":
        dest = input("Enter destination directory: ").strip()
        if os.path.isdir(dest):
            moved = 0
            for files in duplicates.values():
                for file in files[1:]:
                    try:
                        move_file(file['path'], dest)
                        moved += 1
                    except Exception as e:
                        print(f"Error moving {file['path']}: {e}")
            print(f"Moved {moved} duplicate files to {dest}.")
            return scan_directory(directory)
        else:
            print("Invalid directory.")
    else:
        print("Invalid choice.")

    return file_list


def handle_list_files(file_list):
    print("\n[ALL FILES IN DIRECTORY]")
    print(f"Total files: {len(file_list)}")
    for i, file in enumerate(file_list, 1):
        print(f"{i}. {file['name']} ({file['size']} bytes) - {file['date']}")
    print("\nEnter file number to view details, or press Enter to return.")
    selection = input("Selection: ").strip()
    
    if selection.isdigit() and 1 <= int(selection) <= len(file_list):
        selected = file_list[int(selection)-1]
        print("\n[FILE DETAILS]")
        print(f"Name: {selected['name']}")
        print(f"Size: {selected['size']} bytes")
        print(f"Modified: {selected['date']}")
        print(f"Path: {selected['path']}")
        print(f"Extension: {selected['extension']}")



def handle_file_operations():
    path = input("Enter full file path to modify: ").strip()
    if not os.path.exists(path):
        print("File does not exist.")
        return

    print("\nFile Operations:")
    print("1. Rename")
    print("2. Delete")
    print("3. Move")
    action = input("Select action (1-3): ").strip()

    if action == "1":
        new_name = input("Enter new name for the file (with extension): ").strip()
        rename_file(path, new_name)
    elif action == "2":
        confirm = input("Are you sure you want to delete this file? (y/N): ").lower()
        if confirm == 'y':
            delete_file(path)
    elif action == "3":
        destination = input("Enter destination directory: ").strip()
        if os.path.isdir(destination):
            move_file(path, destination)
        else:
            print("Invalid directory.")
    else:
        print("Invalid action.")

def handle_batch_by_extension(file_list):
    batches = batch_files_by_extension(file_list)
    print("\n[FILES BATCHED BY EXTENSION]")
    for ext, files in batches.items():
        print(f"\nExtension: {ext or 'No Extension'} ({len(files)} files)")
        for f in files[:5]:  # Show first 5 files per batch
            print(f"  {f['name']} ({f['size']} bytes)")
        if len(files) > 5:
            print(f"  ...and {len(files)-5} more")

def handle_batch_by_size(file_list):
    batches = batch_files_by_size(file_list)
    print("\n[FILES BATCHED BY SIZE]")
    for size_range, files in sorted(batches.items()):
        print(f"\nSize Range: {size_range} ({len(files)} files)")
        for f in files[:3]:  # Show first 3 files per batch
            print(f"  {f['name']} ({f['size']} bytes)")
        if len(files) > 3:
            print(f"  ...and {len(files)-3} more")



def run_cli():
    print("=== Smart File Organizer ===")
    
    # Input valid directory
    while True:
        directory = input("Enter directory to organize: ").strip()
        if os.path.isdir(directory):
            break
        print("Invalid directory path. Try again.")

    # Initial scan
    file_list = scan_directory(directory)
    print(f"Found {len(file_list)} files in directory.")
    
    while True:
        display_menu()
        choice = input("Select an option (0-10): ").strip()

        if choice == "1":
            handle_sorting(file_list)
        elif choice == "2":
            duplicates = handle_duplicates(file_list, directory)
        elif choice == "3":
            
            duplicates = handle_duplicates(file_list, directory)
            if duplicates:  # Only proceed if duplicates were found
                file_list = handle_duplicate_management(duplicates, file_list, directory)
        elif choice == "4":
            pattern = input("Enter search pattern: ").strip()
            if pattern:
                matches = search_files(pattern, file_list)
                print(f"\n[SEARCH RESULTS] {len(matches)} file(s) found:")
                for m in matches:
                    print(m['path'])
        elif choice == "5":
            handle_file_operations()
            file_list = scan_directory(directory)
        elif choice == "6":
            handle_batch_by_extension(file_list)
        elif choice == "7":
            handle_batch_by_size(file_list)
        elif choice == "8":
            handle_list_files(file_list)
        elif choice == "9":
            other_dir = input("Enter another directory to check against: ").strip()
            if os.path.isdir(other_dir):
                other_files = scan_directory(other_dir)
                duplicates = cross_directory_duplicate_check(file_list, other_files)
                if duplicates:
                    print("\n[Cross-directory Duplicates Found]:")
                    for main_file, dup in duplicates:
                        print(f"- {main_file['path']} is a duplicate of {dup['path']}")
                else:
                    print("No cross-directory duplicates found.")
            else:
                print("Invalid directory.")
        elif choice == "10":
            print("Rescanning directory...")
            file_list = scan_directory(directory)
            print(f"Found {len(file_list)} files.")
        elif choice == "0":
            print("Exiting Smart File Organizer. Goodbye!")
            break
        else:
            print("Invalid option. Please choose 0-10.")

if __name__ == "__main__":
    run_cli()