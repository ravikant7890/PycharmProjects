import sys
import os
import subprocess
import networkx as nx

'''
Arguments:
1. Parent directory where all log folders of 1000 runs are stored

e.g. /home/ravikant/LogFiles/Modelling/LIVJBFS/

2 . Directory with edgeList for each subgraph + boundary vertex information

e.g. /scratch/RavikantLOGS/Metagraph/EdgeCount-LIVJ-5M-40P-F-NULL-2016-08-13-21:44:23

EdgeList file format  : EDGELIST163208757272.txt

Boundary vertex information : SG133143986590.txt


'''
#get a map of subgraph and source v ids.as
#############################################################

parent_folder=sys.argv[1]

subgraph_info_folder=sys.argv[2]

#############################################################

sg_to_src_map={}  #subgraph to source mapping

sg_partition_map={}

sg_bv_map={} #subgraph to boundary vertex map

##############################################

## form a maapping between src and subgraph

cmd="ls -1 "+parent_folder

out_dir_list=[]

for out_dir in os.popen(cmd).read().split("\n"):
    if out_dir:
        out_dir_list.append(out_dir)


print len(out_dir_list)

count=0

for folder in out_dir_list:

    count+=1

    os.chdir(parent_folder+"/"+folder)

    # os.system("pwd")
    getSource_command= " grep \"TESTSRC\" containernode* "

    result=subprocess.check_output(getSource_command,shell=True)

    splitResult=result[:-1].split("-")

    vid=int(splitResult[1])

    sgid=int(splitResult[3])

    pid=int(splitResult[5])

    if sgid in sg_to_src_map.keys():

        l= sg_to_src_map[sgid]

        l.append(vid)
    else:
        l=[]
        l.append(vid)
        sg_to_src_map[sgid]=l

    sg_partition_map[sgid]=pid

    if ( (count%50)==0) :
        print count
    # print result[:-1]
    #
    # print vid,sgid,pid


print len(sg_partition_map.keys())

for sg in sg_partition_map.keys():

    print sg,len(sg_to_src_map[sg])

############ for each subgraph in the sg to pid mapping get the list of boundary vertices:

#how to get list boundary vertices?
for sg in sg_partition_map.keys():

    filename="SG"+str(sg)+".txt"

    file_path=subgraph_info_folder+"/"+filename

    pid=sg_partition_map[sg]

    get_bv_cmd="grep \""+str(sg)+","+str(pid)+" BOUNDARYVERTEX\""

    result=subprocess.check_output(get_bv_cmd,shell=True)

    splitResult=result[:-1].split(",")[3:]

    ###get the list of boundary vertices sg,pid,boundaryVertex,------
    ##getr it as a list of integers

    sg_bv_map[sg]=splitResult

##### form a graph from edge list and get the distance distribution from each source vertex

    edgelist_filename="EDGELIST"+str(sg)+".txt"

    edgelist_file_path=subgraph_info_folder+"/"+filename

    G = nx.read_edgelist(edgelist_file_path, nodetype=int, data=(('weight',float),),create_using=nx.DiGraph())

    ##for each src id in the subgraph get the single source shortest path and get distance for each boundary bvertex

    for source in sg_to_src_map[sg]:

        nx.single_source_shortest_path_length(G, source)

        #get distances for all boub=ndary vertices












### for each subgraph , for each source vertex get path length distribution

exit()



