import matplotlib.pyplot as plt
import pandas as pd
import sys
import os
import csv

#
# df=pd.read_csv(sys.argv[1],header=None
#                ,names = ["Superstep", "PID", "SGID", "Time"])
#
#
# print df.head()
#
# print len(df)

active_ss_partition_map={}

f = open(sys.argv[1])

csv_f = csv.reader(f)
for row in csv_f:
    # print row
    # print row[2]

    ss=int(row[0])
    pid=int(row[1])
    t=int(row[3])

    if(t >0):

        if(ss in active_ss_partition_map.keys()):

            l=active_ss_partition_map[ss]
            l.add(pid)
            active_ss_partition_map[ss]=l
        else:

            l=set()
            l.add(pid)
            active_ss_partition_map[ss]=l




# print active_ss_partition_map

ss_active_count={}

for k in active_ss_partition_map.keys():

    ss_active_count[k]=len(active_ss_partition_map[k])

print ss_active_count


barlist=plt.bar(range(len(ss_active_count)), ss_active_count.values(), align='center')
plt.xticks(range(len(ss_active_count)), ss_active_count.keys())

plt.show()