import snap
import sys
# Graph = snap.GenRndGnm(snap.PNGraph, 100, 1000)

G5 = snap.LoadEdgeList(snap.PNGraph, sys.argv[1], 0, 1)

snap.PlotOutDegDistr(G5,sys.argv[2], "Directed graph - out-degree Distribution")