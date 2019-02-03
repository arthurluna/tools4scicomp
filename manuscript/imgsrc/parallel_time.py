from pyx import color, deco, graph, style

cpus = ['i7-6700hq',]
data = {}
for cpu in cpus:
    data[cpu] = []
    with open(cpu+'.dat') as fh:
        for line in fh:
            nr, t4, t1 = line.rstrip('\n').split()
            nr = int(nr)
            t1 = float(t1)
            t4 = float(t4)
            data[cpu].append((t1, t4))
    data[cpu] = [(2**nr, data[cpu][0][0]/t4, t1/t4)
                 for nr, (t1, t4) in enumerate(data[cpu])]

logparter = graph.axis.parter.log(tickpreexps=
                [graph.axis.parter.preexp([graph.axis.tick.rational(1, 1)], 2)])
g = graph.graphxy(width=8,
        x=graph.axis.log(min=1, max=128, parter=logparter,
                         title='number of divisions per axis'),
        y=graph.axis.lin(min=0, max=6.5, title='acceleration'))
for nr, cpu in enumerate(cpus):
    g.plot(graph.data.points(data[cpu], x=1, y=2),
            [graph.style.line(lineattrs=[style.linestyle.dotted]),
             graph.style.symbol(symbol=graph.style.symbol.circle,
    	         size=0.1, symbolattrs=[deco.filled([color.grey(nr)])])
	    ])
    g.plot(graph.data.points(data[cpu], x=1, y=3),
            [graph.style.line(lineattrs=[style.linestyle.solid]),
             graph.style.symbol(symbol=graph.style.symbol.circle,
		 size=0.1, symbolattrs=[deco.filled([color.grey(nr)])])
            ])
g.writePDFfile()
g.writeGSfile(device="png16m", resolution=600)
