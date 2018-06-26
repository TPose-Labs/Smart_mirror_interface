from tkinter import *
from modules import TwitterModule, ClockModule

root = Tk()
root.attributes('-fullscreen', True)
root.bind('<Escape>',lambda e: root.destroy())
root.configure(background="black")

clock = ClockModule(Frame(root, bg="black"))
clock.pack(side="left")
twitter = TwitterModule(Frame(root, bg="black"))
twitter.pack(side="bottom")

root.mainloop()