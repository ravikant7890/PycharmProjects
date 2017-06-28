import matplotlib

from pip.req.req_set import make_abstract_dist

matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import  os
import sys
import shutil
import re
import subprocess
import matplotlib.pyplot as plt
import pandas as pd
import time


parent_folder=sys.argv[1]

output_folder=sys.argv[2]

simulation_folder=sys.argv[3]
constraint=sys.argv[4]

max_constraint=sys.argv[5]
partition_size=sys.argv[6] #in case of value migration-- the size of the distance map size

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
    # command="python /home/ravikant/PycharmProjects/PycharmProjects/GoFFish_Giraph_Migration/read_csv.py "+new_filename+" "+simulation_folder+"/"+new_filename
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

import numpy as np

# print makespan_list

# exit()

# print metalist


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
# plt.violinplot(makespan_list)
# plt.grid()
# plt.minorticks_on()
# plt.grid(b=True, which='major', color='b', linestyle='-')
# plt.grid(b=True, which='minor', color='r', linestyle='--')
fig = plt.figure(1,  figsize=(9, 6))
ax = fig.add_subplot(111)
bp = ax.violinplot(makespan_list,showmedians=True,showmeans=True,showextrema=True)

bp['cmeans'].set_color('b')
bp['cmedians'].set_color('g')
bp['cmaxes'].set_color('g')
bp['cmins'].set_color('g')
# bp['cmins'].
# ax.set_ylabel('Execution Time(ms)',size=15)
for pc in bp['bodies']:
    pc.set_facecolor('#EEE685')
    pc.set_edgecolor('black')

    pc.set_alpha(1)

ax.yaxis.grid(which='minor', alpha=0.5)
ax.yaxis.grid(which='major', alpha=0.5)
ax.minorticks_on()


from pylab import *

mean=[]
for l in makespan_list:

    mean.append(sum(l)/len(l))



medians=[]

for l in makespan_list:
    medians.append(median(l))

#writing mean and median values
for i in range(1,len(medians) + 1):
	text(i,medians[i-1],'%.1f' % medians[i-1],horizontalalignment='right',color='red',fontsize=12)

for i in range(1,len(mean) + 1):
	text(i,mean[i-1],'%.1f' % mean[i-1],horizontalalignment='left',color='purple',fontsize=12)

#marking median with custom symbol
inds = np.arange(1, len(medians) + 1)
ax.scatter(inds, medians, marker='o', color='white', s=30, zorder=3)


quartile1_1,quartile2_1=np.percentile([makespan_list[0]], [25, 75], axis=1)
quartile1_2,quartile2_2=np.percentile([makespan_list[1]], [25, 75], axis=1)
quartile1_3,quartile2_3=np.percentile([makespan_list[2]], [25, 75], axis=1)
quartile1_4,quartile2_4=np.percentile([makespan_list[3]], [25, 75], axis=1)
quartile1_5,quartile2_5=np.percentile([makespan_list[4]], [25, 75], axis=1)
quartile1_6,quartile2_6=np.percentile([makespan_list[5]], [25, 75], axis=1)
#


quartile1=[quartile1_1[0],quartile1_2[0],quartile1_3[0],quartile1_4[0],quartile1_5[0],quartile1_6[0]]
quartile3=[quartile2_1[0],quartile2_2[0],quartile2_3[0],quartile2_4[0],quartile2_5[0],quartile2_6[0]]
inds = np.arange(1, len(medians) + 1)
ax.vlines(inds, quartile1, quartile3, color='k', linestyle='-', lw=5)

# medians=[median(dSpout['vertex'].dropna().tolist()),median(dSpout['bfs'].dropna().tolist()),median(dSpout['select'].dropna().tolist()),median(dSpout['reach'].dropna().tolist()),median(dSpout['report'].dropna().tolist())]


fig = matplotlib.pyplot.gcf()
# fig.set_size_inches(15.5, 6.5)

