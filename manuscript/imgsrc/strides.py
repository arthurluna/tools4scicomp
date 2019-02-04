import sys
import os.path

from pyx import canvas, color, deco, path, text, trafo, unit

def make_stride_figure(lowerstride, upperstride=1, nrentries=6):
    c = canvas.canvas()
    ht = 0.5
    wd = 2
    dist = 0.2
    textcolor = color.hsb(0.02, 1, 0.6)
    for n in range(nrentries):
        x = n*(wd+dist)
        c.stroke(path.rect(x, 0, wd, ht))
        c.text(x+0.5*wd, 0.5*ht, str(n), [text.halign.center, text.valign.middle])

    for n in range(nrentries-1):
        x = n*(wd+dist)
        c.stroke(path.curve(x-dist/3, ht+0.5*dist,
                            x+0.3*wd, ht+3*dist,
                            x+0.7*wd, ht+3*dist,
                            x+wd+dist/3, ht+0.5*dist),
                 [deco.earrow.large])
        c.text(x+0.5*wd, ht+3.2*dist, r'\Large 8', [text.halign.center, textcolor])

    if lowerstride:
        for n in range((nrentries-1)//lowerstride):
            x = n*lowerstride*(wd+dist)
            c.stroke(path.curve(x-dist/3, -0.5*dist,
                                x+0.5*wd, -5*dist,
                                x+(lowerstride-0.5)*wd+lowerstride*dist, -5*dist,
                                x+lowerstride*wd+(lowerstride-0.7)*dist, -0.5*dist),
                     [deco.earrow.large])
            c.text(x+0.5*lowerstride*wd+dist,-5.2*dist, r'\Large %i' % (lowerstride*8),
                   [text.halign.center, text.valign.top, textcolor])
    return c

text.set(text.LatexRunner)
text.preamble(r'\usepackage[sfdefault,scaled=.85,lining]{FiraSans}\usepackage{newtxsf}')
unit.set(xscale=1.6, wscale=1.5)

c = canvas.canvas()
for nr, stride in enumerate((2, 3, 0)):
    c.insert(make_stride_figure(stride), [trafo.translate(0, 6*nr)])
    s1 = 8*stride
    if stride:
        s = ', '.join([str(s1), '8'])
    else:
        s = '8,'
    c.text(0, 6*nr+2.5, '\\Large ({})'.format(s))

xoff = -5
yoff = 1
for nr, matrix in enumerate((r'$\begin{{pmatrix}}{} & {}\\{} & {}\\{} & {}\end{{pmatrix}}$',
                             r'$\begin{{pmatrix}}{} & {} & {}\\{} & {} & {}\end{{pmatrix}}$',
                             r'$\begin{{pmatrix}}{} & {} & {} & {} & {} & {}\end{{pmatrix}}$')):
    m = matrix.format(*map(lambda x: '\\text{}'.format(x), range(6)))
    c.text(xoff, 6*nr+yoff, '\\Large '+m, [text.halign.center, text.valign.middle])

c.writePDFfile()
c.writeGSfile(device="png16m", resolution=300)
