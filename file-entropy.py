import spacefilling.hilbert as hilbert
import colormaps.moreland as moreland
import entropy
import numpy as np
import tkinter
import math
import sys


def run():
    if len(sys.argv) < 2:
        print("Usage: {} FILENAME [PSFILE]".format(sys.argv[0]))
        sys.exit(1)
    fname = sys.argv[1]

    colormap = moreland.make_black_body()
    colortable = colormap.get_table(256, byte = True, real = False)
    colors = np.array([ '#{:02x}{:02x}{:02x}'.format(*colortable['RGB'][c]) for c in range(256) ])

    e = entropy.Entropy(fname = fname)
    filterwidth = 256
    it = e.compute(filterwidth)
    res = [ int(it[i] * len(colors) / math.log(filterwidth, 2)) for i in it.range() ]

    maxwidth = 2400
    maxheight = 1800

    h = hilbert.HilbertCurve(len(res))
    scalex = maxwidth / h.width
    scaley = maxheight / h.height
    scale = min(scalex, scaley)

    master = tkinter.Tk()
    canvas = tkinter.Canvas(master, width = scale * h.width, height = scale * h.height)
    canvas.pack()

    for d in h.range():
        x, y = h[d]
        canvas.create_rectangle(x * scale, y * scale, (x + 1) * scale, (y + 1) * scale, fill = colors[res[d]])

    if len(sys.argv) > 2:
        psfile = sys.argv[2]
        if not psfile.endswith('.ps'):
            psfile += ".ps"
        canvas.update()
        canvas.postscript(file = psfile, colormode = 'color')

    tkinter.mainloop()

run()
