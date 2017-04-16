# ID,#numv,#numlocaledges,#numRemoteV,#numRemoteE,#boundaryVCount,#b_2_b_avg_path,#diameter,#radius,# avg_clu_coeff,

import os
import random

# mylist=[10,528,415,7,654,656,6562,741,6963,471,2235,71]
#
# rand_smpl = [ mylist[i] for i in sorted(random.sample(xrange(len(mylist)), 4)) ]
#
# print rand_smpl

#
# l=[[10,528,415,7,654,656,6562,741,6963,471,2235,71],[2,5,6,8,2,6,2],[4,6,7,7]]
#
#
# t=l[0]
#
# l.remove(t)
#
# print l


t1={}

t1[1]=3
t1[4]=9


t2={}

t2[1]=10
t2[4]=19


temp=t2

t2=t1

t1=temp


t2[12]=4
t1.clear()

print t1

print t2

p=10

for i in range(p):
    print i
    try:
        i=(i/0)
        print i
    except:

        p=p-1








