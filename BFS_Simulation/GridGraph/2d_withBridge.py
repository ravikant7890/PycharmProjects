from igraph import *
from collections import Counter
import sys
import math

if (len(sys.argv)!=3):
    print "Usage grid.py lenght width"
    print "Example:"
    print "grid.py 5 4"
    quit()

m=int(sys.argv[1])
n=int(sys.argv[2])

g=Graph(m*n)

node_map={}
all_nodes = []
i=0
for x in range(m):
    for y in range(n):
        all_nodes.append((x, y))
        node_map[(x,y)]=i
        i=i+1

# print node_map



edge_list=[]
dirs = [(1, 0), (0, 1), (-1, 0), (0, -1), (1,1), (-1,1), (-1,-1), (1,-1)]
for node in all_nodes:

    for dir in dirs:

        neighbor = (node[0] + dir[0], node[1] + dir[1])
        # print neighbor
        if 0 <= neighbor[0] < m and 0 <= neighbor[1] < n:
            edge_list.append([node,neighbor])
            #if 0 <= neighbor[0] < 20 and 0 <= neighbor[1] < 10:




# print result

# print edge_list

for edge in edge_list:
    # print [node_map[edge[0]],node_map[edge[1]]]
    g.add_edge(node_map[edge[0]],node_map[edge[1]])


######################## Visualization #######################################################
# layout = g.layout("kamada_kawai")
# l=[]
# for i in range(0,m*n):
#    l.append(i)
#
#
# g.vs["name"]=l
# g.vs["label"] = g.vs["name"]
# plot(g, layout = layout)
######################## Visualization #######################################################
#
center=int(math.floor( m/2)*n+math.ceil( n/2))

print "center is "+str(center)

result=g.shortest_paths_dijkstra(source=center, target=None, weights=None, mode=OUT)
#
# print (result[0])

c = Counter( result[0] )
print "Simulation result (superstep,frontierSet Size)"
print( c.items() )
