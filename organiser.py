
import argparse
import json
from searching import search_files
from sort import sort_files
from batching import batch_files_by_extension
from file_scanner import scan_directory


def main():
    parser = argparse.ArgumentParser(description="Organize and search files in current directory")
    parser.add_argument("--sort",nargs="?", const="",choices=["name", "size", "date", ""],help="Sort files by 'name', 'size', or 'date'. Leave blank to sort by all.")
    parser.add_argument("--search", help="Search files by keyword in filename")
    parser.add_argument("--batch", action='store_true', help="Batch files by their extension")
    files = scan_directory(".")
    args = parser.parse_args()
    
    if args.search:
        files = search_files(args.search, files)

    if args.sort is not None:
        sort_keys = [args.sort] if args.sort else ["name", "size", "date"]
        files = sort_files(files, sort_keys)
    if files:
        print("\n\n\n\nAvailable files:")

        for f in files:
            print(f"{f['name']}.{f['extension']} | {f['size']} bytes | {f['date']} | {f['path']}")
    else:
        print("No matching files found.")

if __name__ == "__main__":
    main()
