from igraph import *
from collections import Counter
import sys
import math



m=int(sys.argv[1])
# n=int(sys.argv[2])
size=m*m*m
g=Graph(size)
n=m

# node_map={}
# all_nodes = []
# i=0
# for x in range(m):
#     for y in range(m):
#         for z in range(m):
#             all_nodes.append((x, y, z))
#             node_map[(x,y,z)]=i
#             i=i+1
#
# # print node_map
#
# # exit()
#
#
# edge_list=[]
# dirs = [(1, 0, 0), (0, 1, 0), (-1, 0, 0), (0, -1, 0) , (0, 0, 1), (0, 0, -1)]
# for node in all_nodes:
#
#     for dir in dirs:
#
#         neighbor = (node[0] + dir[0], node[1] + dir[1], node[2] + dir[2] )
#         # print neighbor
#         if 0 <= neighbor[0] < m and 0 <= neighbor[1] < m and  0 <= neighbor[2] < m:
#             edge_list.append([node,neighbor])
#             #if 0 <= neighbor[0] < 20 and 0 <= neighbor[1] < 10:
#
#
#
#
# for edge in edge_list:
#     # print [node_map[edge[0]],node_map[edge[1]]]
#     g.add_edge(node_map[edge[0]],node_map[edge[1]])





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
# # print edge_list
# print len(edge_list)
# center=node_map[(math.floor( m/2),math.floor( m/2),math.floor( m/2))]
#
# print "center is "+str(center)

# result=g.shortest_paths_dijkstra(source=center, target=None, weights=None, mode=OUT)
# #
# # print (result[0])
#
# c = Counter( result[0] )
# print "Simulation result (superstep,frontierSet Size)"
# print( c.items() )


ss_count=int(3*math.floor(m/2))

print "ss count is "+str(ss_count)

########################




##########################
l=[]
l.append(1)
l.append(6)

frame_list=[0 for i in range(0,int(math.floor(m/2)))]

# print frame_list


mid=int(math.floor(m/2))-1

frame_list[mid]=4

frame_list[mid-1]=1

tmp=4

for k in range(2,ss_count+1):

    #check if first frame is touched
    if frame_list[0]< 4:
        tmp= tmp+4

    ###### tmp is increased for 1 but kept constant for 4 and decreses thereafter

    #check if first frame is expanded
    if frame_list[0]>4:
        tmp=tmp-4

    tmp=max(0,tmp)

    # tmp1=tmp -4
    #
    # tmp1=max(0,tmp1)

    l.append(2*sum(frame_list)+tmp) #tmp is middle element of the expansion

    # print "frame list :"+ str(frame_list)

    # for j in range(len(frame_list)):

    frame_list=frame_list[1:] + frame_list[:1]

    frame_list[len(frame_list)-1]=tmp


print "model result "
print l

