# get the superstep times from giraph

#inside the directory
import os
import sys
import pandas as pd


parent_folder=sys.argv[1]
output_dir=sys.argv[2]

os.system("mkdir -p "+output_dir)

#get all directories
cmd="ls -1 "+parent_folder

out_dir_list=[]

for out_dir in os.popen(cmd).read().split("\n"):
    if out_dir:
        out_dir_list.append(out_dir)


for dir in out_dir_list:

    print "processing directory "+parent_folder+"/"+dir

    result_dir=output_dir+"/"+dir
    os.system("mkdir "+result_dir)

    os.chdir(parent_folder+"/"+out_dir)

    ss_time_command="grep -R seconds |grep \"superstep [0-9]*:\" |awk '{print $11}' "

    df_sstime=pd.DataFrame(columns=('ss','master_time'))
    # os.system(ss_time_command)
    superstep_count=0
    for entry in os.popen(ss_time_command).read().split("\n"):
        if entry:
            entry=float(entry)*1000.0
            arr=[superstep_count,entry]
            df_sstime.loc[len(df_sstime)] = arr
            superstep_count+=1


    print df_sstime

    # df_sstime.to_csv(result_dir+"/ss_time.csv")

    max_partition_loading_time=" grep -R \"Calling ReadSubgraph,superstep\"|awk -F\",\" '{print $4,$8,$NF}' "

    # os.system(max_partition_loading_time)
    part_loadingtime_dict={}
    ss_partload_dict={}

    df = pd.DataFrame(columns=('ss', 'pid', 'load_time'))

    for entry in os.popen(max_partition_loading_time).read().split("\n"):
        if entry:
            # print entry
            # ss_partload_dict[int(entry.split()[0])]=(int(entry.split()[1]),int(entry.split()[2]))
            # part_loadingtime_dict
            arow2 = [int(entry.split()[0]),int(entry.split()[1]), int(entry.split()[2])]
            df.loc[len(df)] = arow2


    # print df
    df.to_csv(result_dir+"/load_time.csv")

    max_loading_time={}#key->ss,value->maxloadtime

    for i in range(0,superstep_count):

        df2=df.loc[df['ss'] == i]
        df3=df2.groupby('pid').sum()
        if len(df3)>0:
            # print df3
            max_loading_time[i]=df3['load_time'].max()
        else:
            max_loading_time[i]=0

    print max_loading_time
        # exit()
    df_maxloading_time=pd.DataFrame(max_loading_time.items(), columns=['ss', 'max_loading_time'])

    print df_maxloading_time

    # df_maxloading_time.to_csv(result_dir+"/max_loading_time.csv")
    #actual migration time

    df_migration_time = pd.DataFrame(columns=('ss', 'migration_time'))

    for i in range(0,superstep_count):

        migration_time_command= "grep -R \"TEST,GraphTaskManager.execute,done partitionExchange,superstep,\""+str(i)+"|awk -F\",\" 'BEGIN{max=0}{if(max< $8)max=$8}END{print max}' "

        os.system(migration_time_command)

        for entry in os.popen(migration_time_command).read().split("\n"):
            if entry:
                # print entry
                # ss_partload_dict[int(entry.split()[0])]=(int(entry.split()[1]),int(entry.split()[2]))
                # part_loadingtime_dict
                arow2 = [i, int(entry.split()[0])]
                df_migration_time.loc[len(df_migration_time)] = arow2


    # print df_migration_time
    # df.to_csv(result_dir+"/load_time.csv")

    finaldf=pd.merge(pd.merge(df_sstime,df_migration_time,on='ss'),df_maxloading_time,on='ss')

    print finaldf

    finaldf.to_csv(result_dir+"/results.csv",index=False)

    #get the similar metrics from schedule -- master_time,migration_time,
    