import random
from igraph import *
import sys
import matplotlib.pyplot as plt
##############################graph formation ####################################

m=int(sys.argv[1])
n=int(sys.argv[1])

g = Graph.Lattice([m,m,m],directed=True, circular=False)


print g
# exit()

''' set(g.neighbours(vid)) has adjlist structure of graph
key : vid
value: set of neighbours'''

# print adjList
#################Visualization#############################
# layout = g.layout("grid")
# l=[]
# for i in range(0,m*n*m):
#    l.append(i)
#
# g.vs["name"]=l
# g.vs["label"] = g.vs["name"]
# plot(g, layout = layout)
#
# exit()
#############run bfs################
center=int(math.floor( m/2)*n*n+math.floor( m/2)*n+math.floor( m/2))

print "center is " +str(center)

# exit()
''' result[0][i] has distance for ith vertex from the source vertex'''
result=g.shortest_paths_dijkstra(source=center, target=None, weights=None, mode=OUT)

###form map containing distance as key and value as vid:
#print "distance for each vertex"
#print result[0]
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


number_of_partitions=int(sys.argv[2])
##########################Partitoning of the graph#######################################################
number_of_simulations=int(sys.argv[3])
s=set()
# for i in range(0,9,1):
for i in range(0,m*n*m,1):
    s.add(i)

# slen=len(s) /3
slen=len(s) /number_of_partitions

''' partitioning[i] contains set of vertices  mapped to partition i'''
partitioning=[]

# for i in range(4):
for i in range(number_of_partitions):
    partitioning.append(0)

# for i in range(3):
# for i in range(number_of_partitions-1):
#     partitioning[i]=set(random.sample(s, slen)) # ith random subset
#     s-=partitioning[i]
#
# # print s
#
# # print "=============="
# partitioning[number_of_partitions-1]=s
#
# for i in range(number_of_partitions):
#     print partitioning[i]
#
partitioning[0]=[0,9,18,]
partitioning[1]=[1,10,19]
partitioning[2]=[2,11,20]
partitioning[3]=[3,12,21]
partitioning[4]=[4,13,22]
partitioning[5]=[5,14,23]
partitioning[6]=[6,15,24]
partitioning[7]=[7,16,25]
partitioning[8]=[8,17,26]
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
max_ss= 3* int(math.floor(n/2))

print "max ss "+str(max_ss)
# exit()

for k in range(0,max_ss+1):
    # l=[]
    # internode_communication.append([])
    # intranode_communication.append([])
    # utilization.append([])
    active_vm_list.append(set())
    # superstep_time.append([])

current_makespan=0
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

        for dst in set(g.neighbors(src)):
            if(vertex_partition_map[src]== vertex_partition_map[dst]):
                intranode_comm=intranode_comm+1
            else:
                internode_comm=internode_comm+1

    # print "ss "+str(ss)
    # l1=internode_communication[ss]

    internode_communication.append(internode_comm)
    # print l1
    # l1.append(internode_comm)
    # print "test2"+str(l1)
    # internode_communication[ss]=l1
    #
    # l2=intranode_communication[ss]
    # l2.append(intranode_comm)
    intranode_communication.append(intranode_comm)

    # print partition_active_vertex_map

    ''' superstep time'''

    ss_time= max(partition_active_vertex_map.values())

    current_makespan=current_makespan+ss_time

    # print ss_time

    # ls=superstep_time[ss]
    # ls.append(ss_time)

    '''utilization calculation'''

    total_time=ss_time*number_of_partitions
    active_time=len(active_vertex_list)

    util =(float) (active_time *100/(float (total_time)))

    # lu=utilization[ss]
    # lu.append(util)
    utilization.append(util)
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


print current_makespan
# print superstep_time
#get active VM     vertex_partition_map
#get time required


parent_folder=sys.argv[4]

os.system("mkdir -p "+parent_folder)

font = {'family' : 'normal',
        'weight' : 'normal', #bold
        'size'   : 40}

plt.matplotlib.rc('font', **font)
####################plot utilization#####################


# plt.tick_params(axis='both', which='major', labelsize=14)
plt.grid()

plt.xlabel('Superstep')
plt.ylabel('Utilization%')
# plt.title('BFS with Flat partitioning')
axes = plt.gca()
# axes.set_xlim([xmin,xmax])
axes.set_ylim([0,100])
fig=plt.gcf()
fig.set_size_inches(15.5, 12.5)
plt.xticks([0,1,2,3],('0','1','2','3'))
plt.plot(utilization)
# plt.show()
plt.savefig(parent_folder+"/util.pdf")
plt.close()
####################plot internode#####################
fig=plt.gcf()
fig.set_size_inches(15.5, 12.5)


plt.xlabel('Superstep')
plt.ylabel('Internode Message Count')
# plt.title('Internode Communication for BFS with FP')
plt.grid()
axes = plt.gca()
# axes.set_xlim([xmin,xmax])
axes.set_ylim([0,35])
plt.xticks([0,1,2,3],('0','1','2','3'))
plt.plot(internode_communication)
plt.savefig(parent_folder+"/InterNode.pdf")
plt.close()
# #
# # ####################plot intranode#####################

fig=plt.gcf()
fig.set_size_inches(15.5, 12.5)

plt.grid()
plt.xlabel('Superstep')
plt.ylabel('Intranode Message Count')
plt.xticks([0,1,2,3],('0','1','2','3'))
plt.plot(intranode_communication)
plt.savefig(parent_folder+"/intra.pdf")















