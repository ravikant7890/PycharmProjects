from igraph import *
from collections import Counter
import sys
import math

grid_size=int(sys.argv[1])
g = Graph.Lattice([grid_size,grid_size])

# g.vs["label"]=g.vs["id"]

print g

layout = g.layout("grid")
l=[]
for i in range(0,grid_size*grid_size):
   l.append(i)


g.vs["name"]=l
g.vs["label"] = g.vs["name"]
plot(g, layout = layout)

# exit()


print(g.vs)

center=int(math.floor( grid_size/2)*grid_size+math.ceil( grid_size/2))

print "center is "+str(center)

result=g.shortest_paths_dijkstra(source=center, target=None, weights=None, mode=OUT)
#
print (result[0])

c = Counter( result[0] )
print "Simulation result (superstep,frontierSet Size)"
print( c.items() )