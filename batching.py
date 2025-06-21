from collections import defaultdict

def batch_files_by_extension(file_list):
    """
    Groups files into batches based on their extension.

    :param file_list: List of file dictionaries with 'extension' key.
    :return: Dictionary where keys are extensions and values are lists of files.
    """
    batches = defaultdict(list)
    for file in file_list:
        ext = file.get("extension", "").lower()
        batches[ext].append(file)
    return dict(batches)

files=[{'name': 'desktop.ini', 'size': 282, 'date': '2024-12-13T10:53:40.901762',
         'path': 'C:\\Users\\rutta\\Desktop\\desktop.ini', 'extension': '.ini'},
        {'name': 'Devesh Resume.pdf', 'size': 239064, 'date': '2025-06-06T16:58:15.183964',
         'path': 'C:\\Users\\rutta\\Desktop\\Devesh Resume.pdf', 'extension': '.pdf'},
        {'name': 'Devesh Ruttala Resume backend.pdf', 'size': 201379, 'date': '2025-05-13T03:23:59.728901',
          'path': 'C:\\Users\\rutta\\Desktop\\Devesh Ruttala Resume backend.pdf', 'extension': '.pdf'},
        {'name': 'Docker Desktop.lnk', 'size': 2142, 'date': '2025-04-03T21:59:22.417129',
         'path': 'C:\\Users\\rutta\\Desktop\\Docker Desktop.lnk', 'extension': '.lnk'},
        {'name': 'Haveloc.lnk', 'size': 2776, 'date': '2025-06-02T11:15:01.714996',
         'path': 'C:\\Users\\rutta\\Desktop\\Haveloc.lnk', 'extension': '.lnk'},
]

batched = batch_files_by_extension(files)

for ext, group in batched.items():
    print(f"\nExtension: {ext}")
    for f in group:
        print(f"  Name: {f['name']}, Size: {f['size']}, Date: {f['date']}, Path: {f['path']}")
