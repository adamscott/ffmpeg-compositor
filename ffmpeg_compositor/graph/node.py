class Node:
    def __init__(self):
        self.name = ""
        self.input_sockets = []
        self.output_sockets = []
        self.parameters = []

    @property
    def parents(self):
        found_parents = []
        for input_socket in self.input_sockets:
            if input_socket.link:
                found_parents.append(input_socket.link.start.node)
        return found_parents

    @property
    def children(self):
        found_children = []
        for output_socket in self.output_sockets:
            if output_socket.link:
                for sockets in output_socket.link.end:
                    found_children.append(sockets.node)
        return found_children

    def is_related(self, other):
        searched = []

        def search(a, b):
            if b in a.parents or b in a.children:
                return True
            else:
                for parent in a.parents:
                    if parent not in searched:
                        searched.append(parent)
                        if search(parent, b):
                            return True

                for child in a.children:
                    if child not in searched:
                        searched.append(child)
                        if search(child, b):
                            return True
                return False

        return search(self, other)

    def is_directly_related(self, other, direction='both'):
        if other in self.parents and (direction == 'parents' or direction == 'both'):
            return True
        elif other in self.children and (direction == 'children' or direction == 'both'):
            return True
        else:
            if direction == 'parents' or direction == 'both':
                for parent in self.parents:
                    if Node.is_directly_related(parent, other, direction='parents'):
                        return True

            if direction == 'children' or direction == 'both':
                for child in self.children:
                    if Node.is_directly_related(child, other, direction='children'):
                        return True
            return False

    def add_parameters(self, *parameters):
        self.parameters = self.parameters + list(parameters)

    def get(self, name):
        for parameter in self.parameters:
            if parameter.name == name or parameter.alias == name:
                return parameter

    def export(self):
        parameters_exports = []
        for parameter in self.parameters:
            parameters_exports.append(parameter.export())
        parameters_result = ":".join([x for x in parameters_exports if x])

        command_result = ""
        if parameters_result:
            command_result = "{}={}".format(self.name, parameters_result)

        if command_result:
            if len(self.output_sockets):
                return "{} {} {}".format(
                    " ".join(["[" + x.link.name + "]" for x in self.input_sockets if x.link]),
                    command_result,
                    " ".join(["[" + x.link.name + "]" for x in self.output_sockets if x.link])
                )