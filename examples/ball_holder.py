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

def drill_hole(radius, tool_radius, step, depth):
    cut_radius = radius-tool_radius
    hole = gc.Aggregate()
    hole.add(gc.Rapid(-cut_radius, 0, SAFE_HEIGHT)) #go to start point
    hole.add(gc.Line(z=0)) # go to surface
    i=0
    while (i> -depth):
        i= max(i-2, -depth)
        hole.add(gc.Arc(z=i, i=cut_radius))
    hole.add(gc.Arc(z=i, i=cut_radius))
    hole.add(gc.Rapid(z=SAFE_HEIGHT))
    return hole
    

ball_hole  = gc.Aggregate(gc.Rapid(0, 0, SAFE_HEIGHT), gc.Line(0, 0, -2), gc.Line(z=SAFE_HEIGHT))
all_ball_holes = [gc.Translate([i*50-75,j*50-25,0], ball_hole) for i in range(4) for j in range(2)]
mount_hole = drill_hole(MOUNT_HOLE_RADIUS, TOOL_RADIUS, 2, DEPTH+EXTRA_DEPTH)
all_mount_holes = [gc.Aggregate(gc.Line(0,0,SAFE_HEIGHT), gc.Translate([i,j,0], mount_hole)) for i in [-95,95] for j in [-45,45]]
divot = gc.Aggregate(
    gc.Rapid(-DIVOT_LENGTH/2, 0, SAFE_HEIGHT),
    gc.Line(z=-2),
    gc.Line(x=DIVOT_LENGTH/2),
    gc.Line(z=SAFE_HEIGHT)
    )

all_divots = gc.Aggregate(
    gc.Translate([-BLOCK_WIDTH/2+DIVOT_OFFSET,0,0], gc.Rotate({'z':90}, divot)),
    gc.Translate([BLOCK_WIDTH/2-DIVOT_OFFSET,0,0], gc.Rotate({'z':90}, divot)),
    *[gc.Translate([i,j,0],divot) for i in [-BLOCK_WIDTH/4, +BLOCK_WIDTH/4] 
                                  for j in [BLOCK_HEIGHT/2-DIVOT_OFFSET, DIVOT_OFFSET-BLOCK_HEIGHT/2]]
    )
    

start = BLOCK_WIDTH/2+TOOL_RADIUS
trims = gc.Aggregate(
    gc.Line(0, BLOCK_HEIGHT/2, SAFE_HEIGHT),
    gc.Rapid(start, BLOCK_HEIGHT/2+TOOL_RADIUS, SAFE_HEIGHT),
    gc.Line(z=-2),
    gc.Line(x=-start),
    gc.Line(z=-4),
    gc.Line(x=start),
    gc.Line(z=-6.2),
    gc.Line(x=-start),
    gc.Line(z=SAFE_HEIGHT)
    )


everything = gc.Aggregate(gc.Rapid(0,0, SAFE_HEIGHT, f=800), gc.Line(0,0,SAFE_HEIGHT,f=600))
everything.add(*all_ball_holes)
everything.add(*all_mount_holes)
#everything.add(all_divots)
#everything.add(trims)
print(gc.Translate([BLOCK_WIDTH/2,BLOCK_HEIGHT/2,0],everything))
