import sys
import numpy as np
import networkx as nx
import pickle
import random
'''
Argument

1. Graph file in the form SGID<space>SGID<space>MetaEdgeWeight
path : /home/ravikant/LogFiles/Europar/Metagraphs/Metagraph-ORKT-5M-40P-FV-null-2016-02-14-12:37:23/MetagraphEdgeList-ORKT-5M-40P-FV.txt

2. boundaryV count file
format : subgraph.getId()+","+partition.getId()+","+boundaryV.size()+","+remoteE.size()
path:/scratch/RavikantLOGS/Metagraph/BoundaryVertexCount-ORKT-5M-40P-FV-NULL-2016-09-05-13:31:53/BVCOUNT.txt

3. Folder where pickle formaated b2b path length distribution file are kept
file name format : "b2b_"+MetaVertexID+".txt"
path(/ at end ) : /home/ravikant/PycharmProjects/BFSSImulation/b2bPathLengthDistribution

4. file containing length of shortest paths from source to boundary vertices in source subgraph
#can be created using Source2Blength.py

5. ID of source metaVertex

#edgelist of all subgraphs is present in
# /scratch/RavikantLOGS/Metagraph/EdgeCount-ORKT-5M-40P-FV-NULL-2016-08-14-11:26:38

example:
python BFSSimulationOnBV.py
/home/ravikant/LogFiles/Europar/Metagraphs/Metagraph-ORKT-5M-40P-FV-null-2016-02-14-12\:37\:23/MetagraphEdgeList-ORKT-5M-40P-FV.txt
BVCOUNT.txt
/home/ravikant/PycharmProjects/BFS_Simulation/Networkx/b2bPathLengthDistribution/
out.txt
133143986176

'''
############# intial setup ######################################################
#########form metagraph --- need only weight of metaedge

# read file in the form SGID<space>SGID<space>MetaEdgeWeight

G = nx.read_edgelist(sys.argv[1], nodetype=int, data=(('weight',float),),create_using=nx.DiGraph())

boundaryV_count_file=sys.argv[2]

b2b_pathlengthd_parent_folder=sys.argv[3]

s2b_pathlength_file=sys.argv[4]

src=int(sys.argv[5])



print len(G.nodes())

# for i in G.nodes():
#
#     print i

# exit()
# print len(G.edges())

#to calculate shortest path from source to all boundary vertices
# print nx.single_source_shortest_path_length(G, 8589934592)



############## for each metavertesx initialize a list of length equal to number of boundary vertices

BVdistance={} #key is sgID and value is list of boundary vertices with distance

MsgContainer={} # key is sgID and value is list of list .. each list represent messages from one neighbour

bvCount={}

with open(boundaryV_count_file, "r") as f:

    for line in f:

        if line:

            parts=line.split(',')

            bvCount[int(parts[0])]=int(parts[2])

            BVdistance[int(parts[0])]   = [sys.maxint] * int(parts[2])

            MsgContainer[int(parts[0])]=[]#for each subgraph msg container has list
            #to send a message to subgraph 'S', others will append a list of values to this above list

#to initialize use something like [0] * 10

# print B2barray


###load all b2b distance distributions
b2b_dist={}

for v in G.nodes():


    f= "b2b_"+str(v)+".txt"

    key=v

    f=b2b_pathlengthd_parent_folder+f

    # print f

    with open(f, 'rb') as handle:
        b = pickle.loads(handle.read())

        handle.close()

        factor=1.0/sum(b.itervalues())
        for k in b:
            b[k] = b[k]*factor
            # b[k] = round(b[k]*factor,2)

        b2b_dist[key]=b

    # print str(key)+ " "+str(b2b_dist[key])

############################SStep 0############################################

#initialize the distance of boundary vertices in source subgraph

#read s2b_pathlength_file and update the BVdistance of src

f=open(s2b_pathlength_file,'r')

BVdistance_src_array=BVdistance[int(src)]

i=0
for l in f:

    if l:

        BVdistance_src_array[i]=int(l[:-1])
        i=i+1

