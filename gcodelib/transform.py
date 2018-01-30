import attr

from . import moves


class Aggregate(object):
    def __init__(self, *moves):
        self.moves = moves
        self.transform = [[1,0,0,0],
                          [0,1,0,0],
                          [0,0,1,0],
                          [0,0,0,1]]
        

    def add(self, *moves):
        self.moves += moves
        
class Translate(Aggregate):
    def __init__(self, offset, *moves):
        self.offset = offset
        self.moves = moves
        ##conver these into transform moves....
        
class Rotate(Aggregate):
    def __init__(self, x=None, y=None, z=None):
        #rotate around x, then y, then z if applicable
        
    
