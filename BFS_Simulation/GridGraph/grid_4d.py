from igraph import *
from collections import Counter
import sys
import math



m=int(sys.argv[1])
# n=int(sys.argv[2])
size=m*m*m*m
g=Graph(size)
n=m

node_map={}
all_nodes = []
i=0
for w in range(m):
    for x in range(m):
        for y in range(m):
            for z in range(m):
                all_nodes.append((w, x, y, z))
                node_map[(w,x,y,z)]=i
                i=i+1

# print node_map

# exit()


edge_list=[]
dirs = [(1, 0, 0, 0), (0, 1, 0, 0), (-1, 0, 0, 0), (0, -1, 0, 0) , (0, 0, 1, 0), (0, 0, -1, 0), (0, 0, 0, 1), (0, 0, 0, -1) ]
for node in all_nodes:

    for dir in dirs:

        neighbor = (node[0] + dir[0], node[1] + dir[1], node[2] + dir[2] ,node[3] + dir[3] )
        # print neighbor
        if 0 <= neighbor[0] < m and 0 <= neighbor[1] < m and  0 <= neighbor[2] < m  and  0 <= neighbor[3] < m:
            edge_list.append([node,neighbor])
            #if 0 <= neighbor[0] < 20 and 0 <= neighbor[1] < 10:




for edge in edge_list:
    # print [node_map[edge[0]],node_map[edge[1]]]
    g.add_edge(node_map[edge[0]],node_map[edge[1]])





# layout = g.layout("grid_3d")
# l=[]
# for i in range(0,size):
#    l.append(i)
#
#
# g.vs["name"]=l
# g.vs["label"] = g.vs["name"]
# plot(g, layout = layout)



# print len(node_map)
# print edge_list
# print len(edge_list)
center=node_map[(math.floor( m/2),math.floor( m/2),math.floor( m/2),math.floor( m/2))]

print "center is "+str(center)

result=g.shortest_paths_dijkstra(source=center, target=None, weights=None, mode=OUT)
#
# print (result[0])

c = Counter( result[0] )
print "Simulation result (superstep,frontierSet Size)"
print( c.items() )


#
# f1=1
# f2=8
#
# prev=8
# l=[]
# l.append(1)
# l.append(8)
# d=4
# for i in range(2,9):
#     new_val=4*((i)*(d-1)-1)+prev
#     l.append(new_val)
#     prev=new_val
# print "Model result (superstep,frontierSet Size)"
# print l