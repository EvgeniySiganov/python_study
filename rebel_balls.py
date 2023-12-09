import random
import tkinter as tk
import time

root = tk.Tk()
width = 400
height = 400
canvas = tk.Canvas(root, width=width, height=height, bg='white')
canvas.pack()

colors = ['red', 'blue', 'orange', 'green', 'yellow']


def create_oval():
    r1 = random.randint(0, 100)
    r2 = random.randint(100, 200)
    return canvas.create_oval(r1, r1, r2, r2, fill=random.choice(colors))


circles = []
for i in range(5):
    data = {}
    data["dx"] = random.randint(-10, 10)
    data["dy"] = random.randint(-10, 10)
    data["id"] = create_oval()
    circles.append(data)

while True:
    for i in circles:
        x0, y0, x1, y1 = canvas.coords(i['id'])
        if x0 < 0 or x1 < 0 or x0 > 400 or x1 > 400:
            i["dx"] = i["dx"] * -1
        if y0 < 0 or y1 < 0 or y0 > 400 or y1 > 400:
            i["dy"] = i["dy"] * -1
        canvas.move(i["id"], i["dx"], i["dy"])
    canvas.update()
    time.sleep(0.01)