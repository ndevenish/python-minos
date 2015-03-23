# coding: utf-8

from collections import namedtuple

def _unaryMethodGen(name):
  def __method(self):
    return type(self)._make(getattr(x, name)() for x in self)
  return __method

def _binaryMethodGen(name):
  def __method(self, other):
    if isinstance(other, tuple):
      if len(other) != len(self):
        # We must match attributes, if not lengths
        if not hasattr(other, "_fields"):
          raise AttributeError("Other side of mismatched-length {} is not a namedtuple".format(name))
        # Take whichever side has the subset
        # Make sure that field names are compatible
        if set(self._fields) <= set(other._fields):
          subset = self
          otherset = other
        elif set(self._fields) >= set(other._fields):
          subset = other
          otherset = self
        else:
          raise AttributeError("namedtuple field names are incompatible with contraction")
        return type(subset)._make(getattr(self[self._fields.index(fname)], name)(other[other._fields.index(fname)]) for fname in subset._fields)
      else:
        # Same length, don't care if fields mismatch
        return type(self)._make(getattr(x, name)(y) for x, y in zip(self, other))
    else:
      return type(self)._make(getattr(x, name)(other) for x in self)
  return __method


def operatable_namedtuple(name, fields):
  class OperatorTuple(namedtuple(name, fields)):
    __slots__ = ()
    __pos__ = _unaryMethodGen("__pos__")
    __neg__ = _unaryMethodGen("__neg__")
    __abs__ = _unaryMethodGen("__abs__")
    __invert__ = _unaryMethodGen("__invert__")
    __round__ = _unaryMethodGen("__round__")
    __floor__ = _unaryMethodGen("__floor__")
    __ceil__ = _unaryMethodGen("__ceil__")
    __trunc__ = _unaryMethodGen("__trunc__")
    __add__ = _binaryMethodGen("__add__")
    __sub__ = _binaryMethodGen("__sub__")
    __mul__ = _binaryMethodGen("__mul__")
    __floordiv__ =_binaryMethodGen("__floordiv__")
    __div__ = _binaryMethodGen("__div__")
    __truediv__ = _binaryMethodGen("__truediv__")
    __mod__ = _binaryMethodGen("__mod__")
    __divmod__ = _binaryMethodGen("__divmod__")
    __pow__ = _binaryMethodGen("__pow__")
    __radd__ = _binaryMethodGen("__radd__")
    __rsub__ = _binaryMethodGen("__rsub__")
    __rmul__ = _binaryMethodGen("__rmul__")
    __rfloordiv__ =_binaryMethodGen("__rfloordiv__")
    __rdiv__ = _binaryMethodGen("__rdiv__")
    __rtruediv__ = _binaryMethodGen("__rtruediv__")
    __rmod__ = _binaryMethodGen("__rmod__")
    __rdivmod__ = _binaryMethodGen("__rdivmod__")
    __rpow__ = _binaryMethodGen("__rpow__")
    __iadd__ = _binaryMethodGen("__iadd__")
    __isub__ = _binaryMethodGen("__isub__")
    __imul__ = _binaryMethodGen("__imul__")
    __ifloordiv__ =_binaryMethodGen("__ifloordiv__")
    __idiv__ = _binaryMethodGen("__idiv__")
    __itruediv__ = _binaryMethodGen("__itruediv__")
    __imod__ = _binaryMethodGen("__imod__")
    __ipow__ = _binaryMethodGen("__ipow__")
    __eq__ = _binaryMethodGen("__eq__")
    __ne__ = _binaryMethodGen("__ne__")
    __lt__ = _binaryMethodGen("__lt__")
    __gt__ = _binaryMethodGen("__gt__")
    __le__ = _binaryMethodGen("__le__")
    __ge__ = _binaryMethodGen("__ge__")
  OperatorTuple.__name__ = name
  return OperatorTuple