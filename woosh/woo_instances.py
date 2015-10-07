class WooObject:

    def __init__(self, woo_type, fields):
        self.woo_type = woo_type
        self.fields = fields
        return {}

    def as_string(self):
        return '(a confused woo object)'


class WooBase(WooObject):

    def __init__(self, value, base):
        self.value = value
        self.woo_type = base


class WooStruct(WooObject):

    def __init__(self, slots, struct):
        self.slots = {}
        for slot, cell in slots.items():
            if slot not in struct.slots:
                raise ValueError("no {0} in {1}".format(slot, struct.label))
            self.slots[slot] = cell
        self.woo_type = struct

    def as_string(self):
        return '{0} ({1})'.format(self.woo_type.label,
                                  ' '.join('{0} {1}'.format(slot, cell.as_string())
                                           for slot, cell
                                           in self.slots.items()))


class WooException(WooObject):

    def __init__(self, message, exception):
        self.message = message
        self.woo_type = exception

    def as_string(self):
        return self.message


class WooFun(WooObject):

    def __init__(self, label, code, fun):
        self.label = label
        self.code = code
        self.woo_type = fun


class WooList(WooObject):

    def __init__(self, elements, list_type):
        self.elements = elements
        self.woo_type = list_type

    @property
    def methods(self):
        return self.woo_type.methods

    def as_string(self):
        return '\n'.join(e.as_string() for e in self.elements)


class WooMap(WooObject):

    def __init__(self, hash, map):
        self.hash = hash
        self.woo_type = map

    @property
    def methods(self):
        return self.woo_type.methods

    def as_string(self):
        return '\n'.join('{0}:\t{1}'.format(k.as_string(), v.as_string()) for k, v in self.hash.items())
