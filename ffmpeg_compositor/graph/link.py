class Link:
    last_id = -1

    def __init__(self, name=None, start=None, end=None):
        if not end:
            end = []

        if name:
            self.name = name
        else:
            self.name = Link.generate_name()
        self.start = start
        self.end = end

    def link(self, start, *end):
        if start and end:
            self.start = start
            self.end = list(end)
            self.start.link = self
            for end_socket in self.end:
                end_socket.link = self

    @staticmethod
    def generate_name():
        Link.last_id = Link.last_id + 1
        return "link_{}".format(Link.last_id)
