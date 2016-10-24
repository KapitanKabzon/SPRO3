from collections import namedtuple
import cocos
import cocos.actions as act
import json
import pyglet

WHITE = (255, 255, 255, 255)
RED = (255, 0, 0, 255)

Point = namedtuple('Point', ['x', 'y'])
Line = namedtuple('Line', ['a', 'c'])
Segment = namedtuple('Segment', ['A', 'B'])


class Map(cocos.cocosnode.CocosNode):
    def __init__(self):
        super(Map, self).__init__()
        self.center = 327, 136
        self.walls = []
        self.read('map.json')
        sprite = pyglet.image.load('pls.png')
        self.sprite = cocos.sprite.Sprite(sprite)
        self.add(self.sprite)
        x, y = self.sprite.position
        self.sprite.position = x + 100, y + 100
        self.sprite.scale = 0.5
        self.position = 100, 100

    def read(self, file):
        with open(file) as f:
            lines = json.load(f)
        walls = []
        for line in lines:
            seg = Segment(Point._make(line[0]), Point._make(line[1]))
            mid = Map.Midpoint(seg.A, seg.B)
            walls.append((cocos.draw.Line(self.center, mid, RED,
                                          stroke_width=3)))
            walls.append((cocos.draw.Line(seg.A, seg.B, WHITE,
                                          stroke_width=5)))
        for wall in walls:
            self.add(wall)
        self.walls += walls

    def remove_walls(self):
        for wall in self.walls:
            self.remove(wall)
        self.walls = []

    def render(self):
        pass

    @staticmethod
    def Interception(A: Line, B: Line) -> Point:
        if (B.a - A.a) is 0:
            return None
        x = (A.c - B.c)/(B.a - A.a)
        y = A.a * x + A.c
        return Point(x, y)

    @staticmethod
    def PointsToFactors(A: Point, B: Point) -> Line:
        if (B.x - A.x) is 0:
            return None
        a = (B.y - B.x)/(A.x - B.x)
        c = A.y - a * A.x
        return Line(a, c)

    @staticmethod
    def Midpoint(A: Point, B: Point) -> Point:
        x, y = A.x + (B.x - A.x)/2, A.y + (B.y - A.y)/2
        return Point(x, y)


class MapDisplay(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super(MapDisplay, self).__init__()
        self.map = Map()
        self.add(self.map)
        self.keys_pressed = set()

    def on_key_press(self, key, modifiers):
        if key is 32:
            try:
                self.map.remove_walls()
            except:
                print('No wall to remove')

    def on_key_release(self, key, modifiers):
        if key is 108:
            try:
                self.map.read('map.json')
            except:
                print('Can not read walls file')


cocos.director.director.init(width=800, height=600)
map_layer = MapDisplay()
main_scene = cocos.scene.Scene(map_layer)
cocos.director.director.run(main_scene)
