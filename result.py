class Ok:
    def __init__(self, value):
        self.value = value

    def __bool__(self):
        return True

    def __repr__(self):
        return str(self.value)

    def then(self, f):
        return f(self.value)

    def check(self, condition, error):
        if condition(self.value):
            return Ok(self.value)
        else:
            return Err(error)

    def branch(self, condition, true_f, false_f):
        if condition(self.value):
            return true_f(self.value)
        else:
            return false_f(self.value)

    def conclude(self, ok, err):
        return ok(self.value)


class Err:
    def __init__(self, error):
        self.error = error

    def __bool__(self):
        return False

    def __repr__(self):
        return str(self.error)

    def then(self, f):
        return self

    def check(self, condition, error):
        return self

    def branch(self, condition, true_f, false_f):
        return self

    def conclude(self, ok, err):
        return err(self.error)
