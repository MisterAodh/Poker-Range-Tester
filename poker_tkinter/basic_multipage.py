import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multi-page Example")
        self.geometry("300x200")
        self.frame = None
        self.show_frame(StartPage)

    def show_frame(self, frame_class):
        if self.frame:
            self.frame.destroy()
        self.frame = frame_class(self)
        self.frame.pack()

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Start Page").pack()
        tk.Button(self, text="Go to Page 1", command=lambda: master.show_frame(Page1)).pack()
        tk.Button(self, text="Go to Page 2", command=lambda: master.show_frame(Page2)).pack()

class Page1(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Page 1").pack()
        tk.Button(self, text="Back", command=lambda: master.show_frame(StartPage)).pack()

class Page2(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Page 2").pack()
        tk.Button(self, text="Back", command=lambda: master.show_frame(StartPage)).pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()
