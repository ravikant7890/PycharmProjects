from igraph import *
import sys
import matplotlib.pyplot as plt
import pickle
import networkx as nx

# A=[1,2,3]
# B=[4,5,6]
# C=[7,8,9]
#
# a=[[1,2,3],[4,5,6],[9,9,9]]
#
# print a[:2]
#
# import itertools
# from operator import mul
# #
# # l=[]
# for t in (itertools.product(*a)):
#
#     print t
#     print type(t)
#     print sum(t)
#
# #     # print type(t)
# #
# #     # print t
# #     reduce(mul,t)
# #     l.append(reduce(mul,t))
# #
# #
# # print l
#
# # print list(itertools.product(*a))
# # print len(list(itertools.product(*a)))
#     # print str(max(t))
#

# G=nx.complete_graph(100)

G=nx.fast_gnp_random_graph(100,0.2)

print G.adjacency_list()

nx.write_adjlist(G,"adjlist.txt")

nx.write_edgelist(G, "test.edgelist.txt", data=False)