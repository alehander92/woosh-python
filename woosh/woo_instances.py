class WooObject:

    def __init__(self, woo_type, fields):
        self.woo_type = woo_type
        self.fields = fields


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


class WooMap(WooObject):

    def __init__(self, hash, map):
        self.hash = hash
        self.woo_type = map

    @property
    def methods(self):
        return self.woo_type.methods
