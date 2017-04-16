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

for edge in edge_list:
    # print [node_map[edge[0]],node_map[edge[1]]]
    g.add_edge(node_map[edge[0]],node_map[edge[1]])


# ######################## Visualization #######################################################
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

center=int(math.floor( m/2)*n+math.ceil( n/2))

print "center is "+str(center)

result=g.shortest_paths_dijkstra(source=center, target=None, weights=None, mode=OUT)
#
# print (result[0])

c = Counter( result[0] )
print "Simulation result (superstep,frontierSet Size)"
print( c.items() )




# plot(g, layout = layout)


if(m==n):

    ss_required=2*math.floor(m)

    #condition is 3 + 2x <= m
    full_diamond_ss= (m-3)/2 +1  #FIXME: 1 is added because x=0 refers to SS=1

    #generate sequence
    fsize={}
    fsize[0]=1

    #for 2D sequence is 1,(2*4-4),(3*4-4),......
    for i in range(1,full_diamond_ss+1):

        fsize[i]=((i+1)*4)-4


    max_size=fsize[full_diamond_ss]
    ss=full_diamond_ss+1

    while max_size!=0:

        fsize[ss]=max_size
        max_size=max_size-4
        ss=ss+1

    print "Model Result"
    print fsize

else :

    ss_required=math.floor(m)+ math.floor(n)

    max_dim=max(m,n)
    min_dim=min(m,n)
    #condition is 3 + 2x <= m
    full_diamond_ss= (min_dim-3)/2 +1  #FIXME: 1 is added because x=0 refers to SS=1

    #generate sequence
    fsize={}
    fsize[0]=1

    #for 2D sequence is 1,(2*4-4),(3*4-4),......
    for i in range(1,full_diamond_ss+1):

        fsize[i]=((i+1)*4)-4


    max_size=fsize[full_diamond_ss]
    ss=full_diamond_ss+1


    # print fsize
    # print max_dim-min_dim


    #for max-min ss size will be 2*min

    for i in range(0,(max_dim-min_dim)/2):

        fsize[ss]=2*min_dim
        ss=ss+1

    max_size=2*min_dim

    # print fsize
    max_size=max_size-2 #At the end 2 point would be lost

    while max_size!=0:
        fsize[ss]=max_size
        max_size=max_size-4
        ss=ss+1

    print "Model Result"
    print fsize