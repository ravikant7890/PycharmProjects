__author__ = 'ravikant'

import  sys
import networkx as nx
import subprocess

###command to run python Source2Blength.py EDGELIST133143986176-trimmed.txt  133143986176 27  BOUNDARYVERTEX.txt out.txt

orkt_metaVID=[30064771072,4294967296,25769803776,68719476736,64424509440,73014444032,77309411328,81604378624,17179869184,171798691840,90194313216,60129542144,94489280512,146028888064,98784247808,103079215104,107374182400,111669149696,115964116992,150323855360,120259084288,124554051584,85899345920,128849018880,133143986176,137438953472,141733920768,8589934592,12884901888,154618822656,21474836480,158913789952,163208757248,167503724544,34359738368,38654705664,42949672960,47244640256,51539607552,55834574848]

edgeList=sys.argv[1]

metaVID=sys.argv[2]

src_id=sys.argv[3]


#get the pid from subgraph.log file
# src_pid=sys.argv[3]

#/scratch/RavikantLOGS/Metagraph/EdgeCount-ORKT-5M-40P-FV-NULL-2016-08-14-11:26:38/BOUNDARYVERTEX.txt
bv_list_file=sys.argv[4]

out_file=sys.argv[5]

bvlist=[]

G = nx.read_edgelist(sys.argv[1], nodetype=int,create_using=nx.DiGraph())

# print G.neighbors(27)

# print G.nodes()


# print nx.single_source_shortest_path_length(G, 928)
distance_dict= nx.single_source_shortest_path_length(G, int(src_id))
#get bvlist

# print distance_dict

# exit()

grep_command=" grep "+metaVID+" "+bv_list_file

result = subprocess.check_output(grep_command ,shell=True)


f = open(out_file,'w')

for v in result.split(",")[3:]:
    # print v
    try:
        d=distance_dict[int(v)]

        f.write(str(d)+'\n')

    except:
        continue

f.close()




# print distance_dict[2883486]
#
# print distance_dict[917300]

#
# f = open(out_file,'w')
#
#
# for i in bvlist:
#
#     #write this distance to a file
#     d=distance_dict[int(i)]
#
#     f.write(str(d)+'\n')
#
# f.close()