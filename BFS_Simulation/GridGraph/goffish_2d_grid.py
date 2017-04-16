from igraph import *
from collections import Counter
import sys
import math
import subprocess
import tempfile

if (len(sys.argv)!=3):
    print "Usage grid.py lenght width"
    print "Example:"
    print "grid.py 5 4"
    quit()

m=int(sys.argv[1])
n=int(sys.argv[1])

parts=int(sys.argv[2])
# snap_file=(sys.argv[2])



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
dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
for node in all_nodes:

    for dir in dirs:

        neighbor = (node[0] + dir[0], node[1] + dir[1])
        # print neighbor
        if 0 <= neighbor[0] < m and 0 <= neighbor[1] < n:
            edge_list.append([node,neighbor])
            #if 0 <= neighbor[0] < 20 and 0 <= neighbor[1] < 10:




# print result

# print edge_list
adjlist={}

for i in node_map.values():
    l=[]
    adjlist[i+1]=l

# print adjlist

# snap_graphfile = open(snap_file, 'w')


for edge in edge_list:
    # print [node_map[edge[0]],node_map[edge[1]]]
    g.add_edge(node_map[edge[0]],node_map[edge[1]])
    # print "edge "+str( node_map[edge[0]]+1)+","+str(node_map[edge[1]]+1)


    # snap_graphfile.write(str( node_map[edge[0]])+"\t"+str(node_map[edge[1]])  + "\n")


    l=adjlist[node_map[edge[0]]+1]
    l.append(node_map[edge[1]]+1)
    adjlist[node_map[edge[0]]+1]=l
#
# print adjlist
# snap_graphfile.close()
# print edge_list

################# forming metis graph #####################
#
f = tempfile.NamedTemporaryFile(delete=False)
f.write(str(len(adjlist.keys()))+" "+str(len(edge_list)/2)+"\n")
for i in adjlist.keys():
    f.write( " ".join( str(v) for v in list(adjlist[i])) + "\n")

f.close()

print f.name

metis_command_string="gpmetis "+str(f.name)+" "+str(parts)


run_proc1=subprocess.Popen(metis_command_string ,shell=True)

subprocess.Popen.wait(run_proc1)

################## read file & visualize
out_file_name=f.name+".part."+str(parts)

with open(out_file_name, "r") as ins:
    partition = []
    for line in ins:
        partition.append(int(line))

# print partition

# ######################## Visualization #######################################################
layout = g.layout("kamada_kawai")
# l=[]
# for i in range(0,m*n):
#    l.append(i)


g.vs["name"]=partition
g.vs["label"] = g.vs["name"]
# color_dict = {0: "blue", 1: "pink"}
pal = RainbowPalette(n=20)
g.vs["color"] = [pal[gender] for gender in g.vs["name"]]
plot(g, layout = layout)
# ####################### Visualization #######################################################
