class Parameter:
    def __init__(self, *, name, alias=None, default=None):
        self.name = name
        self.alias = alias
        self._default = None
        self.default = default
        self._value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

    @property
    def default(self):
        return self._default

    @default.setter
    def default(self, default):
        self._default = default

    def reset(self):
        self.value = self.default

    def export(self, use_alias=False):
        if self.value != self.default:
            if self.alias and use_alias:
                name_to_use = self.alias
            else:
                name_to_use = self.name
            return "{}={}".format(name_to_use, self.value)
        else:
            return ""


class TextParameter(Parameter):
    def __init__(self, *, name, default="", alias=None):
        self.value = default
        super(TextParameter, self).__init__(name=name, alias=alias)


class BooleanParameter(Parameter):
    def __init__(self, *, name, default=False, yes="1", no="0", alias=None):
        self.yes = yes
        self.no = no
        self.value = default
        super(BooleanParameter, self).__init__(name=name, alias=alias, default=default)

    @property
    def value(self):
        if self._value:
            return self.yes
        else:
            return self.no

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def default(self):
        if self._default:
            return self.yes
        else:
            return self.no

    @default.setter
    def default(self, default):
        self._default = default


class SelectParameter(Parameter):
    def __init__(self, *options, name, alias=None):
        self.options = {}
        self._selected = None

        for option in options:
            self.options[option.name] = option
            if option.default:
                self._selected = option
        super(SelectParameter, self).__init__(name=name, alias=alias, default=self._selected)

    @property
    def value(self):
        return self._selected.name

    @value.setter
    def value(self, value):
        selected = None
        for option in self.options:
            if self.options[option].name == value:
                selected = self.options[option]
                break
        self._selected = selected

    @property
    def default(self):
        for option in self.options:
            if self.options[option].default:
                return self.options[option].name
        return None

    @default.setter
    def default(self, default):
        pass


class Option:
    def __init__(self, *, name, alias=None, default=False):
        self.name = name
        self.alias = alias
        self.default = default
