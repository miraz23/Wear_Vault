
class LazyProperty(object):
    """A decorator class for lazy instantiation."""

    def __init__(self, f_get):
        self.f_get = f_get
        self.func_name = f_get.__name__

    def __get__(self, obj, cls):
        if obj is None:
            return None
        value = self.f_get(obj)
        setattr(obj, self.func_name, value)
        return value
