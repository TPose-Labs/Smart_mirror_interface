from tkinter import *
from modules import TwitterModule, ClockModule

root = Tk()
root.attributes('-fullscreen', True)
root.bind('<Escape>',lambda e: root.destroy())
root.configure(background="black")

f1 = Frame(root, bg="black")
ClockModule(f1)
f2 = Frame(root, bg="black")
TwitterModule(f2)
f1.pack(side="left")
f2.pack(side="bottom")

root.mainloop()