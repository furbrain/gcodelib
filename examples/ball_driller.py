import gcodelib as gc

BALL_SIZE = 40.0
DEPTH = 6.0
EXTRA_DEPTH = 1.0
SAFE_HEIGHT = 2.0
TOOL_RADIUS = 3.175/2
MOUNT_HOLE_RADIUS = 3.3

BLOCK_WIDTH = 210
BLOCK_HEIGHT = 140

DIVOT_LENGTH = 8.0
DIVOT_OFFSET = 5.0

DRILL_DEPTH = 4.5

def drill_hole(radius, tool_radius, step, depth):
    cut_radius = radius-tool_radius
    hole = gc.Aggregate()
    hole.add(gc.Rapid(-cut_radius, 0, SAFE_HEIGHT)) #go to start point
    hole.add(gc.Line(z=0)) # go to surface
    i=0
    while (i> -depth):
        i= max(i-step, -depth)
        hole.add(gc.Arc(z=i, i=cut_radius))
    hole.add(gc.Arc(z=i, i=cut_radius))
    hole.add(gc.Rapid(z=SAFE_HEIGHT))
    return hole

def plunge_hole(radius, tool_radius, depth):
    cut_radius = radius-tool_radius
    hole = gc.Aggregate()
    hole.add(gc.Rapid(-cut_radius, 0, SAFE_HEIGHT)) #go to start point
    hole.add(gc.Line(z=-depth)) # go to surface
    hole.add(gc.Arc(z=-depth, i=cut_radius))
    hole.add(gc.Rapid(z=SAFE_HEIGHT))
    return hole

def plunge(depth):
    return gc.Aggregate(gc.Rapid(0, 0, SAFE_HEIGHT), gc.Line(z=-depth), gc.Line(z=SAFE_HEIGHT))
    
def ball_drill():
    return gc.Grid(2,9,plunge(DRILL_DEPTH))

def ball_carve():
    return plunge_hole(8, TOOL_RADIUS, DRILL_DEPTH)


all_ball_drills = gc.Grid([4,2],50, ball_drill(), align="bottomleft")
all_ball_carves = gc.Grid([4,2],50, ball_carve(), align="bottomleft")



everything = gc.Aggregate(gc.Rapid(0,0, SAFE_HEIGHT, f=800), gc.Line(0,0,SAFE_HEIGHT,f=800))
everything.add(all_ball_drills)
#everything.add(all_ball_carves)
everything.add(gc.Rapid(x = 100, y=100))
print ("M03 S750\n")
print(everything)
print("M05\n")
