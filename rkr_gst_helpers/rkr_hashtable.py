class RKRHashtable:

    def __init__(self):
        self.dict = {}

    def add(self, hash, data):
        """ Stores data for hash in a list. """
        if self.dict.has_key(hash):
            values = self.dict.get(hash)
            values.append(data)
            self.dict.setdefault(hash, values)
        else:
            self.dict.setdefault(hash, [data])

    def get(self, hash):
        """ Returns a list with data objects for hash. """
        if hash in self.dict:
            return self.dict[hash]
        else:
            return []

    def clear(self):
        """ Clears the hash table. """
        self.dict = {}

    def create_hash_value(self, substring):
        hash_value = 0
        for c in substring:
            hash_value = ((hash_value << 1) + ord(c))  # hash_value = ((hash_value<<1) + substring[i])
        return hash_value
