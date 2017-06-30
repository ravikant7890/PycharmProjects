#!/usr/bin/python
import numpy as np
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import pprint
import os
import sys
# import binpacking

matplotlib.rcParams.update({'font.size': 5})

mapiing_file=sys.argv[1]

stats_file=sys.argv[2]

f1 = open(mapiing_file,'r').readlines()
f2 = open(stats_file, 'r').readlines()

stat_map={}

for l in f2:
    if l:
        pid=int(l.split()[0])
        count=int(l.split()[1])
        stat_map[pid]=count


d = {}
# for line in f1:
#   node, part = line.rstrip().split()
#   print node + " " + part
#   for l in f2:
#     p, count = l.rstrip().split()
#     # print p + " " + count
#     if part == p:
#       d.setdefault(node,{})[part] = count
for l in f1:
    print l
    l=l.rstrip()
    if l:
        wid=int(l.split()[0])
        pid=int(l.split()[1])

        if wid in d:
            k=d[wid]
            k[pid]=stat_map[pid]
            d[wid]=k

        else:
            k={}
            k[pid]=stat_map[pid]
            d[wid]=k





pprint.pprint(d)

new_arr = []
nodes = []
print "Length of d: " + str(len(d))

size = 0

for k in d:
  if size < len(d[k]):
    size = len(d[k])


for k in sorted(d):
  i = 0
  v = d[k]
  count = 0

  # print new_arr

  # print v
  nodes.append(k)
  for val in v:
    count += 1
    if len(new_arr) == size:
      a = new_arr[i]
      a.append(int(v[val]))
      new_arr[i] = a
    else:
      a = []
      a.append(int(v[val]))
      new_arr.append(a)
    i += 1

  print count, size
  for z in range(count,size):
      if len(new_arr)<=z:
          new_arr.append([0])
      else:
          q=new_arr[z]
          q.append(0)
          new_arr[z]=q


  # while len(new_arr)<40:
  #   new_arr.append(0)


pprint.pprint(new_arr)
print nodes

ind = np.arange(len(nodes))
width = 0.35
fig = plt.figure()
ax = plt.axes()

pdf = matplotlib.backends.backend_pdf.PdfPages("orkut_job_graph_10.pdf")

oldl = []
for l in new_arr:
  if len(oldl) == 0:
    plt.bar(ind, l, width)
    y1 = [ x/2 for x in l ]
    oldl = l
  else:
    plt.bar(ind, l, width, bottom = oldl)
    temp1 = [ x for x in l ]
    y1 = [ x/2 + y for x, y in zip(temp1, oldl) ]
    oldl = [x + y for x, y in zip(l, oldl)]
  x1 = [x + 0.175 for x in ind]
  for a,b,c in zip(x1, y1, l):
    ax.annotate(str(c), xy=(a,b), horizontalalignment='center', va='center')


plt.ylabel('Edge Count')
plt.xticks(ind + 0.175, nodes)

pdf.savefig(fig)

pdf.close()

