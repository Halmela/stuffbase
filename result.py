class Ok:
    def __init__(self, value):
        self.value = value

    def __bool__(self):
        return True

    def __repr__(self):
        return str(self.value)


class Err:
    def __init__(self, value):
        self.value = value

    def __bool__(self):
        return False

    def __repr__(self):
        return str(self.value)
