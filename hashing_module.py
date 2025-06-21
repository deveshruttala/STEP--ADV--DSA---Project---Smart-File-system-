import os
import hashlib

class HashTable:
    def __init__(self, size=10007): 
        self.size = size
        self.table = [None] * size

    def _hash(self, key: str) -> int:
        """Converts a SHA-256 hex string into a numeric hash index."""
        return int(key, 16) % self.size

    def insert(self, hash_value: str, file_path: str) -> bool:
        """
        Inserts a hash into the table. If the hash already exists, appends the file path.
        Returns False if it's a duplicate, True otherwise.
        """
        idx = self._hash(hash_value)
        start_idx = idx

        while self.table[idx] is not None:
            stored_hash, paths = self.table[idx]
            if stored_hash == hash_value:
                paths.append(file_path)
                return False  # Duplicate found
            
            idx = (idx + 1) % self.size
            if idx == start_idx:
                raise RuntimeError("Hash table is full!") #Returns to the start index, indicating a full table

        self.table[idx] = (hash_value, [file_path])
        return True  # Unique

    def get_duplicates(self) -> dict:
        """
        Returns a dictionary of hashes with duplicates.
        """
        return {
            hash_val: paths
            for entry in self.table
            if entry is not None
            for hash_val, paths in [entry]
            if len(paths) > 1
        }

def compute_sha256(file_path: str) -> str:
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"[ERROR] Could not read file '{file_path}': {e}")
        return None

def scan_and_hash_duplicates(directory: str) -> dict:

    hashtable = HashTable()

    for root, _, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            hash_val = compute_sha256(full_path)
            if hash_val:
                is_unique = hashtable.insert(hash_val, full_path)
                if not is_unique:
                    print(f"[DUPLICATE] {full_path}")

    return hashtable.get_duplicates()
