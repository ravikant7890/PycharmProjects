''' Partition a list into sublists whose sums don't exceed a maximum


    for a simple description of the method.
'''
#/home/ravikant/anaconda/bin/python

import sys
import csv
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import math
import time
from munkres import Munkres, print_matrix


def costFunction(vmTime,superstep_time):

    #print "Cost function called"
    present_coreMin=math.ceil(vmTime/60000.0)

    if math.ceil( (vmTime + superstep_time)/60000.0) == present_coreMin:

        return True

    return False




def getFirstNonZeroValueIndex(vmList):

    index=-1

    for i in range(0,len(vmList)):
        if vmList[i] >0:
            return i


    return index



def findMin(vmList):

    ans=(-1,-1,-1)
    for i in range(0,len(vmList)):

        if min(vmList[i:]) !=0:
            ans=(i,vmList.index(min(vmList[i:])),min(vmList[i:]))
            break
        if vmList[i]!=0:
            break

    return ans



def calcCoreMin(ActiveVM,SStime):

    vmList=[]
    SStimeList=[]

    for i in ActiveVM.keys():
        #print i

        vmList.append(int(ActiveVM[(i)]))
        SStimeList.append((SStime[(i)]))

    flag=True

    vmMins =0

    while flag==True:

        vmTime=0
        ans=findMin(vmList)
        #print ans

        if ans==(-1,-1,-1):
            flag=False

        if flag==True:

            start_index=ans[0]
            minValue=ans[2]

            for i  in range(start_index,start_index+len(vmList[start_index:])):
                vmList[i]=vmList[i]-minValue
                #print vmList
                vmTime+=SStimeList[i]

            vmMins+=minValue*math.ceil(vmTime/60000.0)
            #print math.ceil(vmTime/60000.0)
            #print vmMins

    #print vmMins

    #print vmList
    if max(vmList)!=0:
        #Apply the cost function


        non_zero_index=0

        while non_zero_index!= -1:
            #print vmMins
            vmTime=0

            non_zero_index=getFirstNonZeroValueIndex(vmList)

            #print "non zero index "+str(non_zero_index)

            if(non_zero_index != -1):

            #Decrease the ActiveVM value at that index by one and decide whether to keep that VM running in subsequent superstep

                vmList[non_zero_index]=vmList[non_zero_index]-1

                #Add the current superstep time to VM time
                #print SStimeList
                vmTime+=SStimeList[non_zero_index]

                #Iterate over next supersteps until you keep the VM running.
                #print vmList
                SSindex=non_zero_index

                runningFlag=True

                while runningFlag==True:

                    SSindex=SSindex+1
                    #print "SSindex is "+str(SSindex)

                    if int(SSindex) >= int(len(vmList)):
                        vmMins+=math.ceil(vmTime/60000.0)
                        #print "breaking"
                        break




                    #If vm is active in this Superstep then add its time to VMMin else apply cost function

                    if vmList[SSindex] >0 :

                        vmTime+=SStimeList[SSindex]
                        vmList[SSindex]=vmList[SSindex]-1
                        #print vmList

                    else:

                        superstep_time=SStimeList[SSindex]

                        if(costFunction(vmTime,superstep_time)):

                            vmTime+=SStimeList[SSindex]
                            #print "Added"
                            #vmList[SSindex]=vmList[SSindex]-1

                        else:

                            #print "Rounded off"
                            present_vmMin=math.ceil(vmTime/60000.0)

                            #vmTime=present_vmMin*60000

                            vmMins+=present_vmMin

                            runningFlag=False

    return vmMins



class Bin(object):
    ''' Container for items that keeps a running sum '''
    def __init__(self):
        self.items = []
        self.sum = 0

    def append(self, item):
        self.items.append(item)
        self.sum += item

    def __str__(self):
        ''' Printable representation '''
        return 'Bin(sum=%d, items=%s)' % (self.sum, str(self.items))


def pack(values, maxValue):
    values = sorted(values, reverse=True)
    #print str(values)
    bins = []

    for item in values:
        # Try to fit item into a bin
        for bin in bins:
            if bin.sum + item <= maxValue:
                #print 'Adding', item, 'to', bin
                bin.append(item)
                break
        else:
            # item didn't fit into any bin, start a new bin
            #print 'Making new bin for', item
            bin = Bin()
            bin.append(item)
            bins.append(bin)

    return bins


#TODO: need to have VM object separately and compute mapping from bins to VM
#FIXME: we add the migration time to the SS for which the migration is done. (prepare SS phase)

