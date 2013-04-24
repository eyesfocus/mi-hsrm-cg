file_a = file("polygonA.dat")
file_z = file("polygonZ.dat")
polygon_z = [(float(y[0]),float(y[1])) for y in [tuple(x.split()) for x in [lines.strip() for lines in file_z.readlines()]]]
polygon_a = [(float(y[0]),float(y[1])) for y in [tuple(x.split()) for x in [lines.strip() for lines in file_a.readlines()]]]


polygon_a = [(y[0]*400, y[1]*400) for y in polygon_a]
polygon_z = [(y[0]*400, y[1]*400) for y in polygon_z]


print polygon_a
#print polygon_z[0]
#print polygon_a[0]

#pola = [(58, 372)]
#polz = [(110, 34)]

#pola = [(1,1),(2,2)]
#polz = [(1,1),(2,2)]

time= 0.5

#print map(lambda a,b: (a[0]+b[0], a[1]+ b[1]), pola, [(time*x[0], time*x[1]) for x in map(lambda p,q: (q[0]-p[0],q[1]-p[1]), pola, polz)])

pola.reverse()
#print pola
