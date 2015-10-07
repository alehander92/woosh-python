class Kind:
    pass


class Base(Kind):

    def __init__(self, label):
        self.label = label


class Struct(Kind):

    def __init__(self, label, **slots):
        self.label = label
        self.slots = {}
        for slot, cell in slots.items():
            self.slots[slot] = cell


class Fun(Kind):

    def __init__(self, arg_types=None, kwargs=None, return_type=None):
        self.arg_types = [ArgType(t) for t in arg_types] if arg_types else []
        self.kwargs = {k: Kwarg(k, v)
                       for k, v in kwargs.items()} if kwargs else {}
        self.return_type = return_type


class ArgType(Kind):

    def __init__(self, a):
        self.label, self.woo_type = a


class Kwarg(Kind):

    def __init__(self, label, t):
        self.label = label
        self.default, self.woo_type = t


class List(Kind):

    def __init__(self, element_type):
        self.element_type = element_type

    @property
    def methods(self):
        return type(self).methods


class Map(Kind):

    def __init__(self, key_type, value_type):
        self.key_type, self.value_type = key_type, value_type
        self.methods = {}

    @property
    def methods(self):
        return type(self).methods


class Nil(Kind):
    pass
