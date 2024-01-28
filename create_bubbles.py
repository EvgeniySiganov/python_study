import random
import tkinter

window = tkinter.Tk()
width = 400
height = 400
canvas = tkinter.Canvas(window, width=width, height=height, bg='white')
canvas.pack()

colors = ['red', 'blue', 'orange', 'green', 'yellow']


def create_circle(x, y):
    radius = random.randint(0, 100)
    return canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=random.choice(colors))


def my_click(event):
    create_circle(event.x, event.y)


# left button of mouse
canvas.bind('<Button-1>', my_click)
window.mainloop()
