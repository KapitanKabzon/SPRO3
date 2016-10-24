import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.hello = tk.Button(self)
        self.hello["text"] = "Hello World"
        self.hello["command"] = self.say_hi
        self.hello.pack(side="left")

        self.QUIT = tk.Button(self, text="QUIT", fg="red", bg="white",
                              command=root.destroy)
        self.QUIT.pack(side="left")
        self.map = tk.Canvas(self.master, width=800, height=600)
        self.map.pack()
        self.map.create_line(0, 0, 50, 50, fill="red")
        self.map.create_rectangle(50, 50, 150, 75, fill="blue")

    def say_hi(self):
        print("yo")

root = tk.Tk()
app = Application(master=root)
app.mainloop()
