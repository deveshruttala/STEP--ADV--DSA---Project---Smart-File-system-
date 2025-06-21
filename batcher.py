from collections import defaultdict

def batch_files_by_extension(file_list):
    """
    Groups files into batches based on their extension.
    
    :param file_list: List of file dictionaries with 'extension' key
    :return: Dictionary where keys are extensions and values are lists of files
    """
    batches = defaultdict(list)
    for file in file_list:
        ext = file.get("extension", "").lower()
        batches[ext].append(file)
    return dict(batches)

def batch_files_by_size(file_list, size_ranges=[(0, 1024), (1024, 10240), (10240, 102400), (102400, None)]):
    """
    Groups files into size-based batches.
    
    :param file_list: List of file dictionaries with 'size' key
    :param size_ranges: List of tuples representing size ranges in bytes
    :return: Dictionary with size range labels as keys
    """
    batches = defaultdict(list)
    for file in file_list:
        size = file['size']
        for range_min, range_max in size_ranges:
            if range_max is None:
                if size >= range_min:
                    label = f"{range_min/1024:.1f}KB+"
                    batches[label].append(file)
                    break
            elif range_min <= size < range_max:
                label = f"{range_min/1024:.1f}KB-{range_max/1024:.1f}KB"
                batches[label].append(file)
                break
    return dict(batches)