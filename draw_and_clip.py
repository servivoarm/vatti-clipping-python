import matplotlib
matplotlib.use('TkAgg')  # <- 👈 Esta línea es CLAVE

import matplotlib.pyplot as plt
import pyclipper

# Variables globales
subject_polygon = []
clip_polygon = []
current_polygon = []
drawing_subject = True
finished = False

fig, ax = plt.subplots()
ax.set_title("Dibuja con el mouse. 'c' cierra polígono, 'n' cambia, 'Enter' recorta, 'r' reinicia")
ax.set_aspect('equal')

ax.set_xlim(0,100)
ax.set_ylim(0,100)

def redraw():
    ax.clear()
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    if subject_polygon:
        poly = subject_polygon + [subject_polygon[0]]
        ax.plot(*zip(*poly), 'b-', label='Sujeto')
        ax.scatter(*zip(*subject_polygon), c='b', s=30)
    if clip_polygon:
        poly = clip_polygon + [clip_polygon[0]]
        ax.plot(*zip(*poly), 'r-', label='Clip')
        ax.scatter(*zip(*subject_polygon), c='r', s=30)
    if current_polygon:
        ax.plot(*zip(*current_polygon), 'k--', label = 'Dibujando')
        ax.scatter(*zip(*current_polygon), c='k', s=30)

    ax.legend()
    ax.set_title("Clic para dibujar. 'c'=cerrar , 'n'=cambiar, Enter=recorrer,'r'=reiniciar")
    ax.grid(True)
    plt.draw()

def onclick(event):
    global current_polygon
    if event.inaxes != ax or finished:
        return
    if event.xdata is None or event.ydata is None:
        return
    x, y = event.xdata, event.ydata
    current_polygon.append((x, y))
    redraw()

def onkey(event):
    global current_polygon, subject_polygon, clip_polygon, drawing_subject, finished

    if event.key == 'c':  # cerrar el polígono actual
        if len(current_polygon) >= 3:
            print("Polígono cerrado(virtualmente).")
        else:
            print("Agrega al menos 3 puntos.")
        redraw()

    elif event.key == 'n':  # cambiar entre sujeto y clip
        if drawing_subject:
            if len(current_polygon) >= 3:
                subject_polygon[:] = current_polygon[:]
                print("Sujeto guardado.")
            else:
                print("Sujeto invalido. Debe tener al menos 3 puntos")
        else:
            if len(current_polygon) >= 3:
                clip_polygon[:] = current_polygon[:]
                print("Sujeto guardado.")
            else:
                print("Clip inválido. Debe tener al menos 3 puntos.")
        current_polygon.clear()
        drawing_subject = not drawing_subject
        redraw()

    elif event.key == 'enter':
        if len(subject_polygon) < 3 or len(clip_polygon) < 3:
            print("Error, faltan poligonos validos")
            return

        pc = pyclipper.Pyclipper()
        pc.AddPath([(int(x), int(y)) for x, y in subject_polygon], pyclipper.PT_SUBJECT , True)
        pc.AddPath([(int(x), int(y)) for x, y in clip_polygon], pyclipper.PT_CLIP, True)
        result = pc.Execute(pyclipper.CT_INTERSECTION, pyclipper.PFT_EVENODD, pyclipper.PFT_EVENODD)

        redraw()
        for poly in result:
            poly = poly + [poly[0]]
            ax.plot(*zip(*poly), 'g-', linewidth=2, label='Resultado')
        plt.draw()
        finished = True
        print("Intersección completada.")

    elif event.key == 'r':  # reiniciar todo
        print("Reiniciando...")
        current_polygon.clear()
        subject_polygon.clear()
        clip_polygon.clear()
        finished = False
        drawing_subject = True
        redraw()

# Eventos
fig.canvas.mpl_connect('button_press_event', onclick)
fig.canvas.mpl_connect('key_press_event', onkey)

# Mostrar gráfico
redraw()
plt.show()
