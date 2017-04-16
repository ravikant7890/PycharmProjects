#! /usr/bin/env python
import sys
import os
import subprocess
# sys.path.append('/usr/lib/python2.7/site-packages/')


from collections import defaultdict



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
    for (v,v_neighbors) in megaPartition:
        reordering[vid] = v
        rReordering[v] = vid
        vid = vid + 1
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
    shell.call(['gpmetis', tempMetisInputPath,str(numPartitions)])
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

    print "*****************************************************"
    print "Call to metis_command"
    print "Args : inputpath "+str(inputPath)
    print "Args : numPartitions1 "+str(numPartitions1)
    print "Args : numPartitions2 "+str(numPartitions2)
    print "*****************************************************"

    from scriptine import shell
    if int(numPartitions1) > 1:
        print "calling metis " + " shell.call(['gpmetis',inputPath,str(numPartitions1)]) "
        print "Args : inputpath "+str(inputPath)
        print "Args : numPartitions1 "+str(numPartitions1)
        print "Args : numPartitions2 "+str(numPartitions2)
        # shell.call(['gpmetis',inputPath,str(numPartitions1)])
    else :
        print "In the else part"
        # tmpFile = open(inputPath + '.part.1', 'w')
        # origFile = open(inputPath)
        # first_line = origFile.read().strip().split()
        # vertices = int(first_line[0])
        # for v in xrange(vertices):
        #     tmpFile.write('0\n')
        # tmpFile.close()
        # origFile.close()
        # print inputPath + '.part.1'


    print "*****************************************************"
    print "done with if else part"



    #take the input path as argument &fome the input for blogel partitioner

    orkut_for_vornoi="/data/ipdpsw-hpbdc-2016/ORKT-4Blogel-5D/Vornoi-input.txt"

    print "*********************************************************"

    print " forming the file for blogel input from "+str(inputPath)+" to "+orkut_for_vornoi
    # f1=open(inputPath,'r')
    f2=open(orkut_for_vornoi,'w')

    zenda=True
    vertex_id=1
    with open(inputPath) as f:
        for line in f:
            if zenda:
                zenda=False
                continue
            neighbours=line.split()
            # print neighbours
            v_line=str(vertex_id)+"\t"+str(len(neighbours))
            for n in neighbours:
                v_line=v_line+" "+str(n)
            v_line=v_line+"\n"
            vertex_id=vertex_id+1
            # print v_line
            f2.write(v_line)


    f.close()
    f2.close()

    print "*******************wrtinting done**************************************"

    copy_to_hdfs_command="hadoop dfs -copyFromLocal /data/ipdpsw-hpbdc-2016/ORKT-4Blogel-5D/Vornoi-input.txt /user/anshu/Blogel-graphs/Metis2Blogel-ORKT10D/"


    print "***********************moving the file to hdfs**********************************"
    os.system(copy_to_hdfs_command)

    #run mpi job
    os.chdir("/home/anshu/hashmin/")
    # run_vornoi_command="mpiexec -n 80 -f $HOME/hashmin/conf  $HOME/hashmin/run"

    run_vornoi_command=" mpiexec.hydra -iface eth0 -f /home/anshu/hashmin/conf -n 80 /home/anshu/hashmin/run"

    print "*********************run mpi job************************************"
    # os.system(run_vornoi_command)

    print run_vornoi_command

    run_proc1=subprocess.Popen(run_vornoi_command,shell=True)

    subprocess.Popen.wait(run_proc1)

    os.chdir("/data/4Mccgrid/goffish-deploy/client/gofs-client/")

    copy_from_hdfs_command="hadoop dfs -copyToLocal /user/anshu/VornoiPartitioned-graphs/6-2-2016/ORKT-5D/part*  /data/ipdpsw-hpbdc-2016/VornoiPartitioned-5D/"

    print "*********************copy the result from hdfs************************************"

    print copy_from_hdfs_command

    os.system(copy_from_hdfs_command)

    print "********************copied*************************************"
    # os.chdir("/scratch/ipdpsw-hpbdc-2016/Metis2Blogel/")


    print "*******************forming the file for metis output**************************************"

    os.system(' cat /data/ipdpsw-hpbdc-2016/VornoiPartitioned-5D/part* >/data/ipdpsw-hpbdc-2016/VornoiPartitioned-5D/ORKT_5P-Vornoi')

    os.system('awk \'{ print $1, $3 }\' /data/ipdpsw-hpbdc-2016/VornoiPartitioned-5D/ORKT_5P-Vornoi |sort -k1 -n |awk \'{print $2}\' >> /data/ipdpsw-hpbdc-2016/VornoiPartitioned-5D/ORKT_5P-Vornoi.part.5')

    # print "********************** file written as metis output @ ***********************************"

    partitionPath = inputPath + '.part.' + str(numPartitions2)

    # partitionPath="/scratch/ipdpsw-hpbdc-2016/VornoiPartitioned-5D/ORKT_5P-Vornoi.part.5"

    os.system("mv \"/data/ipdpsw-hpbdc-2016/VornoiPartitioned-5D/ORKT_5P-Vornoi.part.5\"  "+partitionPath)

    print "********************** file written as metis output @ ***********************************"

    print " metis output is in " +str(partitionPath)



    return partitionPath

    fPartition = open(partitionPath,'r')
    partitions = [0] + [eval(x)+1 for x in fPartition.readlines()]

    print "partitions "
    # print partitions

    # z=raw_input()

    fMetisInput = open(inputPath, 'r')
    metisInput = [[int(a) for a in x.strip().split()] for x in fMetisInput.readlines()]
    megaPartitions = defaultdict(list)
    for i in xrange(1,len(metisInput)):
        megaPartitions[partitions[i]].append((i,metisInput[i]))


    print "megapartitions"

    print megaPartitions.keys()


    # z=raw_input()

    for i in xrange(1,int(numPartitions1) + 1):
        hierarchialize(megaPartitions[i],i,partitions,numPartitions2)
    partitionFilePath = inputPath + ".part." + str(int(numPartitions1) * int(numPartitions2))
    print partitionFilePath
    print numPartitions1
    print numPartitions2
    generateNewPartitions(partitions, partitionFilePath)

if __name__ == "__main__":
  cmdargs = str(sys.argv)
  print ("Args list: %s " % cmdargs)
  import scriptine
  scriptine.run()


