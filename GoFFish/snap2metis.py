import sys
import os

'''
input : snap file

arglist:

1.metis edge list
2.input for metis

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
metis_graph=sys.argv[3]
giraph_graph=sys.argv[4]


snapfile = open(snap_file, 'r')
metis_edgeListfile = open(metis_edgeList, 'w')

reordering = dict()
rReordering = dict()
vid = 1
count=0

graph={}


for line in snapfile:
    # print line[:-1]
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


metis_graphfile = open(metis_graph, 'w')
giraph_graphfile = open(giraph_graph, 'w')

numV=len(graph.keys())
numE=count

metis_graphfile.write(str(numV)+" "+str(numE)+"\n")

for i in range(1,numV+1):

    metis_graphfile.write( " ".join( str(v) for v in list(graph[i])) + "\n")
    # giraph_graphfile.write(str(i)+" "+" ".join( str(v) for v in list(graph[i])) + "\n")
    outstr=str(i)+"\t"+str(0.0)
    prefix="\t"
    for v in list(graph[i]):
        outstr=outstr+prefix+str(v)+prefix+str(1.0)
    giraph_graphfile.write(outstr+"\n")

metis_graphfile.close()
giraph_graphfile.close()