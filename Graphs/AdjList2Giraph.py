
import os
import sys

f = open(sys.argv[1], 'r')
f2=open(sys.argv[2],'w')


for line in f:

    src=int(line.split()[0])

    flag=0

    # sinkList=[]

    valueString=""
    prefix=""

    for sink in line.split():
        if flag==0:
            flag=1
            continue
        else:
            # sinkList.append(int(sink))
            valueString=valueString+prefix+"[" +str(sink)+",1]"
            prefix=","

    record= "["+str(src)+",0,["+valueString+"]]"
    print record

    f2.write(record+'\n')

f2.close()
f.close()