# plt.show()

plt.savefig(plotfolder+"/"+graph_name+"_makespan.pdf")
plt.close()

os.system("pdfcrop "+plotfolder+"/"+graph_name+"_makespan.pdf")
os.system("mv "+plotfolder+"/"+graph_name+"_makespan-crop.pdf " +plotfolder+"/"+graph_name+"_makespan.pdf")

########################################


axes = plt.gca()
plt.xticks([1, 2, 3,4,5,6], ['Default', 'FFD', 'FFDM','FFDMP','MinMax','MF/P'])
plt.ylabel("VM Billed Core-Mins")
# ymax=max([sublist[-1] for sublist in coremin_list])
ymax=getmax(coremin_list)
print ymax
axes.set_ylim([0,ymax+5])
# plt.title(graph_name+"_core-minutes")
fig = plt.figure(1, figsize=(9, 6))
ax = fig.add_subplot(111)
bp = ax.violinplot(coremin_list,showmedians=True,showmeans=True,showextrema=True)

bp['cmeans'].set_color('b')
bp['cmedians'].set_color('g')
bp['cmaxes'].set_color('g')
bp['cmins'].set_color('g')
# bp['cmins'].
# ax.set_ylabel('Execution Time(ms)',size=15)
for pc in bp['bodies']:
    pc.set_facecolor('#EEE685')
    pc.set_edgecolor('black')

    pc.set_alpha(1)

ax.yaxis.grid(which='minor', alpha=0.5)
ax.yaxis.grid(which='major', alpha=0.5)
ax.minorticks_on()


from pylab import *

mean=[]
for l in coremin_list:

    mean.append(sum(l)/len(l))



medians=[]

for l in coremin_list:
    medians.append(median(l))

#writing mean and median values
for i in range(1,len(medians) + 1):
	text(i,medians[i-1],'%.1f' % medians[i-1],horizontalalignment='right',color='red',fontsize=12)

for i in range(1,len(mean) + 1):
	text(i,mean[i-1],'%.1f' % mean[i-1],horizontalalignment='left',color='purple',fontsize=12)

#marking median with custom symbol
inds = np.arange(1, len(medians) + 1)
ax.scatter(inds, medians, marker='o', color='white', s=30, zorder=3)


quartile1_1,quartile2_1=np.percentile([coremin_list[0]], [25, 75], axis=1)
quartile1_2,quartile2_2=np.percentile([coremin_list[1]], [25, 75], axis=1)
quartile1_3,quartile2_3=np.percentile([coremin_list[2]], [25, 75], axis=1)
quartile1_4,quartile2_4=np.percentile([coremin_list[3]], [25, 75], axis=1)
quartile1_5,quartile2_5=np.percentile([coremin_list[4]], [25, 75], axis=1)
quartile1_6,quartile2_6=np.percentile([coremin_list[5]], [25, 75], axis=1)
#


quartile1=[quartile1_1[0],quartile1_2[0],quartile1_3[0],quartile1_4[0],quartile1_5[0],quartile1_6[0]]
quartile3=[quartile2_1[0],quartile2_2[0],quartile2_3[0],quartile2_4[0],quartile2_5[0],quartile2_6[0]]
inds = np.arange(1, len(medians) + 1)
ax.vlines(inds, quartile1, quartile3, color='k', linestyle='-', lw=5)

# medians=[median(dSpout['vertex'].dropna().tolist()),median(dSpout['bfs'].dropna().tolist()),median(dSpout['select'].dropna().tolist()),median(dSpout['reach'].dropna().tolist()),median(dSpout['report'].dropna().tolist())]


fig = matplotlib.pyplot.gcf()
# fig.set_size_inches(15.5, 6.5)

# plt.show()

plt.savefig(plotfolder+"/"+graph_name+"_coremin.pdf")
plt.close()

