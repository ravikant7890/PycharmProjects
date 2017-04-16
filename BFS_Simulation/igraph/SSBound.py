import os
import sys
import igraph
from igraph import *
import matplotlib.pyplot as plt
import pickle
import random
import itertools
from operator import mul


#form a  metagraph


#/home/ravikant/LogFiles/Europar/Metagraphs/Metagraph-ORKT-5M-40P-FV-null-2016-02-14-12\:37\:23/MetagraphEdgeList-ORKT-5M-40P-FV.txt
filename=sys.argv[1]

# /home/ravikant/LogFiles/Europar/Metagraphs/Metagraph-ORKT-5M-40P-FV-null-2016-02-14-12\:37\:23/
os.chdir(sys.argv[2])

# LoadedGraph = Graph.Read_Ncol( edgelist,directed=True)

g = igraph.read(filename, format="ncol", directed=False, names=True)


# from igraph import *

# print g.vs

#get the b_2_b distributions:

meta_dict={}

vertex_list=[]

for v in g.vs:

    f= "b2b_"+v['name']+".txt"

    key=v['name']

    vertex_list.append(int(key))

    with open(f, 'rb') as handle:
        b = pickle.loads(handle.read())

        handle.close()

        factor=1.0/sum(b.itervalues())
        for k in b:
            b[k] = b[k]*factor
            # b[k] = round(b[k]*factor,2)

        meta_dict[key]=b

    print key+ " "+str(meta_dict[key])

print "================================================================"
#### iterate till diameter of the graph

diameter=int(sys.argv[3])

#randomly select source vertex
src=random.choice(vertex_list)


neis = g.neighbors(str(src), mode="out")

# print len(set(g.vs[neis]["name"]))
print "================================================================"
print src
print "================================================================"

#################################determine active set################################
active_set_metalist=[]

active_list_ss0=[src]

active_set_metalist.append(active_list_ss0)

for i in range(1,int(diameter)+1):

    active_set=set()

    active_set_prev_ss=active_set_metalist[i-1]

    for v in active_set_prev_ss:

        neis = g.neighbors(str(v), mode="out")

        for adj in g.vs[neis]["name"]:

            active_set.add(adj)

    # print active_set

    # print len(active_set)

    active_set_metalist.append(list(active_set))


print "================================================================"
# for i in active_set_metalist:
#     print i
print "================================================================"
    # print len(i)

##################################################################################################
#####################find all combinations for length #######################


#for each superstep form all combinations of path length selection & probability


meta_path_permutations=[]

meta_prob_permutations=[]

# for ss in range(0,int(diameter)+1):
for ss in range(1,5):

    path_permutations=[]

    path_permutations_max=[]

    prob_permutations=[]

    prob_permutations_prod=[]

    active_set=active_set_metalist[ss]

    # print active_set
    # get active set

    for v in active_set:

        path=[]
        prob=[]

        for k in meta_dict[str(v)].keys():

            if(k < 10000): #for avoiding infinity value

                path.append(k)
                prob.append(meta_dict[str(v)][k])

        path_permutations.append(path)
        prob_permutations.append(prob)

        # print meta_dict[str(v)].keys()

    # print path_permutations
    # print prob_permutations
    print "================================================================"
    # print (list(itertools.product(*path_permutations)))

    # for t in (list(itertools.product(*path_permutations))):
    for t in ((itertools.product(*path_permutations))):

        path_permutations_max.append(max(t))


    # for t in (list(itertools.product(*prob_permutations))):

    for t in ((itertools.product(*prob_permutations))):

        prob_permutations_prod.append(reduce(mul,t))



    meta_path_permutations.append(path_permutations_max)
    meta_path_permutations.append([1])
    meta_prob_permutations.append(prob_permutations_prod)
    meta_prob_permutations.append([1])

    print len(prob_permutations_prod)
    print "================================================================"
    # for l in list(itertools.product(*path_permutations)):
    #
    #     for t in l:
    #
    #         print t



meta_path_permutations.pop()
meta_prob_permutations.pop()
# print len(meta_prob_permutations)

# print meta_path_permutations

print "########################### find out all valid permutations with supersteps equal diameter of metagraph till diameter# of the graph################################################"


ssbound_map={}

diameter_of_metagraph=int(sys.argv[4])


n=diameter_of_metagraph+diameter_of_metagraph+1

for i in range(n,len(meta_path_permutations),2):

    step_count=int(i/2)

    print "step count "+str(step_count)


    # for j in (list(itertools.product(*meta_path_permutations[:i]))):
    for j in ((itertools.product(*meta_path_permutations[:i]))):

        # print type(j)
        # print j
        # print sum(j)

        if( sum(j)== diameter):

            print j

            if(ssbound_map.has_key(step_count)):

                count=ssbound_map[step_count]

                ssbound_map[step_count]=count+1

            else:

                ssbound_map[step_count]=1


print ssbound_map

    # exit()



















#####################################################################################



# Graph.neighbors()


# print g

#
# layout = g.layout("kamada_kawai")
#
# igraph.plot(g, layout = layout)
# plt.show()
#
#cound the superstep:


#for loop over length of diameter
