#!/usr/bin/python
import sys
import time

sys.path.append('/usr/lib/python2.7/site-packages/')


from collections import defaultdict

#The header line contains  two (n, m),
# n ---number of vertices
# m ---number of edges

def generateNewPartitions(partitions, partitionFilePath):
    f = open(partitionFilePath , 'w')
    for p in partitions[1:]:
        f.write(str(p-1)+"\n")
    f.close()

def createMetisInputFile(metisInput, filePath):
    f = open(filePath,'w')
    for i in metisInput:
        tmp = " ".join(map(str, i)) + "\n"
        f.write(tmp)
    f.close()
    return filePath

def hierarchialize(megaPartition, partitionId, partitions, numPartitions):
    from scriptine import shell
    reordering = dict()
    rReordering = dict()
    vid = 1

    print "called hierarchilize"

    for (v,v_neighbors) in megaPartition:
        reordering[vid] = v
        rReordering[v] = vid
        vid = vid + 1

    #     megaPartitionVertices has total number of vertices
    megaPartitionVertices = vid - 1
    megaPartiitonEdges = 0
    tempMetisInput = []
    megaPartitionEdges = 0

    for vid in xrange(1, megaPartitionVertices + 1):
        tmp = megaPartition[vid-1][1]
        tmp = filter(lambda x : rReordering.has_key(x), tmp)
        tmp = map(lambda x: rReordering[x], tmp)
        megaPartitionEdges += len(tmp)
        tempMetisInput.append(tmp)


    megaPartitionEdges /= 2
    tempMetisInput = [[megaPartitionVertices, megaPartitionEdges]] + tempMetisInput
    tempMetisInputPath = createMetisInputFile(tempMetisInput, "tmpMetis"+ str(partitionId) + ".txt")

    print "created tmp file for metis "+str(tempMetisInputPath)

    print "calling metis"

    # time.sleep(20)

    shell.call(['gpmetis', tempMetisInputPath,str(numPartitions)])

    # time.sleep(40)

    tempMetisPartitionPath = "tmpMetis" + str(partitionId) + ".txt.part." + str(numPartitions)

    fTempPartition = open(tempMetisPartitionPath,'r')

    tempPartitions = [0] + [(((partitionId-1)*int(numPartitions)) + eval(x) + 1) for x in fTempPartition.readlines()]

    m=set()

    for z in tempPartitions:
        m.add(z)

    print " partitions for partition : "+str(partitionId)

    for z in m:
        print z


    for i in xrange(1,megaPartitionVertices + 1):
        partitions[reordering[i]] = tempPartitions[i]

def metis_command(inputPath, numPartitions1, numPartitions2):
    print "call to metis_command with args:"
    print "inputPath :"+str(inputPath)
    print "numpartitions1 :"+str(numPartitions1)
    print "numpartitions2 :"+str(numPartitions2)

    # time.sleep(120)

    from scriptine import shell
    if int(numPartitions1) > 1:
        print "calling metis " + " shell.call(['gpmetis',inputPath,str(numPartitions1)]) "
        print "Args : inputpath "+str(inputPath)
        print "Args : numPartitions1 "+str(numPartitions1)
        print "Args : numPartitions2 "+str(numPartitions2)

        shell.call(['gpmetis',inputPath,str(numPartitions1)])
    else :
        print "else part in metis_command called with args : "
        print "inputPath "+ str(inputPath)
        print "numPart1 "+str(numPartitions1)
        print "numPart2 "+str(numPartitions2)
        #time.sleep(20)
        tmpFile = open(inputPath + '.part.1', 'w')

        print "created a tmp file "+str(tmpFile)+ " original file "+str(inputPath)
        # z=raw_input()()()

        origFile = open(inputPath)
        first_line = origFile.read().strip().split()
        vertices = int(first_line[0])
        for v in xrange(vertices):
            tmpFile.write('0\n')
        tmpFile.close()
        origFile.close()
        # time.sleep(30)
        print inputPath + '.part.1'
        print "check input path again with lines equal no of vertices  "
        #z=raw_input()()

    partitionPath = inputPath + '.part.' + str(numPartitions1)
    fPartition = open(partitionPath,'r')
    print " executing commnd partitions = [0] + [eval(x)+1 for x in fPartition.readlines()] with fpartitions at "+str(partitionPath)

    # time.sleep(20)
    #z=raw_input()()

    partitions = [0] + [eval(x)+1 for x in fPartition.readlines()]

    print "after execution of commnand partitions:  "

    # for z in range(10):
    #     print str(partitions[z])

    print " input path is "+str(inputPath)+ "  executing command fMetisInput = open(inputPath, 'r')"

    fMetisInput = open(inputPath, 'r')

    metisInput = [[int(a) for a in x.strip().split()] for x in fMetisInput.readlines()]

    print "after execution of commnand metisInput = [[int(a) for a in x.strip().split()] for x in fMetisInput.readlines()] :  "

    megaPartitions = defaultdict(list)

    print "after execution of commnand  megaPartitions = defaultdict(list) :  "

    for i in xrange(1,len(metisInput)):
        megaPartitions[partitions[i]].append((i,metisInput[i]))


    for q in megaPartitions:
        print  megaPartitions[q]

    print "after execution of for loop  :  "


    #z=raw_input()()
    # time.sleep(10)

    for i in xrange(1,int(numPartitions1) + 1):
        print "calling hierarchialize(megaPartitions[i],i,partitions,numPartitions2) with megaPartitions[i]: "+"partitions "+" part2: "+str(numPartitions2)
        #z=raw_input()()
        hierarchialize(megaPartitions[i],i,partitions,numPartitions2)
    partitionFilePath = inputPath + ".part." + str(int(numPartitions1) * int(numPartitions2))
    print "partitionFilePath: "+partitionFilePath
    print numPartitions1
    print numPartitions2
    #z=raw_input()()
    # time.sleep(50)
    print "calling generateNewPartitions(partitions, partitionFilePath) with args partitions "+str(partitions)+ " partitionFilePath "+str(partitionFilePath)
    generateNewPartitions(partitions, partitionFilePath)

if __name__ == "__main__":
  cmdargs = str(sys.argv)
  print ("Args list: %s " % cmdargs)
  import scriptine
  scriptine.run()



