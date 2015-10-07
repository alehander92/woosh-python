class Env:

    def __init__(self, parent=None, values=None):
        self.parent = parent
        self.values = values or {}

    def __getitem__(self, key):
        current = self
        while current:
            if key in current.values:
                return current.values[key]
            current = current.parent
        return None

    def __setitem__(self, key, value):
        self.values[key] = value
