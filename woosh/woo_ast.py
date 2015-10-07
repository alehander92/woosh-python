class Node:

    def __init__(self, node_type, **fields):
        self.node_type = node_type
        self.fields = fields
        # for k, v in fields.items():
        #     setattr(self, k, v)
