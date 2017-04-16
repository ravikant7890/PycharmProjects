import os
import subprocess
from igraph import *
import random
from collections import Counter
import pickle


parent_dir=sys.argv[1]

os.chdir(parent_dir)


sglist_command="grep TOPO.SG partitionnode* |awk -F\",\" '{print $9}' "


sglist=[]
#
for subgraph in os.popen(sglist_command).read().split("\n"):
    if subgraph:
        sglist.append(subgraph)

#
#
print len(sglist)


# exit()
# sglist=[34359738409,137438953475]
###### get the edgelist for each subgraph
#
for subgraph in sglist:

    filename="EDGELIST"+str(subgraph)+".txt"

    print subgraph

    edgelist_command="grep -w \"LOCALEDGE\" SG"+str(subgraph)+".txt | awk -F\",\" '{print $4,$5}' OFS=\"\t\"  > "+filename

    os.system(edgelist_command)



for subgraph in sglist:



    edgelist="EDGELIST"+str(subgraph)+".txt"

    # LoadedGraph = snap.LoadEdgeList(snap.PNGraph, edgelist, 0, 1, '\t')
    LoadedGraph = Graph.Read_Ncol( edgelist,directed=True)

    print LoadedGraph


    subgraph_file="SG"+str(subgraph)+".txt"

    print " processing "+str(subgraph_file)

# LoadedGraph.Dump()

    boundary=[]

    f=open(subgraph_file,'r')

    for line in f:

        if ',BOUNDARYVERTEX,' in line:

            # print line

            b=line[:-1].split(',')

            for i in range(3,len(b)):

                boundary.append(b[i])


    f.close()

    print len(boundary)

    # print boundaryV

    # exit()

    command= "grep TOPO.SG partitionnode*| grep -w "+str(subgraph)

    result = subprocess.check_output(command, shell=True)

    # numRV=result[:-1].split(',')[14]

    numV=int(result[:-1].split(',')[10])-int(result[:-1].split(',')[14])


    boundaryV=[]

    if(numV==1):
        pass

        # average_path_length=0


        # average_path_length=snap.GetBfsFullDiam(LoadedGraph, numV)

    elif(len(boundary) <= 2) :

        for b in boundary:
          boundaryV.append(b)

    else:
        boundaryV = [ boundary[i] for i in (random.sample(xrange(len(boundary)), 50)) ]

    distance=[]

    distribution=Counter()

    for src  in boundaryV:

        # print "source "+str(src)

        result=LoadedGraph.shortest_paths_dijkstra(source=src, target=None, weights=None, mode=OUT)

        # print Counter(result[0])
        distribution= distribution+Counter(result[0])

    # print "================================="
    print distribution

    filename="b2b_"+str(subgraph)+".txt"

    factor=1.0/sum(dict(distribution).itervalues())

    for k in dict(distribution):
        dict(distribution)[k] = dict(distribution)[k]*factor


    with open(filename, 'wb') as handle:
         pickle.dump(dict(distribution), handle)
    handle.close()
