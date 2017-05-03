import  os
import sys
import shutil
import re
import subprocess
import matplotlib.pyplot as plt
import pandas as pd

parent_folder=sys.argv[1]

output_folder=sys.argv[2]

simulation_folder=sys.argv[3]
constraint=sys.argv[4]

max_constraint=sys.argv[5]
partition_size=sys.argv[6]

plotfolder=sys.argv[7]


SERIALIZATION_TIME=(sys.argv[8])

DESERIALIZATION_TIME=(sys.argv[9])

#get max from list of lists
def getmax(listoflist):

    ans=-1
    for list in listoflist:

        if(ans < max(list)):
            ans=max(list)

    return ans


df_makespan= pd.DataFrame(columns=('FileName', 'Default', 'FFD' ,'FFDM','FFDMPlanning','MinMax','MF/P'))
df_coremin = pd.DataFrame(columns=('FileName', 'Default', 'FFD' ,'FFDM','FFDMPlanning','MinMax','MF/P'))
df_coresec = pd.DataFrame(columns=('FileName', 'Default', 'FFD' ,'FFDM','FFDMPlanning','MinMax','MF/P'))

os.system("mkdir -p "+output_folder)
os.system("mkdir -p "+simulation_folder)
os.system("mkdir -p "+plotfolder)

cmd="ls -1 "+parent_folder

out_dir_list=[]

makespan_list=[[],[],[],[],[],[]]
coremin_list=[[],[],[],[],[],[]]
coresec_list=[[],[],[],[],[],[]]

for out_dir in os.popen(cmd).read().split("\n"):
    if out_dir:
        out_dir_list.append(out_dir)

srcvid=-100
sgid=-100
pid=-100

for filename in out_dir_list:

    srcvid=-100
    sgid=-100
    pid=-100

    # filename=sys.argv[1]
    f=open(parent_folder+"/"+filename)

    # print filename

    graph_name=filename.split("_")[1]
    for line in f:
        # print line
        pid=line.split(",")[4][:-1]
        srcvid=line.split(",")[2].split(":")[1]
        sgid=line.split(",")[3]

        break

    # print graph_name
    #
    # print pid
    #
    # print srcvid
    #
    # print sgid

    new_filename=graph_name+"_"+srcvid+"_"+sgid+"_"+pid+"_.csv"

    # print new_filename

    shutil.copy(parent_folder+"/"+filename, output_folder+"/"+new_filename)

    # new_filename=output_folder+"/"+new_filename

    os.system("sed -i 1,2d "+output_folder+"/"+new_filename)

    # print new_filename
    # command="python /home/ravikant/PycharmProjects/GoFFish_Giraph_Migration/read_csv.py "+new_filename+" "+simulation_folder+"/"+new_filename
    # print command
    ####run the read_csv script to get the format required for simulation
    os.system("python /home/ravikant/PycharmProjects/GoFFish_Giraph_Migration/read_csv.py "+output_folder+"/"+new_filename+" "+simulation_folder+"/"+new_filename)


################################################


cmd="ls -1 "+simulation_folder

out_dir_list=[]


for out_dir in os.popen(cmd).read().split("\n"):
    if out_dir:
        out_dir_list.append(out_dir)

#command for Default.FFD,FFDwithMigration
#python FFD.py ORKT_40P_40W_1_SRCPID5.csv 5 40

#command for FFD_LossGain_VMIncrement
#python FFD_LossGain_VmIncrement.py ORKT_40P_40W_1_SRCPID5.csv 5 40 45 15000

#commad for MinMax approach
#python MinMax_FFD_LossGain_VMIncreament.py ORKT_40P_40W_1_SRCPID5.csv 5 40 10 100 15000

count=0

constraint_values=[]

