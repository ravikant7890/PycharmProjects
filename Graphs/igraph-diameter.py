from igraph import *
import sys
import os



g = Graph.Read_Edgelist(sys.argv[1], directed=True)

v=Graph.vcount(g)

print v


d=Graph.diameter(g)

print d