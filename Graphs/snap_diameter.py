import snap
import sys

G5 = snap.LoadEdgeList(snap.PNGraph, sys.argv[1], 0, 1,'\t')

count =0
for v in G5.Nodes():
    count=count+1

print count

diam = snap.GetBfsFullDiam(G5, 100)


WccG = snap.GetMxWcc(G5)

print WccG

print diam


# d=GetBfsEffDiam(G5,10,1,)