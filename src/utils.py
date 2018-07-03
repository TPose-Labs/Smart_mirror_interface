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
    "bottom": (1, 0),
    "right": (0, 1),
    "rbot": (1, 1)
}


def remove_unicode(_str):
    char_list = []
    for i in range(len(_str)):
        if ord(_str[i]) in range(65536):
            char_list.append(_str[i])
    _str = ''
    for i in char_list:
        _str += i
    return _str


def overrides(interface_class):
    def overrider(method):
        assert(method.__name__ in dir(interface_class))
        return method
    return overrider


class Container:

    def __init__(self):
        self.root = Tk()
        self.modules = []

        self.root.attributes('-fullscreen', True)
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        self.root.configure(background="black")

    def add_module(self, module, side, **kwargs):
        if "stocks" in kwargs.keys():
            self.modules.append(module(Frame(self.root, bg="black"),
                                kwargs["stocks"]))
        else:
            self.modules.append(module(Frame(self.root, bg="black")))
        location = LOCATIONS[side]
        self.modules[-1].grid(row=location[0], column=location[1])

    def start(self):
        self.root.mainloop()
