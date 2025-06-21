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
    from sorter import sort_files
    return sort_files(rabin_karp_search(pattern, files,param))
