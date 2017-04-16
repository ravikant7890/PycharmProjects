import networkx as nx
import matplotlib.pyplot as plt
import sys


G=nx.Graph()

fh=open(sys.argv[1], 'rb')

for line in fh:

    src= line.split()[0].split(",")[0]

    src_pid=line.split()[0].split(",")[1]

    G.add_node(src,pid=src_pid)

    dst= line.split()[1].split(",")[0]

    dst_pid=line.split()[1].split(",")[1]

    G.add_node(dst,pid=dst_pid)

    G.add_edge(src,dst)



# for node in G.nodes():
#     print G.node[node]
#     print G.node[node]['pid']


color_map = {'1':'b', '2':'#FF0099', '3':'#660066'}
#
# G=nx.read_edgelist(fh)
#
# print G.edges()
#
# print G.nodes()
#
# print nx.diameter(G)
#
nx.draw_networkx(G,node_color=[color_map[G.node[node]['pid']] for node in G])

plt.show()