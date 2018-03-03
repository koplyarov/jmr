class MemoryStorage(object):
    def __init__(self):
        self._root_dir = {}

    def get_root_dir(self):
        return self._root_dir

    def create_table(self, path):
        parsed_path = self._parse_path(path)
        current_dir = self._root_dir
        for dir in parsed_path[:-1]:
            try:
                current_dir = current_dir[dir]
            except KeyError:
                 current_dir[dir] = {}
                 current_dir = current_dir[dir]

        new_table = []
        current_dir[parsed_path[-1]] = new_table
        return new_table

    def get_table(self, path):
        parsed_path = self._parse_path(path)
        current_dir = self._root_dir
        for dir in parsed_path[:-1]:
            current_dir = self._root_dir[dir]

        return current_dir[path]

    def _parse_path(self, path):
        assert path.startswith('/')
        return path.split('/')[1:]
