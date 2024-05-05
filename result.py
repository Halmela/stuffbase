from dataclasses import dataclass
from enum import Enum, auto
from typing import Any
from itertools import repeat


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


class Variant(Enum):
    OK = True
    ERR = False


@dataclass
class Result:
    variant: Variant = Variant.OK
    value: Any = None
    error: str = None

    def __init__(self, value=None, error=None):
        try:
            match value:
                case (None, err) | ('', err):
                    self.variant = Variant.ERR
                    self.error = err
                case None | '':
                    self.variant = Variant.ERR
                    self.error = error
                case (val, err):
                    print("single", val)
                    self.value = val
                    self.error = err
                case [*xs]:
                    self.value = []
                    print(xs)
                    for res in [Result(x) for x in xs]:
                        print("x:", res)
                        match res:
                            case Result(Variant.ERR, _, error):
                                self.variant = Variant.ERR
                                self.error = error
                                return
                            case Result(Variant.OK, val, _):
                                # print("list", x, res.value)
                                self.value.append(val)
                case _:
                    self.value = value
        except Exception as exception:
            self.variant = Variant.ERR
            self.error = error if error else exception

    def __bool__(self):
        return self.variant.value

    # def __repr__(self):
    #     if self.variant:
    #         return self.value
    #     else:
    #         return self.error

    # def __add__(self, other):
    #     print('ADD')
    #     print(self)
    #     print(other)
    #     if self.variant == Variant.ERR:
    #         print('selferr')
    #         return self

    #     match other:
    #         case Result(variant=Variant.OK, value=val):
    #             print('okadd', val)
    #             return Result(self.value + val)
    #         case Result(variant=Variant.ERR, error=err):
    #             print('erredd', err)
    #             return other
    #         case (value, error):
    #             print('valadd', value, error)
    #             return Result(self.value + value, error)
    #         case x:
    #             print('add', x)
    #             print('other:', other)
    #             match Result(x):
    #                 case Result(variant=Variant.OK, value=val):
    #                     print(val)
    #                     self.value = self.value + val
    #                 case Result(variant=Variant.ERR, error=err):
    #                     self.variant = Variant.ERR
    #                     self.error = err

    def then(self, f, error=None):
        print(self)
        if self.variant == Variant.ERR:
            print("return self")
            return self
        try:
            match f(self.value):
                case Result(variant=Variant.OK, value=val) | Ok(value=val):
                    print("thenval", val)
                    self.value = val
                case Result(variant=Variant.ERR, error=err) | Err(error=err):
                    print("thenerr", err)
                    self.variant = Variant.ERR
                    self.error = err
                case x:
                    print("x", x)
                    self.value = x

        except Exception as exception:
            self.variant = Variant.ERR
            self.error = error if error else \
                self.error if self.error else exception
        return self

    def check(self, condition, error):
        if self.variant == Variant.ERR:
            return self

        try:
            if not condition(self.value):
                self.variant = Variant.ERR
                self.error = error
        except Exception as exception:
            self.variant = Variant.ERR
            self.error = error if error else exception

        return self

    def branch(self, condition, true_f, false_f):
        if self.variant == Variant.ERR:
            return self

        if condition(self.value):
            return true_f(self.value)
        else:
            return false_f(self.value)

    def conclude(self, ok, err):
        print(self)
        if self.variant == Variant.OK:
            return ok(self.value)
        else:
            return err(self.error)
