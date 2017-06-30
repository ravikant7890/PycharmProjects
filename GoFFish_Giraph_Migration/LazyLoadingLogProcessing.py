'''
The input is directory with directory for each giraph application
'''

import os
import sys
import pandas as pd
import subprocess

parent_folder=sys.argv[1]
number_of_partition=int(sys.argv[2])

cmd="ls -1 "+parent_folder

out_dir_list=[]

for out_dir in os.popen(cmd).read().split("\n"):
    if out_dir:
        out_dir_list.append(out_dir)




df_app= pd.DataFrame(columns=('PreLoadWO','Loading','PreAPPWC','updateGraph','PostApplication'))



df_SS= pd.DataFrame(columns=('ss','SSTime', 'ComputeTime', 'MigrationTime' ,'PartitionAssign','PreSS','PostSS'))

for log_dir in out_dir_list:

    print "processing " +log_dir

    df_SS= pd.DataFrame(columns=('ss','SSTime', 'ComputeTime', 'MigrationTime' ,'PartitionAssign','PreSS','PostSS'))

    df_partition=pd.DataFrame(columns=('pid','sgid','ss','compute'))

    os.chdir(parent_folder+"/"+log_dir)

    #get number of ss
    no_of_ss_cmd=" grep -R ALL_SUPERSTEPS_DONE |awk '{print $NF}' "

    no_of_ss = int(subprocess.check_output(no_of_ss_cmd, shell=True)[:-1])

    for i in range(0,no_of_ss):

        #master time
        #grep -R "superstep 0: Took" |awk '{print $(NF-1)}'
        masterTime_cmd="grep -R  \"superstep "+str(i)+ ": Took \" |awk '{print $(NF-1)}' "

        # print masterTime_cmd

        masterTime_sec=float(subprocess.check_output(masterTime_cmd,shell=True))

        masterTime=int(masterTime_sec*1000)

        #maxComputeTime
        # grep -R processGraphPartitions,took,|grep superstep,0,|awk -F"," 'BEGIN{max=0}{if($NF>max)max=$NF}END{print max}'
        maxCompute_cmd=" grep -R processGraphPartitions,took,|grep superstep,"+str(i)+",|awk -F\",\" 'BEGIN{max=0}{if($NF>max)max=$NF}END{print max}' "

        maxCompute=int(subprocess.check_output(maxCompute_cmd,shell=True))

        #maxMigration
        maxMigration_cmd=" grep -R ,exchangePartitions,took,|grep superstep,"+str(i)+",|awk -F\",\" 'BEGIN{max=0}{if($NF>max)max=$NF}END{print max}' "

        maxMigration=int(subprocess.check_output(maxMigration_cmd,shell=True))
        #PartititonAssignment
        maxPartitionAssign_cmd=" grep -R ,masterAssignment,took,|grep superstep,"+str(i)+",|awk -F\",\" 'BEGIN{max=0}{if($NF>max)max=$NF}END{print max}' "

        maxPartitionAssign=int(subprocess.check_output(maxPartitionAssign_cmd,shell=True))

        # maxPrepare
        maxPrepare_cmd=" grep -R ,prepareForSuperstep,took,|grep superstep,"+str(i)+",|awk -F\",\" 'BEGIN{max=0}{if($NF>max)max=$NF}END{print max}' "

        maxPrepare=int(subprocess.check_output(maxPrepare_cmd,shell=True))

        # maxCollectStats
        maxCollectStat_cmd=" grep -R ,collectStats,took,|grep superstep,"+str(i)+",|awk -F\",\" 'BEGIN{max=0}{if($NF>max)max=$NF}END{print max}' "

        maxCollectStat=int(subprocess.check_output(maxCollectStat_cmd,shell=True))

        # print maxCollectStat

        row=[int(i),int(masterTime),int(maxCompute),int(maxMigration),int(maxPartitionAssign),int(maxPrepare),int(maxCollectStat)]

        # print row

        df_SS.loc[len(df_SS)]=row

        # print df_SS
        df_SS.to_csv(log_dir,index=None)

        for pid in range(0,number_of_partition):

            #COMPUTE,superstep,6,sgid,25769803777,pid,6,computeTime,0

            grep_cmd="grep -R COMPUTE,superstep,|grep superstep,"+str(i)+"| grep ,pid,"+str(pid)+",|awk -F\",\" '{sum+= $NF}END{print sum}' "
            # print grep_cmd
            ans=subprocess.check_output(grep_cmd,shell=True)

            try:
                computeTime=int(ans)
            except:
                # print grep_cmd
                continue
            if len(ans)>0:
                computeTime=int(ans)
            # computeTime=int(subprocess.check_output(grep_cmd,shell=True))
            # print computeTime
            if computeTime:
                row=[pid,pid,i+1,computeTime]
                df_partition.loc[len(df_partition)]=row


    print df_SS

    # print df_partition

    # df=df_SS[['SSTime']]

    df_SS.to_csv(log_dir,index=None)

    df_partition = df_partition.astype(int)

    df_partition.to_csv(log_dir+"_partition.csv",index=None,header=None)