# Periodic boundaries with surfaces

import math
import smoldyn

def get_axis(line):
    x0, y0, x1, y1 = line
    theta = math.atan2(y1 - y0, x1 - x0)
    if math.isclose(theta, 0.0) or math.isclose(theta, math.pi):
        return '+y'
    return '+x'

def add_maze(s, mazefile):
    panels = []
    offset = 1.5
    scale = 10
    with open(mazefile, "r") as f:
        for i, l in enumerate(f.read().strip().split("\n")):
            line = [scale * (offset + float(x)) for x in l.split()]
            axis = get_axis(line)
            x0, y0, x1, y1 = line
            r = s.addRectangle(
                corner=[x0, y0],
                dimensions=[max((x1 - x0), (y1 - y0))],
                axis=axis,
                name=f"r{i}",
            )
            panels.append(r)
    # close the entry notch
    r = s.addRectangle(
            corner=[10, 10],
            dimensions=[30],
            axis='+y',
            name=f"rrr",
            )
    panels.append(r)
    return panels


s = smoldyn.Simulation(low=[0, 0], high=[120, 120])
A = s.addSpecies("A", difc=2, color="blue")
A.addToSolution(1000, pos=[15, 15])

panels = add_maze(s, "_maze.txt")
maze = s.addSurface("maze", panels=panels)
maze.setAction("front", [A], "reflect")
maze.setAction("back", [A], "reflect")
maze.setStyle("both", thickness=1)

s.addGraphics("opengl", iter=30)
s.run(3000, dt=0.01)
