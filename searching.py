def rabin_karp_search(pattern, file_list,param, prime=101):
    matches = []
    d = 256  # ASCII character base
    m = len(pattern)
    pattern = pattern.lower()
    pattern_hash = 0
    h = 1

    # Precompute h = d^(m-1) % prime
    for i in range(m - 1):
        h = (h * d) % prime

    # Compute hash of pattern
    for i in range(m):
        pattern_hash = (d * pattern_hash + ord(pattern[i])) % prime

    for file in file_list:
        text = file[param].lower()
        n = len(text)
        text_hash = 0
        found = False

        # Initial hash for first window
        for i in range(min(m, n)):
            text_hash = (d * text_hash + ord(text[i])) % prime

        for i in range(n - m + 1):
            if text_hash == pattern_hash:
                if text[i:i + m] == pattern:
                    found = True
                    break  # We only need to know it's present once in the name

            # Recalculate hash for next window
            if i < n - m:
                text_hash = (d * (text_hash - ord(text[i]) * h) + ord(text[i + m])) % prime
                if text_hash < 0:
                    text_hash += prime

        if found:
            matches.append(file)

    return matches


def search_files(pattern,files,param='name'):
    """
    Search for files whose names contain the given pattern using the Rabin-Karp algorithm.
    
    :param pattern: The substring to search for in file names.
    :param files: List of file dictionaries with 'name' key.
    :return: List of matching file dictionaries.
    """
    from sort import sort_files
    return sort_files(rabin_karp_search(pattern, files,param))


# files=[{'name': 'desktop.ini', 'size': 282, 'date': '2024-12-13T10:53:40.901762',
#          'path': 'C:\\Users\\rutta\\Desktop\\desktop.ini', 'extension': '.ini'},
#         {'name': 'Devesh Resume.pdf', 'size': 239064, 'date': '2025-06-06T16:58:15.183964',
#          'path': 'C:\\Users\\rutta\\Desktop\\Devesh Resume.pdf', 'extension': '.pdf'},
#         {'name': 'Devesh Ruttala Resume backend.pdf', 'size': 201379, 'date': '2025-05-13T03:23:59.728901',
#           'path': 'C:\\Users\\rutta\\Desktop\\Devesh Ruttala Resume backend.pdf', 'extension': '.pdf'},
#         {'name': 'Docker Desktop.lnk', 'size': 2142, 'date': '2025-04-03T21:59:22.417129',
#          'path': 'C:\\Users\\rutta\\Desktop\\Docker Desktop.lnk', 'extension': '.lnk'},
#         {'name': 'Haveloc.lnk', 'size': 2776, 'date': '2025-06-02T11:15:01.714996',
#          'path': 'C:\\Users\\rutta\\Desktop\\Haveloc.lnk', 'extension': '.lnk'},
# ]
# print(search_files("de", files))  # Example usage