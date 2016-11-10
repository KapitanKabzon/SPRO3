import tkinter as tk
from tkinter import Canvas, Tk, StringVar
from tkinter.ttk import Frame, Button, Entry, Label
from math import pi, sin, cos
import bellhop as hop


class Application(Frame):
    def __init__(self, master=None):
        self.width = 800
        self.height = 600
        Frame.__init__(self, master)
        pad = 5
        self.grid()

        # Map canvas
        self.canvas = Canvas(self, width=self.width, height=self.height,
                             cursor='plus')
        self.canvas.grid(row=0, column=0, columnspan=4, padx=pad, pady=pad)

        # Quit button
        self.button = Button(self, text='Quit', command=exit)
        self.button.grid(row=1, column=3, padx=pad, pady=pad)

        # Entry
        self.entry = Entry(self)
        self.entry.grid(row=1, column=0,  padx=pad, pady=pad)

        self.entry_contents = StringVar()
        self.entry['textvariable'] = self.entry_contents
        self.entry_contents.set('x1 y1 x2 y2')
        self.entry.bind('<Key-Return>', self.entry_handler)

        # Mouse
        self.bind('<Button-1>', self.mouse_handler)

        # Status label
        self.status = Label(self)
        self.status.grid(row=1, column=2, padx=pad, pady=pad)
        self.entry.focus()

        # Bellhop biz
        self.bellhop = hop.Bellhop(800/2, 600/2, 0, map='map.json')
        self.add_ping(40, 0, 0, id=0)
        self.add_ping(40, 0.125*pi, 0.125*pi, id=1)
        self.add_ping(40, -0.125*pi, -0.125*pi, id=2)
        self.add_ping(40, 1*0.25*pi, 0.5*pi, id=3)
        self.add_ping(40, 3*0.25*pi, 0.5*pi, id=4)
        self.add_ping(40, 5*0.25*pi, -0.5*pi, id=5)
        self.add_ping(40, 7*0.25*pi, -0.5*pi, id=6)
        self.add_ping(40, pi, pi, id=7)

        cords = (self.bellhop.x - 2,
                 self.bellhop.y - 2,
                 self.bellhop.x + 2,
                 self.bellhop.y + 2
                 )
        self.canvas.create_rectangle(*cords, fill='white', tags='hop')

        for sensor in self.bellhop.sensors:
            sensor.d = 20

        # Sensor lables
        xpos = 5
        ypos = 5
        for sensor in self.bellhop.sensors:
            id = sensor.id
            self.canvas.create_text(xpos,
                                    ypos,
                                    text=id,
                                    fill='white',
                                    anchor=tk.NW,
                                    )
            ypos += 15

        # Bellhop position labels
        xpos = 200
        ypos = 5
        self.canvas.create_text(xpos,
                                ypos,
                                text='x:',
                                fill='white',
                                anchor=tk.NW,
                                )
        ypos += 15
        self.canvas.create_text(xpos,
                                ypos,
                                text='y:',
                                fill='white',
                                anchor=tk.NW,
                                )

        self.r = 150
        self.angle = 0

        # Draw map walls
        for wall in self.bellhop.map.walls:
            cords = self.inversey(wall)
            self.canvas.create_line(*cords,
                                    fill='yellow',
                                    tags='wall',
                                    width=2
                                    )
        # Start the loop
        self.onUpdate()

    def update_map(self):
        """Update map canvas"""
        self.redraw_bellhop()

    def redraw_bellhop(self):
        # Delete old lines, and text
        self.canvas.delete('hop')
        self.canvas.delete('sensor')
        self.canvas.delete('reading')
        self.canvas.delete('position')

        # Print position
        xpos = 215
        ypos = 5
        self.canvas.create_text(xpos,
                                ypos,
                                text=self.bellhop.x,
                                fill='white',
                                anchor=tk.NW,
                                tags='position'
                                )
        ypos += 15
        self.canvas.create_text(xpos,
                                ypos,
                                text=self.bellhop.y,
                                fill='white',
                                anchor=tk.NW,
                                tags='position'
                                )

        # Sensor lines and readings
        ypos = 5
        for sensor in self.bellhop.sensors:
            sensor_v = self.bellhop.measurement_vector(sensor)
            x1, y1 = self.bellhop.sensor_point(sensor)
            cords = self.bellhop.x, self.bellhop.y, x1, y1
            cords = self.inversey(cords)
            self.canvas.create_line(*cords, fill='red', tags='hop')

            wall = self.bellhop.map.closest(sensor_v)
            if wall is None:
                ypos += 15
                continue

            # Draw reading
            wall_v = self.bellhop.map.wall_vector(wall)
            intersection = self.bellhop.map.intersection(sensor_v, wall_v)
            if intersection is None:
                ypos += 15
                continue
            cords = x1, y1, intersection[0], intersection[1]
            cords = self.inversey(cords)
            self.canvas.create_line(*cords,
                                    fill='blue',
                                    width=5,
                                    tags='sensor'
                                    )

            # Calculate the reading
            d = self.bellhop.map.length(cords)
            self.canvas.create_text(20,
                                    ypos,
                                    text=d,
                                    fill='white',
                                    anchor=tk.NW,
                                    tags='reading'
                                    )
            ypos += 15

        # Bellhop center
        cords = (self.bellhop.x - 3,
                 self.bellhop.y - 3,
                 self.bellhop.x + 3,
                 self.bellhop.y + 3
                 )
        cords = self.inversey(cords)
        self.canvas.create_rectangle(*cords, fill='white', tags='hop')

    def entry_handler(self, event):
        if self.focus_get() is self.entry:
            try:
                input = self.entry_contents.get().split()
                wall = []
                for cord in input:
                    wall.append(int(cord))
                wall = self.inversey(wall)
                self.canvas.create_line(*input, fill='yellow', width=2)
                self.bellhop.map.walls.append(wall)
            except:
                print('Entry input not in format: "x1 y1 x2 y2"')
            self.entry_contents.set('')

    def mouse_handler(self, event):
        print('click ', event.x, event.y)

    def add_ping(self, *args, **kwargs):
        ping = hop.Ping(*args, **kwargs)
        self.bellhop.sensors.append(ping)

    def inversey(self, cords):
        """Inverse y coordinates of a line"""
        y1 = self.height - cords[1]
        y2 = self.height - cords[3]
        new = cords[0], y1, cords[2], y2
        return new

    def onUpdate(self):
        self.angle += (2*pi)/500
        new_x = self.width/2 + self.r * sin(self.angle)
        new_y = self.height/2 + self.r * cos(self.angle)
        new_alpha = self.angle + (2*pi)/4
        self.bellhop.x = new_x
        self.bellhop.y = new_y
        self.bellhop.alpha = new_alpha
        self.update_map()
        self.after(10, self.onUpdate)

root = Tk()
app = Application(master=root)
app.mainloop()
