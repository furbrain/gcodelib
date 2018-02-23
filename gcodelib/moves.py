import attr
import numpy as np

@attr.s
class Move(object):
    x = attr.ib(default=None)
    y = attr.ib(default=None)
    z = attr.ib(default=None)
    f = attr.ib(default=None)
    code = ""
    values = ['x', 'y', 'z', 'f']
    
    def transform_values(self, transform, current_pos):
        if current_pos is None:
            current_pos = {}
        t = {}
        for val in self.values:
            if getattr(self,val) is None:
                t[val] = current_pos.get(val)
            else:
                t[val] = getattr(self,val)
                current_pos[val] = t[val]
        pos = np.matrix([t['x'],t['y'],t['z'],1]).transpose()
        new_pos = transform*pos
        t['x'] = new_pos[0,0]
        t['y'] = new_pos[1,0]
        t['z'] = new_pos[2,0]
        return t

    
    def get_str_val(self, letter, vals, precision):
        val = vals.get(letter)
        if val is None:
            return ""
        else:
            return "{}{:.{prec}f}".format(letter.upper(), val, prec=precision)
    
    def get_string(self, precision=3, transform=None, current_pos=None):
        t = self.transform_values(transform, current_pos)
        items = [self.code]
        items += [self.get_str_val(x, t, precision) for x in self.values]
        return " ".join(x for x in items if x)
    
    
    def __str__(self):
        return self.get_string()

@attr.s
class Rapid(Move):
    """A rapid movement (G00)
    
    Args:
        x (:obj:`float`, optional): x-position
        y (:obj:`float`, optional): y-position
        z (:obj:`float`, optional): z-position
        f (:obj:`float`, optional): feedrate        
    """
    code = "G00"

@attr.s
class Line(Move):
    """A  movement (G00)
    
    Args:
        x (:obj:`float`, optional): x-position
        y (:obj:`float`, optional): y-position
        z (:obj:`float`, optional): z-position
        f (:obj:`float`, optional): feedrate        
    """
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

    def transform_values(self, transform, current_pos):
        t = Move.transform_values(self, transform, current_pos)
        ###FIXME### need to raise warning if not isometric transform
        if t['r'] is not None:
            ###FIXME### need to account for radius options
            return t
        else:
            #pos = np.matrix([t['i'],t['j'],t['k']]).transpose()
            #new_pos = transform[0:3,0:3]*pos
            #t['i'] = new_pos[0,0]
            #t['j'] = new_pos[0,1]
            #t['k'] = new_pos[0,2]
            return t

