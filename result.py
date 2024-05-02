from dataclasses import dataclass
from typing import Any


@dataclass
class Ok:
    value: Any

    def __bool__(self):
        return True

    def __repr__(self):
        return str(self.value)

    def then(self, f, error=None):
        try:
            x = f(self.value)
            return to_result(x)
        except Exception as e:
            if error:
                return Err(error)
            return Err(e)

    def check(self, condition, error):
        try:
            if condition(self.value):
                return Ok(self.value)
            else:
                return Err(error)
        except Exception as e:
            return Err(e)

    def branch(self, condition, true_f, false_f):
        if condition(self.value):
            return true_f(self.value)
        else:
            return false_f(self.value)

    def conclude(self, ok, err):
        return ok(self.value)


@dataclass
class Err:
    error: Any

    def __bool__(self):
        return False

    def __repr__(self):
        return str(self.error)

    def then(self, f, error=None):
        return self

    def check(self, condition, error):
        return self

    def branch(self, condition, true_f, false_f):
        return self

    def conclude(self, ok, err):
        return err(self.error)


def to_result(x):
    print(x, type(x))
    match x:
        case Ok(value):
            return Ok(value)
        case Err(error):
            return Err(error)
        case None:
            return Err("value not present")
        case value:
            return Ok(value)