for filename in out_dir_list:

    count+=1

    no_of_partitions=re.findall('\d+', filename.split("_")[0])[0]

    source_partition=filename.split("_")[3]

    constraint=sys.argv[4]

    print "************************************************"
    print "processing ",filename
    print "************************************************"
    # print source_partition
    #
    # print no_of_partitions
    constraint=sys.argv[4]

    max_constraint=sys.argv[5]

    #######################################################
    # exit()
    command_for_Default_FFD_FFDwithMigration="python /home/ravikant/PycharmProjects/GoFFish_Giraph_Migration/FFD.py "+simulation_folder+"/"+filename+" "+source_partition+" "+no_of_partitions+" "+partition_size+" "+SERIALIZATION_TIME+" "+DESERIALIZATION_TIME

    print "executing command ",command_for_Default_FFD_FFDwithMigration

    # os.system(command_for_Default_FFD_FFDwithMigration)

    result = subprocess.check_output(command_for_Default_FFD_FFDwithMigration, shell=True)
    outcome= result.split("\n")
    FFDwithMigration= outcome[-2]
    FFD= outcome[-3]
    default= outcome[-4]

    print "default",default
    print "FFD",FFD
    print "FFDwithMigration",FFDwithMigration
    ####################################################################
    default_makspan=default.split(",")[0]

    command_for_FFD_LossGainVMIncrement="python /home/ravikant/PycharmProjects/GoFFish_Giraph_Migration/FFD_LossGain_VmIncrement.py "+simulation_folder+"/"+filename+" "+source_partition+" "+no_of_partitions+" "+constraint+" "+default_makspan+" "+partition_size +" "+SERIALIZATION_TIME+" "+DESERIALIZATION_TIME


    print "executing command ",command_for_FFD_LossGainVMIncrement

    result = subprocess.check_output(command_for_FFD_LossGainVMIncrement, shell=True)
    outcome= result.split("\n")
    FFDLossGainVMIncrement= outcome[-2]

    print "FFDLossGainVMIncrement",FFDLossGainVMIncrement

    while(FFDLossGainVMIncrement.split()[0]=="ERROR"):
        print "can not schedule with constraint ",constraint+" enter increased value"
        constraint=str(int(constraint)+5)
        command_for_FFD_LossGainVMIncrement="python /home/ravikant/PycharmProjects/GoFFish_Giraph_Migration/FFD_LossGain_VmIncrement.py "+simulation_folder+"/"+filename+" "+source_partition+" "+no_of_partitions+" "+constraint+" "+default_makspan+" "+partition_size +" "+SERIALIZATION_TIME+" "+DESERIALIZATION_TIME
        print "executing command ",command_for_FFD_LossGainVMIncrement

        result = subprocess.check_output(command_for_FFD_LossGainVMIncrement, shell=True)
        outcome= result.split("\n")
        FFDLossGainVMIncrement= outcome[-2]
        # print "FFDLossGainVMIncrement",FFDLossGainVMIncrement
        # exit()
    constraint_values.append(int(constraint))

    print "FFDLossGainVMIncrement",FFDLossGainVMIncrement

    #######################################################



    command_for_MinMax="python /home/ravikant/PycharmProjects/GoFFish_Giraph_Migration/MinMax_FFD_LossGain_VMIncreament.py "+simulation_folder+"/"+filename+" "+source_partition+" "+no_of_partitions+"  10 "+max_constraint+" "+default_makspan+" "+partition_size +" "+SERIALIZATION_TIME+" "+DESERIALIZATION_TIME


    print "executing command ",command_for_MinMax

    result = subprocess.check_output(command_for_MinMax, shell=True)
    outcome= result.split("\n")
    MinMax= outcome[-2]

    print "MinMax",MinMax

    while(MinMax.split()[0]=="ERROR"):
        min_constraint=max_constraint
        max_constraint=str(int(max_constraint)+100)
        command_for_MinMax="python /home/ravikant/PycharmProjects/GoFFish_Giraph_Migration/MinMax_FFD_LossGain_VMIncreament.py "+simulation_folder+"/"+filename+" "+source_partition+" "+no_of_partitions+"  "+min_constraint+" "+max_constraint+" "+default_makspan+" "+partition_size +" "+SERIALIZATION_TIME+" "+DESERIALIZATION_TIME
        print "executing command ",command_for_MinMax

        result = subprocess.check_output(command_for_MinMax, shell=True)
        outcome= result.split("\n")
        MinMax= outcome[-2]
        # print "FFDLossGainVMIncrement",FFDLossGainVMIncrement
        # exit()

    print "MinMax",MinMax


    ###########################################################

    command_for_MaxFit="python /home/ravikant/PycharmProjects/GoFFish_Giraph_Migration/MaxFitwithPinning.py "+simulation_folder+"/"+filename+" "+source_partition
    print "executing command ",command_for_MaxFit

    result = subprocess.check_output(command_for_MaxFit, shell=True)
    outcome= result.split("\n")
    MaxFit= outcome[-2]

    print "MaxFit",MaxFit


    ###########################################################


    makespan_list[0].append(float(default.split(",")[0]))
    makespan_list[1].append(float(FFD.split(",")[0]))
    makespan_list[2].append(float(FFDwithMigration.split(",")[0]))
    makespan_list[3].append(float(FFDLossGainVMIncrement.split(",")[0]))
    makespan_list[4].append(float(MinMax.split(",")[0]))
    makespan_list[5].append(float(MaxFit.split(",")[0]))

    coremin_list[0].append(float(default.split(",")[1]))
    coremin_list[1].append(float(FFD.split(",")[1]))
    coremin_list[2].append(float(FFDwithMigration.split(",")[1]))
    coremin_list[3].append(float(FFDLossGainVMIncrement.split(",")[1]))
    coremin_list[4].append(float(MinMax.split(",")[1]))
    coremin_list[5].append(float(MaxFit.split(",")[1]))


    coresec_list[0].append(float(default.split(",")[2]))
    coresec_list[1].append(float(FFD.split(",")[2]))
    coresec_list[2].append(float(FFDwithMigration.split(",")[2]))
    coresec_list[3].append(float(FFDLossGainVMIncrement.split(",")[2]))
    coresec_list[4].append(float(MinMax.split(",")[2]))
    coresec_list[5].append(float(MaxFit.split(",")[2]))

    ####update the dataframes
    # df_makespan= pd.DataFrame(columns=('FileName', 'Default', 'FFD' ,'FFDM','FFDMPlanning','MinMax'))
    # df_coremin = pd.DataFrame(columns=('FileName', 'Default', 'FFD' ,'FFDM','FFDMPlanning','MinMax'))
    # df_coresec = pd.DataFrame(columns=('FileName', 'Default', 'FFD' ,'FFDM','FFDMPlanning','MinMax'))


    df_makespan = df_makespan.T
    df_makespan[count]=[filename,float(default.split(",")[0]),float(FFD.split(",")[0]),float(FFDwithMigration.split(",")[0]),float(FFDLossGainVMIncrement.split(",")[0]),float(MinMax.split(",")[0]),float(MaxFit.split(",")[0])]
    df_makespan = df_makespan.T


    df_coremin = df_coremin.T
    df_coremin[count]=[filename,float(default.split(",")[1]),float(FFD.split(",")[1]),float(FFDwithMigration.split(",")[1]),float(FFDLossGainVMIncrement.split(",")[1]),float(MinMax.split(",")[1]),float(MaxFit.split(",")[1])]
    df_coremin = df_coremin.T


    df_coresec = df_coresec.T
    df_coresec[count]=[filename,float(default.split(",")[2]),float(FFD.split(",")[2]),float(FFDwithMigration.split(",")[2]),float(FFDLossGainVMIncrement.split(",")[2]),float(MinMax.split(",")[2]),float(MaxFit.split(",")[2])]
    df_coresec = df_coresec.T


    # exit()

