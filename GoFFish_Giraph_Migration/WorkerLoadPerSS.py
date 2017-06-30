'''
1. Partition V+E
2. Pid,SS,WID
3. Pid,sgid,SS,Time
'''

import os
import sys
import csv

partition_stats_file=sys.argv[1]
partition_mapping_file=sys.argv[2]
partition_time_file=sys.argv[3]

partition_activation_schedule={} #ss set{pid}

f = open(partition_time_file, 'rt')

try:
    reader = csv.reader(f)
    for row in reader:
        if row:
            pid=int(row[1])
            ss=int(row[0])

            if ss in partition_activation_schedule.keys():
                l=partition_activation_schedule[ss]
                l.add(pid)
                partition_activation_schedule[ss]=l
            else:
                l=set()
                l.add(pid)
                partition_activation_schedule[ss]=l

finally:
    f.close()


# print partition_activation_schedule

mapping_dict={} #s,{w:pid}


f = open(partition_mapping_file, 'rt')

try:
    reader = csv.reader(f)
    for row in reader:
        if row:
            # print row
            pid=int(row[0])
            ss=int(row[1])
            wid=int(row[2])

            if ss in mapping_dict.keys():

                l=mapping_dict[ss]
                if wid in l.keys():
                    p=l[wid]
                    p.add(pid)
                    l[wid]=p
                    mapping_dict[ss]=l
                else:
                    p=set()
                    p.add(pid)
                    # t={}
                    l[wid]=p
                    mapping_dict[ss]=l

            else:
                l={}
                p=set()
                p.add(pid)
                # t={}
                l[wid]=p
                mapping_dict[ss]=l


finally:
    f.close()


# print mapping_dict

f = open(partition_stats_file,"rt")

stats={}

for line in f:
    # print line
    pid=int(line.split()[0])
    count=int(line.split()[1][:-1])
    stats[pid]=count

# print stats
ss=1

map_set=mapping_dict[1] #wid->pid

for w in map_set.keys():

    for p in map_set[w]:

        if p in partition_activation_schedule[ss]:

            print w,p