os.system("pdfcrop "+plotfolder+"/"+graph_name+"_coremin.pdf")
os.system("mv "+plotfolder+"/"+graph_name+"_coremin-crop.pdf " +plotfolder+"/"+graph_name+"_coremin.pdf")




################################################################################
axes = plt.gca()
plt.xticks([1, 2, 3,4,5,6], ['Default', 'FFD', 'FFDM','FFDMP','MinMax','MF/P'])
plt.ylabel("VM Used Core-Secs")
# ymax=max([sublist[-1] for sublist in coresec_list])
ymax=getmax(coresec_list)
print ymax
axes.set_ylim([0,ymax+100])
# plt.title(graph_name+"_core-seconds")
fig = plt.figure(1, figsize=(9, 6))
ax = fig.add_subplot(111)
bp = ax.violinplot(coresec_list,showmedians=True,showmeans=True,showextrema=True)

bp['cmeans'].set_color('b')
bp['cmedians'].set_color('g')
bp['cmaxes'].set_color('g')
bp['cmins'].set_color('g')
# bp['cmins'].
# ax.set_ylabel('Execution Time(ms)',size=15)
for pc in bp['bodies']:
    pc.set_facecolor('#EEE685')
    pc.set_edgecolor('black')

    pc.set_alpha(1)

ax.yaxis.grid(which='minor', alpha=0.5)
ax.yaxis.grid(which='major', alpha=0.5)
ax.minorticks_on()


from pylab import *

mean=[]
for l in coresec_list:

    mean.append(sum(l)/len(l))



medians=[]

for l in coresec_list:
    medians.append(median(l))

#writing mean and median values
for i in range(1,len(medians) + 1):
	text(i,medians[i-1],'%.1f' % medians[i-1],horizontalalignment='right',color='red',fontsize=12)

for i in range(1,len(mean) + 1):
	text(i,mean[i-1],'%.1f' % mean[i-1],horizontalalignment='left',color='purple',fontsize=12)

#marking median with custom symbol
inds = np.arange(1, len(medians) + 1)
ax.scatter(inds, medians, marker='o', color='white', s=30, zorder=3)


quartile1_1,quartile2_1=np.percentile([coresec_list[0]], [25, 75], axis=1)
quartile1_2,quartile2_2=np.percentile([coresec_list[1]], [25, 75], axis=1)
quartile1_3,quartile2_3=np.percentile([coresec_list[2]], [25, 75], axis=1)
quartile1_4,quartile2_4=np.percentile([coresec_list[3]], [25, 75], axis=1)
quartile1_5,quartile2_5=np.percentile([coresec_list[4]], [25, 75], axis=1)
quartile1_6,quartile2_6=np.percentile([coresec_list[5]], [25, 75], axis=1)
#


quartile1=[quartile1_1[0],quartile1_2[0],quartile1_3[0],quartile1_4[0],quartile1_5[0],quartile1_6[0]]
quartile3=[quartile2_1[0],quartile2_2[0],quartile2_3[0],quartile2_4[0],quartile2_5[0],quartile2_6[0]]
inds = np.arange(1, len(medians) + 1)
ax.vlines(inds, quartile1, quartile3, color='k', linestyle='-', lw=5)

# medians=[median(dSpout['vertex'].dropna().tolist()),median(dSpout['bfs'].dropna().tolist()),median(dSpout['select'].dropna().tolist()),median(dSpout['reach'].dropna().tolist()),median(dSpout['report'].dropna().tolist())]


fig = matplotlib.pyplot.gcf()
# fig.set_size_inches(15.5, 6.5)

# plt.show()

plt.savefig(plotfolder+"/"+graph_name+"_coresec.pdf")
plt.close()


os.system("pdfcrop "+plotfolder+"/"+graph_name+"_coresec.pdf")
os.system("mv "+plotfolder+"/"+graph_name+"_coresec-crop.pdf " +plotfolder+"/"+graph_name+"_coresec.pdf")



################################################################################
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
