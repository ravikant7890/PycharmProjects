# # from igraph import *
# # from collections import Counter
# # import sys
# # import math
# #
# # grid_size=int(sys.argv[1])
# # g = Graph.Lattice([grid_size,grid_size,grid_size])
# # n=grid_size
# # m=grid_size
# # # g.vs["label"]=g.vs["id"]
# #
# # # print g
# #
# # node_map={}
# # all_nodes = []
# # i=0
# # for x in range(m):
# #     for y in range(m):
# #         for z in range(m):
# #             all_nodes.append((x, y, z))
# #             node_map[(x,y,z)]=i
# #             i=i+1
# #
# # # layout = g.layout("grid_3d")
# # l=[]
# # for i in range(0,grid_size*grid_size*grid_size):
# #    l.append(i)
# #
# #
# # g.vs["name"]=l
# # g.vs["label"] = g.vs["name"]
# # # plot(g, layout = layout)
# #
# # center=n*n*math.floor(n/2)+n*math.ceil(n/2)+math.ceil(n/2)
# #
# # print "centre is "+str(center)
# #
# #
# # center=node_map[(math.floor( m/2),math.floor( m/2),math.floor( m/2))]
# #
# # print "center is "+str(center)
# #
# #
# # #################################
# #
# #
# #
# #
# # result=g.shortest_paths_dijkstra(source=center, target=None, weights=None, mode=OUT)
# # #
# # # print (result[0])
# #
# # c = Counter( result[0] )
# # print "Simulation result (superstep,frontierSet Size)"
# # print( c.items() )
# #
# #
# #
# #
# # f1=1
# # f2=6
# #
# # prev=6
# # l=[]
# # l.append(1)
# # l.append(6)
# # d=3
# # for i in range(2,n):
# #     new_val=4*((i)*(d-1)-1)+prev
# #     l.append(new_val)
# #     prev=new_val
# # print "Model result (superstep,frontierSet Size)"
# # print l
#
# l=[0,2,8,10,32,34,40,42]
#
# hypercubeid=0
# hypercube_map={}
#
# for i in l:
#
#     elements=[]
#     # 0
#     elements.append(i)
#     elements.append(i+1)
#     elements.append(i+4)
#     elements.append(i+16)
#     elements.append(i+64)
#     # 1
#     elements.append(i+1+4)
#     elements.append(i+1+16)
#     elements.append(i+1+64)
#
#     # 4
#     # elements.append(i+4+1)
#     elements.append(i+4+16)
#     elements.append(i+4+64)
#
#     # 5
#     elements.append(i+1+4+16)
#     elements.append(i+1+4+64)
#
#     #16
#     elements.append(i+16+64)
#     # 17
#     elements.append(i+1+16+64)
#     #20
#     elements.append(i+4+16+64)
#     # 21
#     elements.append(i+4+1+16+64)
#
#
#     hypercube_map[hypercubeid]=elements
#
#     hypercubeid=hypercubeid+1
#
#
#
#
#
# for k in hypercube_map.keys():
#
#     hypercubeid=hypercubeid+1
#
#     l=[]
#     for v in hypercube_map[k]:
#
#         l.append(v+128)
#
#     hypercube_map[hypercubeid]=l
#
#
# for k in hypercube_map.keys():
#
#     print (hypercube_map[k])
#
#
#
#
# print  "====================================================="
#
#
# # hypercube_map=[]
#
#
# l=[0,2,8,10,32,34,40,42]
#
# hypercubeid=0
# hypercube_map={}
#
# for i in l:
#
#     elements=[]
#     # 0
#     elements.append(i)
#     elements.append(i+1)
#     elements.append(i+4)
#     elements.append(i+16)
#     # elements.append(i+64)
#     # 1
#     elements.append(i+1+4)
#     elements.append(i+1+16)
#     # elements.append(i+1+64)
#
#     # 4
#     # elements.append(i+4+1)
#     elements.append(i+4+16)
#     # elements.append(i+4+64)
#
#     # 5
#     elements.append(i+1+4+16)
#     # elements.append(i+1+4+64)
#
#     #16
#     # elements.append(i+16+64)
#     # 17
#     # elements.append(i+1+16+64)
#     #20
#     # elements.append(i+4+16+64)
#     # 21
#     # elements.append(i+4+1+16+64)
#
#
#     hypercube_map[hypercubeid]=elements
#
#     hypercubeid=hypercubeid+1
#
#
#
#
# for k in hypercube_map.keys():
#
#     print (hypercube_map[k])
#
#
#
#
from igraph import *

# g=Graph.Static_Power_Law(50,200,10)

g = Graph.Read_Ncol(sys.argv[1], directed=True)


layout = g.layout("grid")
l=[]
for i in range(0,int(Graph.vcount(g))):
   l.append(i)

# g.vs["name"]=l
# g.vs["label"] = g.vs["name"]
# plot(g, layout = layout)

# plot(g,color_name_to_rgb("rgb(100%, 50%, 0%)",palette=None))

# c=rgba(red, green, blue, alpha)
g.vs["color"] = 'grey'
plot(g)