metalist=[]
metalist.append(makespan_list)
metalist.append(coremin_list)
metalist.append(coresec_list)

print metalist


font = {'family' : 'normal',
        'weight' : 'normal', #bold
        'size'   : 16}

import matplotlib
matplotlib.rc('font', **font)




axes = plt.gca()
plt.xticks([1, 2, 3,4,5,6], ['Default', 'FFD', 'FFDM','FFDMP','MinMax','MF/P'])
# plt.title(graph_name+"_makespan")
plt.ylabel("Makespan (seconds)")
# ymax=max([sublist[-1] for sublist in makespan_list])
ymax=getmax(makespan_list)
print ymax
axes.set_ylim([0,ymax+20])
plt.violinplot(makespan_list)
plt.grid()
# plt.minorticks_on()
# plt.grid(b=True, which='major', color='b', linestyle='-')
# plt.grid(b=True, which='minor', color='r', linestyle='--')

plt.savefig(plotfolder+"/"+graph_name+"_makespan.pdf")
plt.close()

axes = plt.gca()
plt.xticks([1, 2, 3,4,5,6], ['Default', 'FFD', 'FFDM','FFDMP','MinMax','MF/P'])
plt.ylabel("VM Billed Core-Mins")
# ymax=max([sublist[-1] for sublist in coremin_list])
ymax=getmax(coremin_list)
print ymax
axes.set_ylim([0,ymax+5])
# plt.title(graph_name+"_core-minutes")
plt.violinplot(coremin_list)
plt.grid()
# plt.minorticks_on()
# plt.grid(b=True, which='major', color='b', linestyle='-')
# plt.grid(b=True, which='minor', color='r', linestyle='--')

plt.savefig(plotfolder+"/"+graph_name+"_coremin.pdf")
plt.close()

axes = plt.gca()
plt.xticks([1, 2, 3,4,5,6], ['Default', 'FFD', 'FFDM','FFDMP','MinMax','MF/P'])
plt.ylabel("VM Used Core-Secs")
# ymax=max([sublist[-1] for sublist in coresec_list])
ymax=getmax(coresec_list)
print ymax
axes.set_ylim([0,ymax+100])
# plt.title(graph_name+"_core-seconds")
plt.violinplot(coresec_list)
plt.grid()
# plt.minorticks_on()
# plt.grid(b=True, which='major', color='b', linestyle='-')
# plt.grid(b=True, which='minor', color='r', linestyle='--')

plt.savefig(plotfolder+"/"+graph_name+"_coresec.pdf")
plt.close()

df_makespan.to_csv(plotfolder+"/"+graph_name+"_makespan.csv")
df_coremin.to_csv(plotfolder+"/"+graph_name+"_coremin.csv")
df_coresec.to_csv(plotfolder+"/"+graph_name+"_coresec.csv")

constraint_filename=plotfolder+"/"+graph_name+"_constraint.csv"


constraint_values.sort()
print constraint_values

thefile = open(constraint_filename, 'w')

for item in constraint_values:
  thefile.write("%s\n" % item)

thefile.close()
