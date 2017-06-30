import os
import sys
import csv

#input file format
#pid,ss,wid

loaddict={}

f = open(sys.argv[1], 'rt')
try:
    reader = csv.reader(f)
    for row in reader:

        if(float(row[2])>40):
            continue

        if(int(row[2]) in loaddict.keys()):
            l=loaddict[int(row[2])]
            l.add(int(row[0]))
            loaddict[int(row[2])]=l
        else:
            l=set()
            l.add(int(row[0]))
            loaddict[int(row[2])]=l

finally:
    f.close()
###

print loaddict

f = open(sys.argv[2], 'wt')
try:
    # writer = csv.writer(f)
    # writer.writerow( ('Title 1', 'Title 2', 'Title 3') )

    for i in loaddict.keys():
        s=str(i)
        for j in loaddict[i]:
            s=s+","+str(j)
        f.write( s )
        f.write("\n")
finally:
    f.close()

print open(sys.argv[2], 'rt').read()