if __name__ == '__main__':
    #import random

    #current_milli_time = lambda: int(round(time.time() * 1000))

    startTime = int(round(time.time() * 1000))

    if (len(sys.argv)!=7):
        print "Usage FDD.py file_name source_partition number_of_partitions partition_size_in_MB SERIALIZATION_TIME_in_ms DESERIALIZATION_TIME_in_ms"
        print "Example:"
        print "knapsack.py test.csv 4 40 50 1324 6512"
        print "columns in test.csv PartitionID,SubgraphID,SuperStep,ComputeTime"
        quit()

    vmCoreMins={}

    df = pd.DataFrame(columns=('Superstep', 'ActiveVM', 'MAX_TIME' ,'SUM_TIME','Total_TIME'))

    source_partition=int(sys.argv[2])

    input_csv=sys.argv[1]


    number_of_partitions=int(sys.argv[3])

    PARTITION_SIZE=float(sys.argv[4])


    SERIALIZATION_TIME=float(sys.argv[5])

    DESERIALIZATION_TIME=float(sys.argv[6])

    #TODO: maintain a map to store the Supertep timings

    Superstep_time_map={}

    Superstep_activeVM_map={}

    Physical_VM_Map={} #this map contains mapping of VM->partitions assigned to it. NUmber of keys will denote the number of VMs we have used till now.

    partition_to_PhysicalVM_map={}

    next_VMID_to_use=0

    for i in range(0,number_of_partitions+1):
        partition_to_PhysicalVM_map[i]=-1


    Physical_VM_SS_active_map={}##map gives a given VM(key)--> is active in which SS(value)
    Physical_VM_migration_active_map={}##VM->SS will indicate supersteps in which VMs need to send partitions
    SS_migration_cost={} ##stores the migration cost for the SS

     #MB
    BANDWIDTH=60.0 #MB/s

    ############################# NEW METRICS ####################################
    sstime_with_migration={}

    makespan_with_migration=0 ## add the default SS time + migration cost

    core_seconds_with_migration=0

    core_mins_with_migration=0

    Physical_VM_CoreMin_map={}

    Physical_VM_CoreSec_map={}

    max_partition_vm_list=0
    ##################READ input for first superstep #####################
    maxTime=0
    f = open(input_csv)
    csv_f = csv.reader(f)
    for row in csv_f:
        # print row[2]
        if int(row[2]) == 1 and int(row[0]) == source_partition :
            maxTime+=int(row[3])

    f.close()
    ####################Computation for first superstep###############################
    #vmCoreMins[1]=maxTime

    Superstep_activeVM_map[1]=int(1)


    Superstep_time_map[int(1)]=maxTime #FIXME: after a given superstep finishes, we add the consequent migration time to the next SS

    df = df.T
    df[1]=[int(1),int(1),int(maxTime),int(maxTime),int(0)]
                    #df.append(superstep,vmid,partSum,maxCost)
    df = df.T

    print df

    sstime_with_migration[1]=maxTime

    makespan_with_migration=makespan_with_migration+maxTime
    Physical_VM_Map[next_VMID_to_use]=[source_partition] #Assigned source partition to VM 1
    partition_to_PhysicalVM_map[source_partition]=next_VMID_to_use

    Physical_VM_SS_active_map[next_VMID_to_use]=[1]#value is list of superstep

    next_VMID_to_use+=1
    print Physical_VM_Map



    # exit()


    ####################Loop until done with all supersteps####################
    partTime={}

    superstep=2
    flag=1
    ##################Read the input data####################
    while flag ==1:
        flag=0
        f = open(sys.argv[1])
        csv_f = csv.reader(f)
        for row in csv_f:
            if int(row[2]) == superstep:   ##check if atleast one partition is active
                     flag=1
                     if int(row[0]) in partTime:
                        # print partTime[int(row[0])] +" " +row[0]
                         initial=partTime[int(row[0])]
                         partTime[int(row[0])] =int(initial)  + int(row[3])   ##this is because a given partition can have multiuple subgraphs
                        # print partTime[int(row[0])] +" " +row[0] +" "+row[3]
                     else:
                        partTime[int(row[0])] = row[3]

        #inv_map = {v: k for k, v in partTime.items()}
        if(flag==1):

            print "===================Superstep"+str(superstep)+"================"

            maxTime=0
            partSum=0
            SStimeList=[]

            # print partTime

            for k in partTime.keys():
                SStimeList.append(int(partTime[k]))
                partSum=partSum+int(partTime[k])
                if maxTime<int(partTime[k]):
                    maxTime=int(partTime[k])

            ############Sort the partitions based on compute timings#####################
            SStimeList.sort()


            # print "maxtime is:" +str(maxTime)

            # print SStimeList
            ####################Call the bin_packing algo######################
            bins = pack(SStimeList, int(maxTime))

            #TODO: Compute the mapping of the bins to the active VMs
            #for each bin form an ordered list indicating cost (set difference)
            #no of lists: number of bins
            #no of entries == number of keys in Physical_VM_Map

            logical_bin={} #bin_number-->list of partition

            logical_bin_to_PhysicalVM_mapping={}

            # print 'Solution using', len(bins), 'bins:'

            bin_number=-1
            for bin in bins:
                # print bin
                bin_number=bin_number+1
                l=[]
                for item in bin.items:
                    for p in partTime.keys():
                        if int(partTime[p])==item:
                            # print p
                            l.append(p)

                logical_bin[bin_number]=l

            print "partTime",partTime

            print "bins by FFD"
            print logical_bin


            print "Physical VM map"
            print Physical_VM_Map

            ####cost matrix formation
            ##cost here is computed as bin-Vm as this gives us the number of partitions to be migrated
            cost_matrix=[]

            for bin in logical_bin:
                l=[]
                for vm in Physical_VM_Map.keys():

                    # print set(bin.items)-set(Physical_VM_Map[vm])
                    # l.append(len(set(bin.items)-set(Physical_VM_Map[vm])))
                    l.append(len(set(logical_bin[bin])-set(Physical_VM_Map[vm])))

                cost_matrix.append(l)

            print "cost matrix"
            print cost_matrix

            m=  Munkres()


            indexes = m.compute(cost_matrix)
            total = 0
            for row, column in indexes:
                value = cost_matrix[row][column]
                total += value
                # print '(%d, %d) -> %d' % (row, column, value)#(bin,vm)-->cost
                logical_bin_to_PhysicalVM_mapping[row]=column
                #####update the Physical_VM_SS_active_map
                l=Physical_VM_SS_active_map[column]
                l.append(superstep)
                Physical_VM_SS_active_map[column]=l

            # print 'total cost: %d' % total

            print "logical_bin_to_PhysicalVM_mapping"
            print logical_bin_to_PhysicalVM_mapping

            ##FIXME:spwan new VM in case all bins are not mapped and update the Physical_VM_SS_active_map

            if(len(logical_bin_to_PhysicalVM_mapping.keys()) != len(bins)):

                for unassigned_bin in (set(logical_bin.keys())-set(logical_bin_to_PhysicalVM_mapping.keys())):

                    # print unassigned_bin
                    #
                    # print next_VMID_to_use

                    logical_bin_to_PhysicalVM_mapping[unassigned_bin]=next_VMID_to_use

                    Physical_VM_Map[next_VMID_to_use]=[]

                    Physical_VM_SS_active_map[next_VMID_to_use]=[superstep]

                    next_VMID_to_use=next_VMID_to_use+1




            # print logical_bin_to_PhysicalVM_mapping

            #TODO: compute which VM need to send which partition to which VM (dependency set)
            #TODO: compute maximum migration to/from VM
            #TODO: compute new mapping PID-> VM & VM->PID

            VM_partition_send_map={}

            VM_partition_receive_map={}

            for i in range(0,next_VMID_to_use):
                VM_partition_receive_map[i]=set()
                VM_partition_send_map[i]=set()


            for bin in logical_bin.keys():

                #get the VM to which it is mapped
                mapped_vm=logical_bin_to_PhysicalVM_mapping[bin]

                available_partition_on_vm=set(Physical_VM_Map[mapped_vm])
                # print logical_bin[bin]
                for partition in logical_bin[bin]:

                    if(partition in available_partition_on_vm):
                        continue
                    else:
                        if(partition_to_PhysicalVM_map[partition]!= -1): #FIXME: this ensure that partitions are preloaded for first use
                            VM_partition_receive_map[mapped_vm].add(partition)
                            VM_partition_send_map[partition_to_PhysicalVM_map[partition]].add(partition)





            print "send map"
            print VM_partition_send_map
            ##update the Physical_VM_migration_active_map
            for vm in VM_partition_send_map.keys():

                if (len(VM_partition_send_map[vm]) > 0) :

                    if(vm in Physical_VM_migration_active_map.keys()):
                        l=Physical_VM_migration_active_map[vm]
                        l.append(superstep)
                        Physical_VM_migration_active_map[vm]=l

                    else:
                        Physical_VM_migration_active_map[vm]=[superstep]


            print "receive map"
            print VM_partition_receive_map

            ################## determine the migration cost #################################
            #based on the max (send+receive for a given VM)
            max_send_receive_partition_count_for_vm=0

            for vm in VM_partition_send_map.keys():

                if((len(VM_partition_send_map[vm]) ) > max_send_receive_partition_count_for_vm):

                    max_send_receive_partition_count_for_vm=(len(VM_partition_send_map[vm]))

                if(len(VM_partition_receive_map[vm]) > max_send_receive_partition_count_for_vm):

                    max_send_receive_partition_count_for_vm=len(VM_partition_receive_map[vm])

            ## in milliseconds

            print "max_send_receive_partition_count_for_vm" +str(max_send_receive_partition_count_for_vm)
            if(max_send_receive_partition_count_for_vm==0):
                migration_cost=0
            else:
                migration_cost=(((max_send_receive_partition_count_for_vm*PARTITION_SIZE)/BANDWIDTH) *1000)+SERIALIZATION_TIME+DESERIALIZATION_TIME

            SS_migration_cost[superstep]=migration_cost
            ###################################################################################
            ####update the partition->vm map and vm->partition map

            for bin in logical_bin.keys():

                #get the VM to which it is mapped
                mapped_vm=logical_bin_to_PhysicalVM_mapping[bin]

                print " bin "+str(bin)+" mapped to "+str(mapped_vm)

                # available_partition_on_vm=set(Physical_VM_Map[mapped_vm])
                # print logical_bin[bin]
                for partition in logical_bin[bin]:

                    # print "processing partition "+str(partition)
                    #remove from the earlier VM and map to new VM
                    old_vm=partition_to_PhysicalVM_map[partition]

                    # print "old vm "+str(old_vm)
                    if(old_vm!=-1):

                        l_old=Physical_VM_Map[old_vm]
                        # print "l_old "+str(l_old)
                        l_old.remove(partition)
                        Physical_VM_Map[old_vm]=l_old

                    l_new=Physical_VM_Map[mapped_vm]
                    l_new.append(partition)
                    Physical_VM_Map[mapped_vm]=l_new

                    partition_to_PhysicalVM_map[partition]=mapped_vm


            # print VM_partition_receive_map


            ##TODO: after migration update the Physical_VM_Map



            # exit()

            #TODO:Assign the vmCoreMin at the end of algorithm
            Superstep_time_map[int(superstep)]=maxTime #FIXME add the migration time here
            Superstep_activeVM_map[int(superstep)]=int(len(bins))
            #This is incorrect
            # for i in range(1,len(bins)+1,1):
            #     if i in vmCoreMins.keys():
            #         vmCoreMins[int(i)]+=maxTime
            #     else:
            #         vmCoreMins[int(i)]=maxTime


            df = df.T
            df[superstep]=[int(superstep),int(len(bins)),int(maxTime),int(partSum),int(0)]
                    #df.append(superstep,vmid,partSum,maxCost)
            df = df.T

            print df

            ################# NEW METRIC UPDATION #####################
            makespan_with_migration = makespan_with_migration+ maxTime +migration_cost
            sstime_with_migration[superstep]=maxTime+migration_cost

            superstep += 1

            for vm in Physical_VM_Map.keys():

                if(len(Physical_VM_Map[vm]) > max_partition_vm_list):
                    max_partition_vm_list=len(Physical_VM_Map[vm])



            partTime={}




    #########################Post superstep calculations################
    total_supersteps=superstep-1

    print "superstep Count "+str(total_supersteps)

    print "Physical_VM_SS_active_map"
    print Physical_VM_SS_active_map

    print "Physical_VM_migration_active_map"
    print Physical_VM_migration_active_map

    print "SS_migration_cost"
    print SS_migration_cost

    print "makespan_with_migration"
    print makespan_with_migration

    print "sstime_with_migration"
    print sstime_with_migration
    #TODO: compute the activation for physical VMs using cost function

    ###########NEW METRIC COMPUTATION ########################################

    #core_seconds_with_migration  ##for each vm get seconds in active SS + time when it is active only for migration

    for vm in Physical_VM_SS_active_map:

        vm_min=0
        vm_msec=0

        current_vm_msec=0
        if(vm in Physical_VM_migration_active_map.keys()):
            pass
        else:
            Physical_VM_migration_active_map[vm]=[]



        # vmTime=0

        active_list_for_vm=Physical_VM_SS_active_map[vm]


                #to avoid exception in condition check ss in vm_migration_ss_map[vm]

        flag=0 ##vm not started

        #TODO: update billing at end of loop

        for ss in range(1,total_supersteps+1):

            if (ss in active_list_for_vm):##case when vm is active

                current_vm_msec= current_vm_msec + sstime_with_migration[ss]
                if(flag==0):
                    flag=1

            elif(ss in Physical_VM_migration_active_map[vm] ):#case when migration is required

                if(math.ceil(current_vm_msec/60000.0)==math.ceil((current_vm_msec+sstime_with_migration[ss])/60000.0)):

                    current_vm_msec+=sstime_with_migration[ss]

                    flag=1

                else:
                    current_vm_msec+=SS_migration_cost[ss]
                    flag=0
                    vm_min+=math.ceil(current_vm_msec / 60000.0)
                    vm_msec+=current_vm_msec
                    current_vm_msec=0

            else:

                if(math.ceil(current_vm_msec/60000.0)==math.ceil((current_vm_msec+sstime_with_migration[ss])/60000.0)):#no active partition and no migration required

                    current_vm_msec+=sstime_with_migration[ss]

                    flag=1

                else:

                    flag=0
                    vm_min+=math.ceil(current_vm_msec / 60000.0)
                    vm_msec+=current_vm_msec
                    current_vm_msec=0

        vm_msec+=current_vm_msec
        vm_min+=math.ceil(current_vm_msec / 60000.0)

        Physical_VM_CoreMin_map[vm]=vm_min
        Physical_VM_CoreSec_map[vm]=vm_msec

