class Socket:
    def __init__(self, node, *accepts):
        self.node = node
        self.accepts = list(accepts)
        self.link = None
