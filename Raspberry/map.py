import cocos
import json


def ReadMap(file):
    with open(file) as f:
        data = json.load(f)
    return data


def Interception(A, B):
    a1, c1, a2, c2 = A[0], A[1], B[0], B[1]
    if (a2 - a1) is 0:
        return None
    x = (c1 - c2)/(a2 - a1)
    y = a1 * x + c1
    return x, y


def PointsToFactors(A, B):
    x1, y1, x2, y2 = A[0], A[1], B[0], B[1]
    if (x2 - x1) is 0:
        return None
    a = (y2 - y1)/(x2 - x1)
    c = y1 - a * x1
    return a, c


def Midpoint(A, B):
    x1, y1, x2, y2 = A[0], A[1], B[0], B[1]
    x, y = x2 - x1, y2 - y1
    return x, y


class MapDisplay(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super(MapDisplay, self).__init__()
        self.lines = ReadMap('map.json')
        center = 327, 136
        for line in self.lines:
            fac1 = PointsToFactors(line[0], line[1])
            fac2 = PointsToFactors(center, Midpoint(line[0], line[1]))
            if fac1 and fac2 is not None:
                int = Interception(fac1, fac2)
                if int is not None:
                    self.add(cocos.draw.Line(center, int,
                                             (255, 255, 255, 255),
                                             stroke_width=2))
            self.add(cocos.draw.Line(line[0], line[1],
                                     (255, 255, 255, 255),
                                     stroke_width=5))



cocos.director.director.init()
map_layer = MapDisplay()
main_scene = cocos.scene.Scene(map_layer)
cocos.director.director.run(main_scene)
