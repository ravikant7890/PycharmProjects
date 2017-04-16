import random
from igraph import *
import sys

##############################graph formation ####################################

m=int(sys.argv[1])
n=int(sys.argv[1])

g=Graph(m*n)

node_map={}  ##maps (x,y) to single integer
all_nodes = []
i=0
for x in range(m):
    for y in range(n):
        all_nodes.append((x, y))
        node_map[(x,y)]=i
        i=i+1

edge_list=[]
adjList={}

for i in range(m*n):
    x=set()
    adjList[i]=x

dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
for node in all_nodes:

    for dir in dirs:

        neighbor = (node[0] + dir[0], node[1] + dir[1])
        # print neighbor
        if 0 <= neighbor[0] < m and 0 <= neighbor[1] < n:
            edge_list.append([node,neighbor])
            x=adjList[node_map[node]]
            x.add(node_map[neighbor])
            adjList[node_map[node]]=x


for edge in edge_list:
    # print [node_map[edge[0]],node_map[edge[1]]]
    g.add_edge(node_map[edge[0]],node_map[edge[1]])

''' adjList has adjlist structure of graph
key : vid
value: set of neighbours'''

# print adjList
#################Visualization#############################
    # layout = g.layout("kamada_kawai")
    # l=[]
    # for i in range(0,m*n):
    #    l.append(i)
    #
    # g.vs["name"]=l
    # g.vs["label"] = g.vs["name"]
    # plot(g, layout = layout)
#############run bfs################
center=int(math.floor( m/2)*n+math.ceil( n/2))

print "center is " +str(center)

''' result[0][i] has distance for ith vertex from the source vertex'''
result=g.shortest_paths_dijkstra(source=center, target=None, weights=None, mode=OUT)

###form map containing distance as key and value as vid:
print "distance for each vertex"
print result[0]
distance_map={}
l=[]
for i in range(0,len(result[0])):
    l.append(i)

# print l

dict_list = zip(l, result[0])

vertex_distance_map=dict(dict_list)

# print vertex_distance_map

distance_vertex_map = {}

for key, value in sorted(vertex_distance_map.iteritems()):
    distance_vertex_map.setdefault(value, []).append(key)


''' distance_vertex_map has key as distance while value is a list of vid with given distance'''
print "distance_vertex_map"
print distance_vertex_map



##########################Partitoning of the graph#######################################################
# number_of_partitions=3
number_of_partitions=int(sys.argv[2])
s=set()
# for i in range(0,9,1):
for i in range(0,m*n,1):
    s.add(i)

# slen=len(s) /3
slen=len(s) /number_of_partitions

''' partitioning[i] contains set of vertices  mapped to partition i'''
partitioning=[]

# for i in range(4):
for i in range(number_of_partitions):
    partitioning.append(0)

# for i in range(3):
for i in range(number_of_partitions-1):
    partitioning[i]=set(random.sample(s, slen)) # ith random subset
    s-=partitioning[i]

# print s

# print "=============="
partitioning[number_of_partitions-1]=s

for i in range(number_of_partitions):
    print partitioning[i]


#### create a reverse mapping
vertex_partition_map={}

for i in range(len(partitioning)):

    l=list(partitioning[i])
    for v in l:
        vertex_partition_map[v]=i

''' vertex_partition_map has key as vid while value is pid'''

print "========================vertex partition map================="
print vertex_partition_map
#find inter/intra communcation --- utilization ---makespan
print "============================Simulation Start====================================================="
############################Algorithm simulation#################################################################

#get  bound on SS
makespan=[]
internode_communication=[]
intranode_communication=[]
active_vm_list=[]
utilization=[]
superstep_time=[]

''' number of supersteps required'''
max_ss= 2* int(math.floor(n/2))

for k in range(0,max_ss+1):
    # l=[]
    internode_communication.append([])
    intranode_communication.append([])
    utilization.append([])
    active_vm_list.append(set())
    superstep_time.append([])

# print max_ss

# get current ss
for ss in range(0,max_ss+1):



    '''find the partition with maximum number of active vertices'''
    partition_active_vertex_map={} #TEMP map to store mappings of active vertices
    for i in range(number_of_partitions):
        partition_active_vertex_map[i]=0

    '''local variables to calulate intra/inter node communication'''
    intranode_comm=0
    internode_comm=0

    '''get active vertices -- distance_vertex_map'''

    active_vertex_list=distance_vertex_map[ss]
    # print active_vertex_list

    '''find intera and internode communication cost --- get neighbours adjList for each neighbour get partition vertex_partition_map'''
    for src in active_vertex_list:

        partition_active_vertex_map[vertex_partition_map[src]]=partition_active_vertex_map[vertex_partition_map[src]]+1

        vm_list=active_vm_list[ss]
        vm_list.add(vertex_partition_map[src])

        for dst in adjList[src]:
            if(vertex_partition_map[src]== vertex_partition_map[dst]):
                intranode_comm=intranode_comm+1
            else:
                internode_comm=internode_comm+1

    # print "ss "+str(ss)
    l1=internode_communication[ss]
    # print l1
    l1.append(internode_comm)
    # print "test2"+str(l1)
    # internode_communication[ss]=l1
    #
    l2=intranode_communication[ss]
    l2.append(intranode_comm)


    # print partition_active_vertex_map

    ''' superstep time'''

    ss_time= max(partition_active_vertex_map.values())

    # print ss_time

    ls=superstep_time[ss]
    ls.append(ss_time)

    '''utilization calculation'''

    total_time=ss_time*number_of_partitions
    active_time=len(active_vertex_list)

    util =(float) (active_time *100/(float (total_time)))

    lu=utilization[ss]
    lu.append(util)
    # superstep_time.append(max(x, key=partition_active_vertex_map.get))
    # intranode_communication[ss]=l2
    # print "#####################################"
    # print internode_communication

print "##############final result #######################"

print "internode_communication"
print internode_communication

print "intranode_communication"
print intranode_communication

print "SS time"
print superstep_time

print "utilization "
print utilization



print "active vm list"
print active_vm_list

# print superstep_time
#get active VM     vertex_partition_map
#get time required
















