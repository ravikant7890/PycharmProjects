from igraph import *
from collections import Counter
import sys
import math
import subprocess
import tempfile
#
# if (len(sys.argv)!=1):
#     print "Usage grid.py lenght width"
#     print "Example:"
#     print "grid.py 5 4"
#     quit()

m=int(sys.argv[1])
n=int(sys.argv[1])

# parts=int(sys.argv[2])
# snap_file=(sys.argv[2])



g=Graph(m*n)

node_map={}
all_nodes = []
edge_map=[]

adjList_map={}

i=0
for x in range(m):
    for y in range(n):
        all_nodes.append((x, y))
        node_map[(x,y)]=i
        i=i+1

# print node_map



edge_list=[]
dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
for node in all_nodes:

    for dir in dirs:

        neighbor = (node[0] + dir[0], node[1] + dir[1])
        # print neighbor
        if 0 <= neighbor[0] < m and 0 <= neighbor[1] < n:
            edge_list.append([node,neighbor])
            edge_map.append([node_map[node],node_map[neighbor]])
            if(adjList_map.has_key(node_map[node])):
                x=adjList_map[node_map[node]]
                x.add(node_map[neighbor])
                adjList_map[node_map[node]]=x
            else:
                x=set()
                x.add(node_map[neighbor])
                adjList_map[node_map[node]]=x
            #if 0 <= neighbor[0] < 20 and 0 <= neighbor[1] < 10:




# print result

for k in adjList_map.keys():
    print str(k)+ ":["+ str(adjList_map[k])+"]"
