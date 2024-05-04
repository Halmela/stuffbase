from dataclasses import dataclass
from typing import Any


@dataclass
class Ok:
    value: Any

    def __bool__(self):
        return True

    def __repr__(self):
        return str(self.value)

    def __add__(self, other):
        print('MULTI')
        match other:
            case Ok(val):
                print('okadd', val)
                return Ok(self.value + val)
            case Err(e):
                print('erredd', e)
                return Err(e)
            case x:
                print('add', x)
                return self + to_result(x)

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

    def __add__(self, other):
        return self

    def then(self, f, error=None):
        return self

    def check(self, condition, error):
        return self

    def branch(self, condition, true_f, false_f):
        return self

    def conclude(self, ok, err):
        return err(self.error)


def to_result(x, error=None):
    print(x, type(x))
    match x:
        case None | [None] | '' | ['', *_]:
            return Err(error if error else "value not present")
        case Ok(value):
            return Ok(value)
        case Err(err) | [Err(err), *_]:
            return Err(err)
        case [Ok(x), *rest] | [x, *rest]:
            return Ok([x]) + to_result(rest, error=error)
        case [Ok(x)] | [x]:
            return Ok([x])
        case value:
            return Ok(value)
