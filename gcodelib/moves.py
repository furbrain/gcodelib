import attr

@attr.s
class Move(object):
    x = attr.ib(default=None)
    y = attr.ib(default=None)
    z = attr.ib(default=None)
    f = attr.ib(default=None)
    code = ""
    values = ['x', 'y', 'z', 'f']
    
    def get_str_val(self, letter, precision):
        val = getattr(self, letter)
        if val is None:
            return ""
        else:
            return "{}{:.{prec}f}".format(letter.upper(), val, prec=precision)
    
    def get_string(self, precision=3):
        items = [self.code]
        items += [self.get_str_val(x, precision) for x in self.values]
        return " ".join(x for x in items if x)
    
    
    def __str__(self):
        return self.get_string()

@attr.s
class Rapid(Move):
    code = "G00"

@attr.s
class Line(Move):
    code = "G01"

@attr.s            
class Arc(Move):
    i = attr.ib(default=None)
    j = attr.ib(default=None)
    k = attr.ib(default=None)
    r = attr.ib(default=None)
    clockwise = attr.ib(default=True)
    values = ['x', 'y', 'z', 'i', 'j', 'k', 'r']
    
    @property
    def code(self):
        if self.clockwise:
            return "G02"
        else:
            return "G03"