# print BVdistance[int(src)]
#TODO: some vertices are unreachable : how to handle?

#send messages to neighbours based on edge weights

ssCount=0

for n in G.neighbors(int(src)):

    #get edgeweight
    msg_count=int( G[int(src)][n]['weight'])

    # print msg_count

    msg_list=[]

    for k in range(msg_count):

        #pick random value from
        msg_list.append(random.choice(BVdistance[int(src)])+1)#1 is the edge weight

    # print n,len(msg_list)
    #send as many msg as edgeweight
    #append it to msg container
    l= MsgContainer[n]
    l.append(list(msg_list))

ssCount=ssCount+1

#########verification of message passing
# for n in MsgContainer.keys():
#
#     print len(MsgContainer[n])
#
#     if(len(MsgContainer[n])>0):
#         print n,len(MsgContainer[n][0])

####################################### END SS1 #######################################
##################from ss1 #############

#read message and delete it from queue

#for each active metaVetex

    #read the messages from MsgContainer

        #for each message list

            #for each vertex update the distance


#compute the fraction of updated vertices

#for each neighbour put the message list in container

#TODO: Maintain two containers send & recv


while(1):

    sendMsgContainer={}

    for metav in G.nodes():
        l=[]
        sendMsgContainer[metav]=list(l)

    print sendMsgContainer


    print "IN superstep " +str(ssCount)
    for sg in MsgContainer.keys():

        update_count=0

        updated_index=[]
        #if there is incoming message
        if(len(MsgContainer[sg])>0):

            for received_msg_list in MsgContainer[sg]:


                #randomly select k vertices from sg & see if there distance can be updated
                BVdistance_list_sg=BVdistance[int(sg)]

                for k in range(len(received_msg_list)):

                    index=random.choice(range(len(BVdistance_list_sg)))

                    if(BVdistance_list_sg[index] > received_msg_list[k] ):

                        update_count=update_count+1

                        updated_index.append(index)

                        BVdistance_list_sg[index] = received_msg_list[k]

                #delete the processed message list
                MsgContainer[sg].remove(received_msg_list)

            if(update_count >0):

                b2b_dist_sg=b2b_dist[sg]

                # print b2b_dist_sg

                key_length=len(b2b_dist_sg.keys())

                probability_values=[]

                for p in range(key_length):

                    try:
                        probability_values.append(b2b_dist_sg[p])
                    except:
                        key_length=key_length-1
                        continue
                # print b2b_dist_sg
                # print probability_values

                # exit()
                BVdistance_list_sg=BVdistance[int(sg)]
                #for each vertex see if distance can be updated
                for i in range(len(BVdistance_list_sg)):

                    choice=random.choice(updated_index)

                    #randomly select value from b2b path length distribution
                    #TODO:pick random updated vertex and distance from distribution
                    #TODO np.random.choice(np.arange(1, 7), p=[0.1, 0.05, 0.05, 0.2, 0.4, 0.2])
                    distance=np.random.choice(np.arange(key_length), p=probability_values)


                    if(BVdistance_list_sg[i] > BVdistance_list_sg[choice]+distance ):

                        update_count=update_count+1
                        BVdistance_list_sg[i] = BVdistance_list_sg[choice]+distance

                # send update_count/bvCount[sg]*remote edges to all neighbours
                for neighbour in G.neighbors(sg):
                    msg_to_send= (update_count/(float(bvCount[sg]))) *G[sg][neighbour]['weight']

                    send_list=[]
                    for k in range(int(msg_to_send)):

                        #pick random value from
                        send_list.append(random.choice(BVdistance[sg])+1)#1 is the edge weight

                    l=sendMsgContainer [neighbour]
                    l.append(list(send_list))











                ##process the message





    #Check if is anyone has message recived if no break
    ssCount += 1
    flag=False

    # print MsgContainer

    MsgContainer=sendMsgContainer

    sendMsgContainer.clear()

    for n in MsgContainer.keys():

        # print len(MsgContainer[n])

        if(len(MsgContainer[n])>0):
            flag=True
            break

    if(flag):
        continue
    else:
        print "all messages consumend"
        break







