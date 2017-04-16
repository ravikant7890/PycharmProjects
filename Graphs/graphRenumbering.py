import sys
import os

'''
input : snap file
Assuming that input graph is undirected
arglist:

1.metis edge list
2.output filename for metis

output :

1. metis format

2. edge list

3. giraph_file

'''

# fout = open('hello.txt', 'w')
# fout.write('Hello, world!\n')                # .write(str)
# fout.write('My name is Homer.\n')
# fout.write("What a beautiful day we're having.\n")
# fout.close()
#


snap_file=sys.argv[1]
metis_edgeList=sys.argv[2]
# metis_graph=sys.argv[3]
# giraph_graph=sys.argv[4]


snapfile = open(snap_file, 'r')
metis_edgeListfile = open(metis_edgeList, 'w')

reordering = dict()
rReordering = dict()
vid = 1
count=0

graph={}


for line in snapfile:
    print line[:-1]
    src= line[:-1].split()[0]
    dst= line[:-1].split()[1]

    if(rReordering.has_key(src)):
        pass
    else:
        reordering[vid] = src
        rReordering[src] = vid
        vid=vid+1


    if(rReordering.has_key(dst)):
        pass
    else:
        reordering[vid] = dst
        rReordering[dst] = vid
        vid=vid+1

    # graph formation

    if(graph.has_key(rReordering[src])):
        n=graph[rReordering[src]]
        n.add(rReordering[dst])
        graph[rReordering[src]]=n

    else:
        n = set()
        n.add(rReordering[dst])
        graph[rReordering[src]]=n




    count=count+1

    # print rReordering[src],rReordering[dst]
    outString=str(rReordering[src]-1)+" "+str(rReordering[dst]-1)
    # print outString
    metis_edgeListfile.write(outString+"\n")

# print count
# print rReordering
# print graph
snapfile.close()
metis_edgeListfile.close()
