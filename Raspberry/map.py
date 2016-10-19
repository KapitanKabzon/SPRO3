import os
os.environ["PYSDL2_DLL_PATH"] = "/usr/lib64"
import sdl2
import sdl2.ext
import sdl2.sdlgfx
import json

BACKGROUND = sdl2.ext.Color(0, 0, 0)


class Renderer(sdl2.ext.Renderer):
    def __init__(self, colour=BACKGROUND, logical_size=(800, 400)):
        self.window = sdl2.ext.Window("Test", size=logical_size)
        self.window.show()
        self.colour = colour
        self.map = []
        self.read_map()
        self.wallcolour = sdl2.ext.Color(255, 0, 0)
        super().__init__(self.window, logical_size=logical_size)

    def render(self):
        self.clear(self.colour)
        self.fill(self.colour)
        for item in self.map:
            self.thick_line(item, sdl2.ext.Color(255, 0, 0), 10)
        self.present()

    def read_map(self):
        try:
            with open('map.json', 'r') as f:
                self.map = json.load(f)
        except:
            print('Could not read map.json')

    def thick_line(self, points, color=None, thickness=3):
        color = sdl2.ext.rgba_to_color(color)
        sdl2.sdlgfx.thickLineColor(self.renderer, points[0], points[1],
                                   points[2], points[3], thickness, color)


def run():
    sdl2.ext.init()

    renderer = Renderer(logical_size=(500, 300))

    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_r:
                    renderer.read_map()
        renderer.render()

try:
    run()
finally:
    sdl2.ext.quit()
