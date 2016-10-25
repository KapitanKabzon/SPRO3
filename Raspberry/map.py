from tkinter import Canvas, Tk, StringVar
from tkinter.ttk import Frame, Button, Entry, Label
from math import pi, cos, sin
import bellhop as hop


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        pad = 5
        self.grid()

        # Map canvas
        self.canvas = Canvas(self, width=800, height=600)
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
        self.ping = hop.Ping(45, 0.15*pi, 0.5 * pi)
        self.ping.d = 0
        self.r = 80
        self.angle = 0
        self.ping.d = 30
        xoff = 800/2 + self.r * cos(self.angle)
        yoff = 600/2 + self.r * sin(self.angle)
        x1, y1 = self.ping.point()
        x2, y2 = self.ping.measurement_point()
        x1 += xoff
        x2 += xoff
        y1 += yoff
        y2 += yoff
        self.xoff = xoff
        self.yoff = yoff
        print(x1, y1, x2, y2)
        cords = (x1, y1, x2, y2)
        self.ping_line = self.canvas.create_line(*cords,
                                                 fill='red',
                                                 width=1,
                                                 activewidth=4)
        self.onUpdate()

    def entry_handler(self, event):
        if self.focus_get() is self.entry:
            print(self.entry_contents.get())

    def onUpdate(self):
        old = self.canvas.coords(self.ping_line)
        old_point = old[2], old[3]
        step = 2*pi/(30)
        step2 = 2*pi/(pi*25)
        self.angle += step2
        self.xoff = 800/2 + self.r * cos(self.angle)
        self.yoff = 600/2 + self.r * sin(self.angle)
        self.reverse = False
        self.ping.gamma += step
        point = self.ping.measurement_point()
        new_point = point[0] + self.xoff, point[1] + self.yoff
        cords = old_point[0], old_point[1], new_point[0], new_point[1]
        self.canvas.create_line(*cords, fill='yellow', width=1)
        new = old[0], old[1], point[0] + self.xoff, point[1] + self.yoff
        self.canvas.coords(self.ping_line, new)
        self.after(1, self.onUpdate)


root = Tk()
app = Application(master=root)
app.mainloop()
