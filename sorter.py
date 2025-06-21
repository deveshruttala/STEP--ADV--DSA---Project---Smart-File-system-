from datetime import datetime

def file_compare(file1, file2, keys):
    for key in keys:
        v1 = file1[key]
        v2 = file2[key]

        # Convert to common format for comparison
        if key == "size":
            v1 = int(v1)
            v2 = int(v2)
        elif key == "date":
            v1 = datetime.fromisoformat(v1)
            v2 = datetime.fromisoformat(v2)

        if v1 < v2:
            return -1
        elif v1 > v2:
            return 1
    return 0

def merge_sort(arr, keys):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], keys)
    right = merge_sort(arr[mid:], keys)
    return merge(left, right, keys)

def merge(left, right, keys):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if file_compare(left[i], right[j], keys) <= 0:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def sort_files(files, keys=["name"]):
    return merge_sort(files, keys)