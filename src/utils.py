from tkinter import Tk, Frame

DAYS = {
    "Sun": "Sunday",
    "Mon": "Monday",
    "Tue": "Tuesday",
    "Wed": "Wednesday",
    "Thu": "Thursday",
    "Fri": "Friday",
    "Sat": "Saturday",
    "Sun": "Sunday"
}

MONTHS = {
    "Jan": "January",
    "Feb": "February",
    "Mar": "March",
    "Apr": "April",
    "May": "May",
    "Jun": "June",
    "Jul": "July",
    "Aug": "August",
    "Sep": "September",
    "Oct": "October",
    "Nov": "November",
    "Dec": "December"
}

LOCATIONS = {
    "left": (0, 0),
    "bottom": (4, 0)
}


class Container:

    def __init__(self):
        self.root = Tk()
        self.modules = []

        self.root.attributes('-fullscreen', True)
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        self.root.configure(background="black")

    def add_module(self, module, side):
        self.modules.append(module(Frame(self.root, bg="black")))
        location = LOCATIONS[side]
        self.modules[-1].grid(row=location[0], column=location[1])

    def start(self):
        self.root.mainloop()
