from tkinter import Canvas, Tk, StringVar
from tkinter.ttk import Frame, Button, Entry, Label
from math import pi, atan2, sin, cos
import bellhop as hop


class Application(Frame):
    def __init__(self, master=None):
        self.width = 800
        self.height = 600
        Frame.__init__(self, master)
        pad = 5
        self.grid()

        # Map canvas
        self.canvas = Canvas(self, width=self.width, height=self.height)
        self.canvas.grid(row=0, column=0, columnspan=4, padx=pad, pady=pad)

        # Add button
        self.add = Button(self, text='Add')
        self.add.grid(row=1, column=0, padx=pad, pady=pad)

        # Entry
        self.entry = Entry(self)
        self.entry.grid(row=1, column=1,  padx=pad, pady=pad)

        self.entry_contents = StringVar()
        self.entry['textvariable'] = self.entry_contents
        self.entry_contents.set('x1, y1, x2, y2')
        self.entry.bind('<Key-Return>', self.entry_handler)

        # Status label
        self.status = Label(self)
        self.status.grid(row=1, column=2, padx=pad, pady=pad)
        self.entry.focus()

        # Bellhop biz
        self.bellhop = hop.Bellhop(800/2, 600/2, 0)
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

        self.readings = []
        for sensor in self.bellhop.sensors:
            sensor.d = 50
            x1, y1 = self.bellhop.sensor_point(sensor)
            x2, y2 = self.bellhop.sensor_measurement(sensor)
            cords = x1, y1, x2, y2
            cords = self.inversey(cords)
            self.canvas.create_line(*cords,
                                    fill='blue',
                                    width=3,
                                    tags='hop'
                                    )
            cords = self.bellhop.x, self.bellhop.y, x1, y1
            cords = self.inversey(cords)
            line = self.canvas.create_line(*cords, fill='red', tags='hop')
            self.readings.append(line)

        self.update_map()
        self.r = 90
        self.angle = 0

        # Start the loop
        self.onUpdate()

    def update_map(self):
        """Update map canvas"""
        # Store old position and bearing of bellhop
        x, y, alpha = self.bellhop.x, self.bellhop.y, self.bellhop.alpha

        # Get change
#        dx, dy, dalpha = self.bellhop.deltas()

        # Delete old lines
        self.canvas.delete('hop')

        # Redraw bellhop
        for sensor in self.bellhop.sensors:
            sensor.d = 50
            x1, y1 = self.bellhop.sensor_point(sensor)
            x2, y2 = self.bellhop.sensor_measurement(sensor)
            cords = x1, y1, x2, y2
            cords = self.inversey(cords)
            self.canvas.create_line(*cords,
                                    fill='blue',
                                    width=3,
                                    tags='hop'
                                    )
            cords = self.bellhop.x, self.bellhop.y, x1, y1
            cords = self.inversey(cords)
            line = self.canvas.create_line(*cords, fill='red', tags='hop')
            self.readings.append(line)

    def newpos(x, y):
        return x, y

    def entry_handler(self, event):
        if self.focus_get() is self.entry:
            try:
                input = self.entry_contents.get().split()
                self.canvas.create_line(*input, fill='red', width=3)
            except:
                print('')
            self.entry_contents.set('')

    def add_ping(self, r, beta, gamma, id=None):
        ping = hop.Ping(r, beta, gamma, id)
        self.bellhop.sensors.append(ping)

    def inversey(self, cords):
        y1 = self.height - cords[1]
        y2 = self.height - cords[3]
        new = cords[0], y1, cords[2], y2
        return new

    def onUpdate(self):
        self.bellhop.x = 800/2 + self.r * sin(self.angle)
        self.bellhop.y = 600/2 + self.r * cos(self.angle)
        self.bellhop.alpha = self.angle + (2*pi)/4
        self.angle += (2*pi)/500
        self.update_map()
        self.after(10, self.onUpdate)

root = Tk()
app = Application(master=root)
app.mainloop()
