class Kind:
    pass

    def as_string(self):
        return '(a confused woo object)'


class Base(Kind):

    def __init__(self, label):
        self.label = label


class Struct(Kind):

    def __init__(self, label, **slots):
        self.label = label
        self.slots = {}
        for slot, cell in slots.items():
            self.slots[slot] = cell

    def as_string(self):
        return '{0}({1})'.format(self.label,
                                 ' '.join('{0} {1}'.format(slot, cell.as_string())
                                          for slot, cell
                                          in self.slots.items()))


class Fun(Kind):

    def __init__(self, arg_types=None, kwargs=None, return_type=None):
        self.arg_types = [ArgType(t) for t in arg_types] if arg_types else []
        self.kwargs = {k: Kwarg(k, v)
                       for k, v in kwargs.items()} if kwargs else {}
        self.return_type = return_type


class ArgType(Kind):

    def __init__(self, a):
        self.label, self.woo_type = list(a)[:2]


class Kwarg(Kind):

    def __init__(self, label, t):
        self.label = label
        self.woo_type, self.default = t

    def as_string(self):
        return '@{0}={1}'.format(self.label, self.default)


class List(Kind):

    def __init__(self, element_type):
        self.element_type = element_type

    @property
    def methods(self):
        return type(self).methods

    def as_string(self):
        return '[{0}]'.format(self.element_type.as_string())


class Map(Kind):

    def __init__(self, key_type, value_type):
        self.key_type, self.value_type = key_type, value_type
        self.methods = {}

    @property
    def methods(self):
        return type(self).methods

    def as_string(self):
        return '\{{0}:{1}\}'.format(self.key_type.as_string(), self.value_type.as_string())


class WException(Kind):

    def __init__(self):
        pass

    def as_string(self):
        return 'WException'


class Nil(Kind):
    pass

    def as_string(self): return 'nil'


class WooNilS:

    def __init__(self):
        self.woo_type = Nil

    def as_string(self): return 'nil'

WooNil = WooNilS()
