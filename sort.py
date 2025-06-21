from datetime import datetime

# Helper to convert size like "2MB" to bytes
def size_to_bytes(size_str):
    size_units = {"B": 1, "KB": 1e3, "MB": 1e6, "GB": 1e9}
    num = float(size_str[:-2])
    unit = size_str[-2:].upper()
    return int(num * size_units.get(unit, 1))

# Multi-level comparator
def file_compare(file1, file2, keys):
    for key in keys:
        v1 = file1[key]
        v2 = file2[key]

        # if key == "size":
        #     v1 = size_to_bytes(v1)
        #     v2 = size_to_bytes(v2)

        if v1 < v2:
            return -1
        elif v1 > v2:
            return 1
    return 0  # all keys equal

# Multi-key merge sort
def merge_sort_multi(arr, keys):
    #print("called",arr)
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort_multi(arr[:mid], keys)
    right = merge_sort_multi(arr[mid:], keys)
    return merge_multi(left, right, keys)

def merge_multi(left, right, keys):
    sorted_array = []
    i = j = 0
    while i < len(left) and j < len(right):
        comp = file_compare(left[i], right[j], keys)
        if comp <= 0:
            sorted_array.append(left[i])
            i += 1
        else:
            sorted_array.append(right[j])
            j += 1
    sorted_array.extend(left[i:])
    sorted_array.extend(right[j:])
    return sorted_array

# files=[{'name': 'desktop.ini', 'size': 282, 'date': '2024-12-13T10:53:40.901762', 
#         'path': 'C:\\Users\\rutta\\Desktop\\desktop.ini', 'extension': '.ini'},
#         {'name': 'Devesh Resume.pdf', 'size': 239064, 'date': '2025-06-06T16:58:15.183964',
#         'path': 'C:\\Users\\rutta\\Desktop\\Devesh Resume.pdf', 'extension': '.pdf'},
#         {'name': 'Devesh Ruttala Resume backend.pdf', 'size': 201379, 'date': '2025-05-13T03:23:59.728901',
#           'path': 'C:\\Users\\rutta\\Desktop\\Devesh Ruttala Resume backend.pdf', 'extension': '.pdf'},
#         {'name': 'Docker Desktop.lnk', 'size': 2142, 'date': '2025-04-03T21:59:22.417129', 
#          'path': 'C:\\Users\\rutta\\Desktop\\Docker Desktop.lnk', 'extension': '.lnk'}, 
#          {'name': 'Haveloc.lnk', 'size': 2776, 'date': '2025-06-02T11:15:01.714996', 
#           'path': 'C:\\Users\\rutta\\Desktop\\Haveloc.lnk', 'extension': '.lnk'},
# ]
# # Before sorting
# print("Before Sorting:")
# for file in files:
#     print(f"Name: {file['name']}, Size: {file['size']}, Date: {file['date']}")

# # Sort by name → size → date
# files_sorted = merge_sort_multi(files, keys=["name", "size", "date"])

# # After sorting
# print("\nAfter Multi-Level Sorting by name, size, then date:")
# for file in files_sorted:
#     print(f"Name: {file['name']}, Size: {file['size']}, Date: {file['date']}")
def sort_files(files,keys=["name", "size", "date"]):
    return merge_sort_multi(files, keys)
