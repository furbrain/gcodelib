from . import transform

class Grid(transform.Aggregate):
    """Creates multiple copies of a set of moves in a grid pattern.
    
    Args:
        count: a list of how many [rows, columns]
        spacing: a list of [row_spacing, column_spacing] or a single float of spacing between each item for both dimensions
        *moves: The moves to be duplicated
        align: defines where the origin will be for each set of moves to be offset. options are 
        `topleft`,    `top`,    `topright`,
        `left`,       `centre`, `right`,
        `bottomleft`, `bottom`, `bottomright`
        
    Examples:
        Grid(3, 50, my_moves) -- this creates a 3 x 3 grid of sets of my_moves, the bottom left is at (-50,-50),
        the top right is at (50, 50)
        
        Grid([2,4], [20,40], my_move1, my_move2, align="bottomleft") -- this creates a 2x4 grid with 20 units space horizontally 
        and 40 units vertically. Bottom left is at (0, 0), top right is at (40, 160)
    """
    
    LOCATIONS = {
        'topleft': (0, -1),
        'top': (-0.5, -1),
        'topright': (-1,-1),
        'left': (0, -0.5),
        'centre': (-0.5, -0.5),
        'right': (-1, -0.5),
        'bottomleft': (0, 0),
        'bottom': (-0.5, 0),
        'bottomright': (-1, 0)
    }
    
    def __init__(self, count, spacing, *moves, align='centre'):
        if isinstance(count, (list, tuple)):
            self.count = count
        else:
            self.count = [count, count]
        if isinstance(spacing, (list, tuple)):
            self.spacing = spacing
        else:
            self.spacing = [spacing, spacing]
        self.moves = moves
        self.align = align
        
    def create_grid(self):
        grid = transform.Aggregate()
        origin = [(i-1)*j*k for i, j, k in zip(self.count, self.spacing, self.LOCATIONS[self.align])]
        x_coords = [i*self.spacing[0]+origin[0] for i in range(self.count[0])]
        y_coords = [i*self.spacing[1]+origin[1] for i in range(self.count[1])]
        if self.spacing[0]<self.spacing[1]: # select based on which gap is shorter
            for i, y in enumerate(y_coords):
                if i % 2:
                    temp_x = reversed(x_coords)
                else:
                    temp_x = x_coords
                for x in temp_x:
                    grid.add(transform.Translate([x,y,0], *self.moves))
        else:
            for i, x in enumerate(x_coords):
                if i % 2:
                    temp_y = reversed(y_coords)
                else:
                    temp_y = y_coords
                for y in temp_y:
                    grid.add(transform.Translate([x,y,0], *self.moves))
        return grid
                
    def get_string(self, precision=3, transform=None, current_pos=None):
        grid = self.create_grid()
        return grid.get_string(precision, transform, current_pos)        
