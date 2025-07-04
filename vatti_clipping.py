import pyclipper
import matplotlib.pyplot as plt

def draw_polygon(ax, polygon, color, label=None):
    if not polygon:
        return
    for poly in polygon:
        poly = poly + [poly[0]]  # cerrar el polígono
        x, y = zip(*poly)
        ax.plot(x, y, color=color, label=label)

subject = [[(0, 0), (0, 100), (100, 100), (100, 0)]]
clip = [[(50, 50), (50, 150), (150, 150), (150, 50)]]

pc = pyclipper.Pyclipper()
pc.AddPath(subject[0], pyclipper.PT_SUBJECT, True)
pc.AddPath(clip[0], pyclipper.PT_CLIP, True)

solution = pc.Execute(pyclipper.CT_INTERSECTION, pyclipper.PFT_EVENODD, pyclipper.PFT_EVENODD)

fig, ax = plt.subplots()
draw_polygon(ax, subject, 'blue', 'Sujeto')
draw_polygon(ax, clip, 'red', 'Clip')
draw_polygon(ax, solution, 'green', 'Resultado')

plt.legend()
plt.gca().set_aspect('equal', adjustable='box')
plt.title("Recorte de Vatti (Intersección)")
plt.grid(True)
plt.show()
