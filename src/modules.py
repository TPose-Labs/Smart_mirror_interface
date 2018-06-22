from tkinter import Label
from tkinter.font import Font
import datetime
import calendar

class ClockModule:

    def __init__(self, root):
        montserrat_big = Font(family="Helvetica", size=72)
        montserrat_small = Font(family="Helvetica", size=48)

        self.root = root
        self.day = Label(root, font=montserrat_big, fg="white", bg="black",
                         padx=5)
        self.day.grid(row=0, sticky="w")
        self.fulldate = Label(root, font=montserrat_small, fg="white",
                              bg="black", padx=5)
        self.fulldate.grid(row=1, column=0, sticky="w")
        self.clock = Label(root, font=montserrat_small, fg="white", bg="black",
                           padx=5)
        self.clock.grid(row=2, column=0, sticky="w")

        self.time = ""
        self.dotw = ""
        self.date = ""
        self.loop()

    def loop(self):
        currday = datetime.datetime.today()
        dotw = calendar.day_name[currday.weekday()] + ","
        date = currday.strftime("%B %d, %Y")
        time = currday.strftime("%I:%M %p")
        if self.time != time:
            self.time = time
            self.clock.config(text=time)
        if self.dotw != dotw:
            self.dotw = dotw
            self.day.config(text=dotw)
        if self.date != date:
            self.date = date
            self.fulldate.config(text=date)
        self.day.after(1000, self.loop)
