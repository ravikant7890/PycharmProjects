import snap
import sys
import matplotlib.pyplot as plt
import os
import subprocess
import random

from itertools import groupby as g
def most_common_oneliner(L):
  return max(g(sorted(L)), key=lambda(x, v):(len(list(v)),-L.index(x)))[0]

##### get the list of sgids

parent_dir=sys.argv[1]

os.chdir(parent_dir)


sglist_command="grep TOPO.SG partitionnode* |awk -F\",\" '{print $9}' "


sglist=[]

for subgraph in os.popen(sglist_command).read().split("\n"):
    if subgraph:
        sglist.append(subgraph)

#
#
# print len(sglist)

# sglist=[34359738409,137438953475]
###### get the edgelist for each subgraph
#
for subgraph in sglist:

    filename="EDGELIST"+str(subgraph)+".txt"

    print subgraph

    edgelist_command="grep -w \"LOCALEDGE\" SG"+str(subgraph)+".txt | awk -F\",\" '{print $4,$5}' OFS=\"\t\"  > "+filename

    os.system(edgelist_command)

    # break
    # exit()
# exit()


for subgraph in sglist:



    edgelist="EDGELIST"+str(subgraph)+".txt"

    LoadedGraph = snap.LoadEdgeList(snap.PNGraph, edgelist, 0, 1, '\t')


    subgraph_file="SG"+str(subgraph)+".txt"

    print " processing "+str(subgraph_file)

# LoadedGraph.Dump()

    boundaryV=[]

    f=open(subgraph_file,'r')

    for line in f:

        if ',BOUNDARYVERTEX,' in line:

            # print line

            b=line[:-1].split(',')

            for i in range(3,len(b)):

                boundaryV.append(b[i])


    f.close()

    print len(boundaryV)

    # print boundaryV


    command= "grep TOPO.SG partitionnode*| grep -w "+str(subgraph)

    result = subprocess.check_output(command, shell=True)

    # numRV=result[:-1].split(',')[14]

    numV=int(result[:-1].split(',')[10])-int(result[:-1].split(',')[14])

    # print result
    #
    # print numRV
    #
    # print numV

    if(numV==1):
        average_path_length=0

    elif(len(boundaryV)==1):

        average_path_length=snap.GetBfsFullDiam(LoadedGraph, numV)

    elif(len(boundaryV) <= 5) : ##

        distance=[]

        for src  in range(0,len(boundaryV)-1,1):

            for target in range(src+1,len(boundaryV),1):

                # print "src "+str(boundaryV[src])+" target "+str(boundaryV[target])

                if(src!=target):

                    try:
                        Length = snap.GetShortPath(LoadedGraph,int(boundaryV[src]), int(boundaryV[target]))

                        print Length
                        if(Length!=-1):

                            distance.append(Length)

                    except:
                        pass


        try:
            average_path_length=most_common_oneliner(distance)
        except:
            average_path_length=0

    else:#########sample boundary vertices

        rand_smpl = [ boundaryV[i] for i in (random.sample(xrange(len(boundaryV)), 5)) ]

        print rand_smpl

        distance=[]

        for src  in range(0,len(rand_smpl)-1,1):

            for target in range(src+1,len(rand_smpl),1):


                # print "src "+str(src)+" target "+str(target)

                if(src!=target):

                    try:
                        Length = snap.GetShortPath(LoadedGraph, int(rand_smpl[src]), int(rand_smpl[target]))
                    except:
                        pass
                    # print "lenght "+str(Length)

                    if(Length!=-1):

                        distance.append(Length)

        print "distances calculated"
        print len(distance)

        try:
            average_path_length=most_common_oneliner(distance)
        except:
            average_path_length=0


    print "writing distance"

    f=open('B2BAVGPath.txt','a')

    f.write(str(subgraph)+","+str(average_path_length)+"\n")

    f.close()


    # exit()



















    # exit()




    # print len(LoadedGraph.Nodes())


    # diam = snap.GetBfsFullDiam(LoadedGraph, 1000)

    # print "diameter "+str(diam)

# exit()

    #
    # b2b_path_length=[]
    #
    # # print boundaryV
    # print boundaryV[0]
    #
    # print boundaryV[1]
    #
    # Length = snap.GetShortPath(LoadedGraph, int(boundaryV[0]), int(boundaryV[1]))
    # #
    #
    # print "Shortest Path from node 1 to node 100 is %d edges" % Length
    #
    # # exit()
    #
    #
    # for b in boundaryV:
    #     # print b+","+str(nx.eccentricity(G,v=b))
    #
    #     for target in boundaryV:
    #
    #         if(b!=target):
    #             try:
    #
    #                 # print "src "+b+" dst "+target
    #
    #                 Length = snap.GetShortPath(LoadedGraph, int(b), int(target))
    #                 #
    #
    #                 print "Shortest Path from node 1 to node 100 is %d edges" % Length
    #                 # print Le
    #
    #                 # exit()
    #                 b2b_path_length.append(len(p))
    #
    #             except:
    #
    #                 pass
    #
    #
    # # print boundaryV
    # average_path_length=most_common_oneliner(b2b_path_length)-1
    #
    # print average_path_length