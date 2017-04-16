import networkx as nx
import matplotlib.pyplot as plt
import sys
import os
import subprocess


from itertools import groupby as g
def most_common_oneliner(L):
  return max(g(sorted(L)), key=lambda(x, v):(len(list(v)),-L.index(x)))[0]

parent_folder=sys.argv[1]

os.chdir(parent_folder)

cmd="ls -1 SG*"

out_dir_list=[]
for out_dir in os.popen(cmd).read().split("\n"):
    if out_dir:
        out_dir_list.append(out_dir)

###################### Precompute stats for each metaVertex ###############
#ID
#numv
#numlocaledges
#numRemoteV
#numRemoteE
#boundaryVCount
#b_2_b_avg_path
#diameter
#radius
# avg_clu_coeff

header="#ID,#numv,#numlocaledges,#numRemoteV,#numRemoteE,#boundaryVCount,#b_2_b_avg_path"
       # "#diameter,#radius,# avg_clu_coeff,"

f = open('METAVAnalysis','w')

f.write(header+'\n')

f.close()

######Form metagraph

for sg in out_dir_list:

    G=nx.Graph()

    id=sg[2:-4]


    print "=============================================SGID :"+id

    boundaryV=[]

    localedgeCount=0

    remoteedgeCount=0


    f=open(sg,'r')

    for line in f:

        if line:

            if ',LOCALEDGE,' in line:

                # print line


                src= line[:-1].split(",")[3]

                # src_pid=line.split(",")[1]

                G.add_node(src)

                dst= line[:-1].split(",")[4]

                # dst_pid=line.split(",")[4]

                G.add_node(dst)

                G.add_edge(src,dst)



            if ',BOUNDARYVERTEX,' in line:

                b=line[:-1].split(',')

                for i in range(3,len(b)):

                    boundaryV.append(b[i])

            if ',COUNTREMOTEEDGE,' in line:

                remoteedgeCount=line[:-1].split(',')[3]

            if 'COUNTLOCALEDGE' in line:

                localedgeCount=line[:-1].split(',')[3]

    # print boundaryV

    f.close()

    if len(boundaryV)==0:
        continue

    average_path_length=0 #b2b path

    print len(boundaryV)

    if(len(boundaryV)==1):

        # print boundaryV

        average_path_length= nx.eccentricity(G, v=boundaryV[0])

        # print average_path_length

    else:

        b2b_path_length=[]

        # print boundaryV

        for b in boundaryV:

            p= nx.eccentricity(G, v=b)

            print p

            try:

                b2b_path_length.append(p)

            except:
                pass
            # print b+","+str(nx.eccentricity(G,v=b))

            # for target in boundaryV:
            #
            #     if(b!=target):
            #         try:
            #             p=nx.shortest_path(G,source=b,target=target)
            #             #
            #             # print "src "+b+" dst "+target
            #             # print p
            #
            #             b2b_path_length.append(len(p))
            #
            #         except:
            #
            #             pass
            #

        # print boundaryV
        average_path_length=most_common_oneliner(b2b_path_length)-1

        # print average_path_length




    # print average_path_length
    # if(G.number_of_nodes() > 1):
    #     diameter=nx.diameter(G)
    #
    #     radius=nx.radius(G)
    #
    #     average_clustering_coefficient=nx.average_clustering(G)
    #
    # else:
    #     diameter=0
    #
    #     radius=0
    #
    #     average_clustering_coefficient=0


    command= "grep TOPO.SG partitionnode*| grep -w "+id

    result = subprocess.check_output(command, shell=True)


    # print result


    numRV=result[:-1].split(',')[14]

    # print numRV

    print "SGID "+id
    #
    # print G.nodes()
    #
    # print G.edges()
    #
    # print G.number_of_nodes()
    #
    # print G.number_of_edges()
    #
    # print localedgeCount


#ID
#numv
#numlocaledges
#numRemoteV
#numRemoteE
#boundaryVCount
#b_2_b_avg_path
#diameter
#radius
# avg_clu_coeff


    f = open('METAVAnalysis','a')
    #
    #
    # header="#ID,#numv,#numlocaledges,#numRemoteV,#numRemoteE,#boundaryVCount,#b_2_b_avg_path,#diameter,#radius,# avg_clu_coeff,"
    f.write(id+","+str(G.number_of_nodes())+","+str(G.number_of_edges())

            +","+str(numRV)+","+str(remoteedgeCount)

            +","+str(len(boundaryV))+","+str(average_path_length)

            # +","+str(diameter)+","+str(radius)+","+str(average_clustering_coefficient)

            +"\n"

            ) # python will convert \n to os.linesep
    #
    f.close()
