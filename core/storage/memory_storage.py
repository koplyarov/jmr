class MemoryStorage(object):
    def __init__(self):
        self._tables = {}

    def create_table(self, path):
        new_table = []
        self._tables[path] = new_table
        return new_table

    def get_table(self, path):
        return self._tables[path]
