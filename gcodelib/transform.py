import numpy as np

from . import moves


class Aggregate(object):
    def __init__(self, *moves):
        self.moves = moves
        self.transform = np.matrix([[1,0,0,0],
                                    [0,1,0,0],
                                    [0,0,1,0],
                                    [0,0,0,1]])
        

    def add(self, *moves):
        self.moves += moves
        
    def get_string(self, precision=3, transform=None, current_pos=None):
        if transform is not None:
            transform = transform * self.transform
        else:
            transform = self.transform
        if current_pos is None:
            current_pos = {'x':0, 'y':0, 'z':0}
        return "\n".join(move.get_string(precision,transform, current_pos) for move in self.moves)
        
    def __str__(self):
        return self.get_string()
        
class Translate(Aggregate):
    def __init__(self, offset, *moves):
        x_off, y_off, z_off = offset
        self.transform = np.matrix([[1,0,0,x_off],
                                    [0,1,0,y_off],
                                    [0,0,1,z_off],
                                    [0,0,0,1]])
        self.moves = moves
        ##conver these into transform moves....
        
class Rotate(Aggregate):
    def __init__(self, rotation, *moves):
        #rotate around z, then y, then x if applicable, angle in degrees
        self.transform = np.matrix(np.identity(4))
        if 'z' in rotation:
            theta = np.radians(rotation['z'])
            s = np.sin(theta)
            c = np.cos(theta)
            self.transform = self.transform * np.matrix([[c,-s, 0, 0],
                                                         [s, c, 0, 0],
                                                         [0, 0, 1, 0],
                                                         [0, 0, 0, 1]])
        if 'y' in rotation:
            theta = np.radians(rotation['y'])
            s = np.sin(theta)
            c = np.cos(theta)
            self.transform = self.transform * np.matrix([[c, 0, s, 0],
                                                         [0, 0, 0, 0],
                                                         [-s,0, c, 0],
                                                         [0 ,0, 0, 1]])
        if 'x' in rotation:
            theta = np.radians(rotation['x'])
            s = np.sin(theta)
            c = np.cos(theta)
            self.transform = self.transform * np.matrix([[0, 0, 0, 0],
                                                         [0, c,-s, 0],
                                                         [0, s, c, 0],
                                                         [0, 0, 0, 1]])
        self.moves = moves
    
class Scale(Aggregate):
    def __init__(self, scale_by, *moves):
        try:
            x_scale, y_scale, z_scale = scale_by
        except TypeError:
            x_scale = y_scale = z_scale = scale_by
        self.transform = np.matrix([[x_scale, 0, 0, 0],
                                    [0, y_scale, 0, 0],
                                    [0, 0, z_scale, 0],
                                    [0, 0, 0, 1]])
        self.moves = moves
