from operator import truediv

import pyclipper
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MlpPolygon

subject_polygon = []
clip_polygon = []
current_polygon = []
drawing_subject = True
finished = False

fig, ax = plt.subplots()
plt.title("Haz clic para dibujar. Presiona 'n' para cambiar de poligono, 'Enter' para recortar")

def redraw():
    ax.clear()
    if subject_polygon:
        poly = subject_polygon + [subject_polygon[0]]
        ax.plot(*zip(*poly), 'b-',label='Sujeto')
    if clip_polygon:
        poly = clip_polygon + [clip_polygon[0]]
        ax.plot(*zip(*poly),'r-',label= 'Clip')
    if current_polygon:
        ax.plot(*zip(*current_polygon),'k--')
    ax.legend()
    ax.set_aspect('equal')
    plt.draw()

def onclick(event):
    global current_polygon
    if event.inaxes != ax or finished:
        return
    x, y= round(event.xdata), round(event.ydata)
    current_polygon.append((x,y))
    redraw()

def onkey(event):
    global current_polygon , subject_polygon, clip_polygon,drawing_subject , finished

    if event.key == 'n':
        if drawing_subject:
            subject_polygon = current_polygon[:]
            print("Sujeto finalizado")
        else:
            clip_polygon = current_polygon[:]
            print("Clip finalizado")
        current_polygon = []
        drawing_subject = not drawing_subject
        redraw()

    elif event.key == 'enter':
        if not subject_polygon or not clip_polygon:
            print("Falta uno de los polígonos")
            return

        pc = pyclipper.Pyclipper()
        pc.AddPath(subject_polygon, pyclipper.PT_SUBJECT, True)
        pc.AddPath(clip_polygon, pyclipper.PT_CLIP, True)

        result = pc.Execute(pyclipper.CT_INTERSECTION, pyclipper.PFT_EVENODD, pyclipper.PFT_EVENODD)

        redraw()
        for poly in result:
            poly = poly + [poly[0]]
            ax.plot(*zip(*poly), 'g-', linewidth = 2, label = 'Intersección')
        plt.draw()
        finished = True
        print("Recorte aplicado")

fig.canvas.mpl_connect('button_press_event', onclick)
fig.canvas.mpl_connect('key_press_event', onkey)

plt.show()