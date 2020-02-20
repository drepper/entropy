import spacefilling.hilbert as hilbert
import colormaps.moreland as moreland
import entropy
import numpy as np
import tkinter
import math


if __name__ == '__main__':
    import sys
    fname = sys.argv[1]

    colormap = moreland.make_black_body()
    colortable = colormap.get_table(256, byte = True, real = False)
    colors = np.array([ '#{:02x}{:02x}{:02x}'.format(*colortable['RGB'][c]) for c in range(256) ])

    e = entropy.Entropy(fname = fname)
    filterwidth = 256
    it = e.compute(filterwidth)
    res = [ int(it[i] * 256 / math.log(filterwidth, 2)) for i in it.range() ]

    maxwidth = 1600
    maxheight = 1200

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

    canvas.update()
    canvas.postscript(file = "test.ps", colormode = 'color')

    tkinter.mainloop()
