import networkx as nx
import matplotlib.pyplot as plt
import sys
import os

G=nx.Graph()

def nodes_connected(u, v):
    return u in G.neighbors(v)


parent_folder=sys.argv[1]

os.chdir(parent_folder)

cmd="ls -1 SG*"

out_dir_list=[]
for out_dir in os.popen(cmd).read().split("\n"):
    if out_dir:
        out_dir_list.append(out_dir)

###################### Precompute stats for each metaVertex ###############
# diameter
# eccentricity of boundary vertex
# V, E, R
# 


######Form metagraph

for sg in out_dir_list:

    cmd="grep  -w REMOTEEDGE  "+sg+" |head"

    for line in os.popen(cmd).read().split("\n"):
        if line:

            print line
            src= line.split(",")[0]

            src_pid=line.split(",")[1]

            G.add_node(src,pid=src_pid)

            dst= line.split(",")[3]

            dst_pid=line.split(",")[4]

            G.add_node(dst,pid=dst_pid)

            G.add_edge(src,dst)


            # break

nx.draw_networkx(G)

plt.show()
### grep remote edge ... it forms an edgelist


### Add attributes to the vertices


### BFS Simulation