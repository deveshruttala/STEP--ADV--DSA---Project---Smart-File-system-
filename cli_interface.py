import os
from file_scanner import scan_directory
#from sorter import merge_sort, quick_sort
#from hasher import detect_duplicates
#from searcher import search_files

def display_menu():
    print("\n==== Smart File Organizer CLI ====")
    print("1. Sort files by name")
    print("2. Sort files by size")
    print("3. Detect duplicate files")
    print("4. Delete duplicate files")
    print("5. Search files by name pattern")
    print("6. Rescan directory")
    print("7. Exit")
    print("===================================")

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
    
    while True:
        display_menu()
        choice = input("Select an option (1-7): ").strip()

        if choice == "1":
            sorted_files = merge_sort(file_list, key="name")
            print("\n[SORTED BY NAME]")
            for f in sorted_files:
                print(f"{f['path']}")

        elif choice == "2":
            sorted_files = quick_sort(file_list, key="size")
            print("\n[SORTED BY SIZE]")
            for f in sorted_files:
                print(f"{f['path']} ({f['size']} bytes)")

        elif choice == "3":
            duplicates = detect_duplicates(file_list)
            if duplicates:
                print("\n[DUPLICATES FOUND]")
                for d in duplicates:
                    print(d['path'])
            else:
                print("No duplicates found.")

        elif choice == "4":
            duplicates = detect_duplicates(file_list)
            if not duplicates:
                print("No duplicates to delete.")
                continue
            confirm = input("Delete all duplicates? [y/N]: ").strip().lower()
            if confirm == "y":
                for d in duplicates:
                    try:
                        os.remove(d['path'])
                        print(f"Deleted: {d['path']}")
                    except Exception as e:
                        print(f"Failed to delete {d['path']}: {e}")
                file_list = scan_directory(directory)
            else:
                print("Deletion canceled.")

        elif choice == "5":
            pattern = input("Enter search pattern: ").strip()
            if pattern:
                matches = search_files(file_list, pattern)
                print(f"\n[SEARCH RESULTS] {len(matches)} file(s) found:")
                for m in matches:
                    print(m['path'])
            else:
                print("No pattern provided.")

        elif choice == "6":
            print("Rescanning directory...")
            file_list = scan_directory(directory)
            print("Directory rescan completed.")

        elif choice == "7":
            print("Exiting Smart File Organizer. Goodbye!")
            break
        
        
        elif choice == "8":
            path = input("Enter full file path to modify: ").strip()
            if not os.path.exists(path):
                print("File does not exist.")
                continue

            print("\n1. Rename")
            print("2. Delete")
            print("3. Move")
            print("4. Mark as duplicate")
            action = input("Select file action (1-4): ").strip()

            from file_operations import rename_file, delete_file, move_file, mark_duplicate

            if action == "1":
                new_name = input("Enter new name for the file (with extension): ").strip()
                rename_file(path, new_name)

            elif action == "2":
                confirm = input("Are you sure you want to delete this file? (y/N): ").lower()
                if confirm == "y":
                    delete_file(path)

            elif action == "3":
                destination = input("Enter destination directory: ").strip()
                move_file(path, destination)

            elif action == "4":
                mark_duplicate(path)

            else:
                print("Invalid action selected.")
        

        elif choice == "9":
            other_dir = input("Enter another directory to check against: ").strip()
            if not os.path.isdir(other_dir):
                print("Invalid directory.")
                continue
            from file_operations import cross_directory_duplicate_check
            duplicates = cross_directory_duplicate_check(file_list, other_dir)
            if duplicates:
                print(f"\n[Cross-directory Duplicates Found]: {len(duplicates)}")
                for main_file, dup in duplicates:
                    print(f"- {main_file['path']} is a duplicate of {dup['path']}")
            else:
                print("No cross-directory duplicates found.")

        

        else:
            print("Invalid option. Please choose 1-7.")

if __name__ == "__main__":
    run_cli()
