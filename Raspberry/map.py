import cocos
import json
from collections import namedtuple

WHITE = (255, 255, 255, 255)
RED = (255, 0, 0, 255)

Point = namedtuple('Point', ['x', 'y'])
Line = namedtuple('Line', ['a', 'c'])
Segment = namedtuple('Segment', ['A', 'B'])


def ReadMap(file):
    with open(file) as f:
        data = json.load(f)
    return data


def Interception(A: Line, B: Line) -> Point:
    if (B.a - A.a) is 0:
        return None
    x = (A.c - B.c)/(B.a - A.a)
    y = A.a * x + A.c
    return Point(x, y)


def PointsToFactors(A: Point, B: Point) -> Line:
    if (B.x - A.x) is 0:
        return None
    a = (B.y - B.x)/(A.x - B.x)
    c = A.y - a * A.x
    return Line(a, c)


def Midpoint(A: Point, B: Point) -> Point:
    x, y = A.x + (B.x - A.x)/2, A.y + (B.y - A.y)/2
    return Point(x, y)


class MapDisplay(cocos.layer.Layer):
    is_event_handler = True
    center = 327, 136

    def __init__(self):
        super(MapDisplay, self).__init__()
        self.lines = ReadMap('map.json')
        self.center = 327, 136
        for line in self.lines:
            seg = Segment(Point._make(line[0]), Point._make(line[1]))
            mid = Midpoint(seg.A, seg.B)
            self.add(cocos.draw.Line(self.center, mid, RED, stroke_width=3))
            self.add(cocos.draw.Line(seg.A, seg.B, WHITE, stroke_width=5))


cocos.director.director.init()
map_layer = MapDisplay()
main_scene = cocos.scene.Scene(map_layer)
cocos.director.director.run(main_scene)