#########################################################################
    print "VM CoreMin"
    print Physical_VM_CoreMin_map

    print "VM CoreSec"
    print Physical_VM_CoreSec_map


    print "total core_Min"
    print sum(Physical_VM_CoreMin_map.values())
    core_min=sum(Physical_VM_CoreMin_map.values())

    print "total core_sec"
    print sum(Physical_VM_CoreSec_map.values())
    core_sec=sum(Physical_VM_CoreSec_map.values())/1000.0













    #########calculate makespan##############
    # print df
    makespan=0
    # print df.Superstep.count()
    for i in range(1,df.Superstep.count()+1):
        if i>1:
            df.Total_TIME[i]=df.SUM_TIME[i]+df.Total_TIME[i-1]
            makespan+=df.MAX_TIME[i]
        else:
            df.Total_TIME[i]=df.SUM_TIME[i]
            makespan+=df.MAX_TIME[i]
    print df

    # plot=df.plot(x='Superstep', y='ActiveVM', kind='bar')
    # fig = plot.get_figure()
    # filename="FFD-ActiveVM-"+sys.argv[1]+".png"
    # fig.savefig(filename)
    #
    # plt.close()
    # print "makespan is "+str(makespan)

    # df['Util'] = (df.SUM_TIME/ ( df.ActiveVM * df.MAX_TIME)).T

    # df['DefaultUtil'] = ((df.SUM_TIME/ ( number_of_partitions * df.MAX_TIME))*100).T

    # plot1=df.plot(x='Total_TIME',y= 'Util',kind='line')
    #
    # fig1 = plot1.get_figure()
    # filename1="FFD-Util-"+sys.argv[1]+".png"
    # fig1.savefig(filename1)
    #
    # plt.close()

    # plot4=df.plot(x='Superstep',y= 'DefaultUtil',kind='bar')
    #
    #
    # matplotlib.rcParams.update({'font.size': 20})
    #
    #
    # axes = plt.gca()
    #
    # print df['DefaultUtil']
    # axes.legend_.remove()
    # fig4 = plot4.get_figure()
    #
    # #fig4.set_size_inches(30.5, 22.5)
    # axes.set_ylim([0,100.0])
    #
    # axes.yaxis.grid()
    # plot4.set_xlabel("Superstep", fontsize=25)
    # plot4.set_ylabel("Utilization",fontsize=25)
    # filename4="Default-Util-"+sys.argv[1]+".png"
    # # fig4.savefig(filename4)
    # # plt.show()
    # plt.close()


    df['UnderUtil'] = ( ( df.ActiveVM * df.MAX_TIME) - df.SUM_TIME).T

    df['DefaultUnderUtil'] = ( ( number_of_partitions * df.MAX_TIME) - df.SUM_TIME).T

    underutil=0
    defaultUnderUtil=0

    for i in range(1,df.Superstep.count()+1):

        underutil+=df.UnderUtil[i]
        defaultUnderUtil+=df.DefaultUnderUtil[i]


    #df['UnderUtil'] = ( ( df.ActiveVM * df.MAX_TIME) - df.SUM_TIME).T
    # print df
    #
    for i in range(1,df.Superstep.count()+1):

        df.UnderUtil[i]=math.ceil(df.UnderUtil[i]/60000.0)
        df.DefaultUnderUtil[i]=math.ceil(df.DefaultUnderUtil[i]/60000.0)

    # plot2=df.plot(x='Superstep', y='UnderUtil', kind='bar')
    # fig2 = plot2.get_figure()
    # filename2="FFD-UnderUtil-"+sys.argv[1]+".png"
    # fig2.savefig(filename2)
    #
    # plt.close()
    # #
    # #
    # plot3=df.plot(x='Superstep', y='DefaultUnderUtil', kind='bar')
    # fig3 = plot3.get_figure()
    # filename3="default-UnderUtil-"+sys.argv[1]+".png"
    # fig3.savefig(filename3)
    #
    # plt.close()
    #
    #
    #
    df['VMCoreMilliSec'] = ( ( df.ActiveVM * df.MAX_TIME) ).T
    #
    # print df

    vmCoreMilliSec=0
    for i in range(1,df.Superstep.count()+1):
        vmCoreMilliSec+=df.VMCoreMilliSec[i]



    # print vmCoreMins

    # print sum(vmCoreMins.values())
    for i in range(1,len(vmCoreMins)+1,1):
        vmCoreMins[i]=math.ceil(vmCoreMins[i]/60000.0)

    # print vmCoreMins

    # print sum(vmCoreMins.values())

    # print makespan

    ############call to the cost function ###################
    vmMins=calcCoreMin(Superstep_activeVM_map,Superstep_time_map)

    ################print the final result set#############
    # print "Superstep Active VM map is "+str(Superstep_activeVM_map)

    # print "Superstep time map  "+str(Superstep_time_map)

    # print "vmCoreMin using cost function : "+ str(vmMins)
    # print "makespan : "+  str(makespan)


    # print "Supersteps "+str(df.Superstep.count()) +" underUtil value "+str(underutil) +" default underutil value "+str(defaultUnderUtil)

    # print "vmcoreMilliSec are "+str(vmCoreMilliSec)

    # df['CoreMinBalanced']=( ( df.ActiveVM * df.MAX_TIME)).T
    #
    # df['CoreMinDefault']=( ( 40 * df.MAX_TIME)).T
    #
    #
    # for i in range(1,df.Superstep.count()+1):
    #     df.CoreMinBalanced[i]=math.ceil(df.CoreMinBalanced[i]/60000)
    #     df.CoreMinDefault[i]=math.ceil(df.CoreMinDefault[i]/60000)
    # print df
    #
    #
    # df2 = pd.DataFrame(columns=('Superstep','CoreMinBalanced','CoreMinDefault'))
    # df2=df[['Superstep','CoreMinBalanced','CoreMinDefault']]
    #
    # print df2
    endTime = int(round(time.time() * 1000))

    # print "running time in ms "+str(endTime-startTime)

    print "FFD,Makespan,"+str(makespan/1000.0)+",Core-Mins,"+str(vmMins)+",Core-Secs,"+str(vmCoreMilliSec/1000.0)+",UnderUtilization,"+str(math.ceil(underutil/60000.0))

    print "Default,Makespan,"+str(makespan/1000.0)+",Core-Mins,"+str((math.ceil(makespan/60000.0))*number_of_partitions)+",Core-Secs,"+str(makespan*number_of_partitions/1000.0)+",UnderUtilization,"+str(math.ceil(defaultUnderUtil/60000.0))

    ####first line for default then FFD and last for FFDwithMigration

    print str(makespan/1000.0)+","+str((math.ceil(makespan/60000.0))*number_of_partitions)+","+str(makespan*number_of_partitions/1000.0)

    print str(makespan/1000.0)+","+str(vmMins)+","+str(vmCoreMilliSec/1000.0)

    print str(makespan_with_migration/1000.0)+","+str(core_min)+","+str(core_sec)

    print max_partition_vm_list