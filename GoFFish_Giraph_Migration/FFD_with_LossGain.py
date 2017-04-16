
# Loss Gain Approach :
#
# Superstep (i)
#
# Active partition set :  Pi
# Number of active VM : n
#
#
# Superstep (i+1):
#
# Run FFD
# 	FFD(Pi+1)==> M(i+1) : P(i+1)-> m   //packing
#
#        2.  Calculate the cost for mapping using hungarian algo (compute + migration)
# 	       if	(Cost(Placement(Mi+1, Mi) <=120)
# 			Use this mapping
# 	       Else:
# Loss Gain
#
#      3.  (Else part) Find the VM causing bottleneck for the VM
#
# 		Vmax =(Vin, Vout)
#
#      4.  For each partition in M(i+1) ( Vmax )
#
# 		Compute the score for the partition
#
# 		Cost! = |P| /|B| + ( T(src +partition) - Tmax)
#
#     5. Do not move the partition with max score and compute the cost from eqn 2
#
# 	Else
# 		Increase the number of VM
# Run the FFD with given fixed number of VM
# Hoping we get more space of data movement cost
#
# If the increase in number of VM doesn't help go with same mapping


import csv
import sys
import os
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import math
import time
from munkres import Munkres, print_matrix
from sys import maxint
#########################################################################
######################FFD Implementation##############################

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
#################################################################################
#helper functions

#function to get max send/receive partition count
#argument

def max_migration_partition_count(VM_partition_send_map, VM_partition_receive_map):

    max_send_receive_partition_count_for_vm=0

    for vm in VM_partition_send_map.keys():

        if( ((len(VM_partition_send_map[vm]) ) ) > max_send_receive_partition_count_for_vm ):

            max_send_receive_partition_count_for_vm=((len(VM_partition_send_map[vm]) ))
            bottleneck_vmid=vm
            send_bottleneck_flag=1

    for vm in VM_partition_receive_map.keys():

        if( ( len(VM_partition_receive_map[vm])) > max_send_receive_partition_count_for_vm ):

            max_send_receive_partition_count_for_vm=( len(VM_partition_receive_map[vm]))
            bottleneck_vmid=vm
            send_bottleneck_flag=0
    




###################################################################################

if __name__ == '__main__':


    ##### input parsing #################################################
    startTime = int(round(time.time() * 1000))

    if (len(sys.argv)!=5):
        print "Usage FDD_with_LossGain.py file_name source_partition number_of_partitions constraint_val"
        print "Example:"
        print "FDD_with_LossGain.py test.csv 4 40 20"
        print "columns in test.csv PartitionID,SubgraphID,SuperStep,ComputeTime"
        quit()

    vmCoreMins={}

    df = pd.DataFrame(columns=('Superstep', 'ActiveVM', 'MAX_TIME' ,'SUM_TIME','Total_TIME'))

    source_partition=int(sys.argv[2])

    input_csv=sys.argv[1]


    number_of_partitions=int(sys.argv[3])

    CONSTRAINT_VALUE=int(sys.argv[4])

    ######################### METRICS+ DS TO BE USED #######################

    Superstep_time_map={}

    Superstep_activeVM_map={}

    PhysicalVM_Partition_Map={} #this map contains mapping of VM->partitions assigned to it. NUmber of keys will denote the number of VMs we have used till now.

    Partition_PhysicalVM_Map={}

    next_VMID_to_use=0

    for i in range(0,number_of_partitions+1):
        Partition_PhysicalVM_Map[i]=-1


    Physical_VM_SS_active_map={}##map gives a given VM(key)--> is active in which SS(value)
    Physical_VM_migration_active_map={}##VM->SS will indicate supersteps in which VMs need to send partitions
    SS_migration_cost={} ##stores the migration cost for the SS

    PARTITION_SIZE=float(50.0) #MB
    BANDWIDTH=float(60.0) #MB/s

    sstime_with_migration={}

    makespan_with_migration=0 ## add the default SS time + migration cost

    core_seconds_with_migration=0

    core_mins_with_migration=0

    Physical_VM_CoreMin_map={}

    Physical_VM_CoreSec_map={}

    ############################################################################

######################## Superstep  Execution ############################################

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
    PhysicalVM_Partition_Map[next_VMID_to_use]=[source_partition] #Assigned source partition to VM 1
    Partition_PhysicalVM_Map[source_partition]=next_VMID_to_use

    Physical_VM_SS_active_map[next_VMID_to_use]=[1]#value is list of superstep

    next_VMID_to_use=next_VMID_to_use+1
    print PhysicalVM_Partition_Map


    ################# From Superstep 2 onwards ######################################

    partTime={}
    superstep=2
    flag=1
    ##################Read the input data####################
    while flag ==1:

        partTime.clear()

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
                        partTime[int(row[0])] = int(row[3])

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

            print "bins by FFD"
            print logical_bin


            print "Physical VM map"
            print PhysicalVM_Partition_Map

            ####cost matrix formation
            ##cost here is computed as bin-Vm as this gives us the number of partitions to be migrated
            cost_matrix=[]

            for bin in logical_bin:
                l=[]
                for vm in PhysicalVM_Partition_Map.keys():

                    # print set(bin.items)-set(Physical_VM_Map[vm])
                    # l.append(len(set(bin.items)-set(Physical_VM_Map[vm])))
                    l.append(len(set(logical_bin[bin])-set(PhysicalVM_Partition_Map[vm])))

                cost_matrix.append(l)

            # print "cost matrix"
            # print cost_matrix

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
            #FIXME: we are not updating the partiton_to_physicalVM map here as we need to compute the send & receive map
            #FIXME: we have to compute the vm_ActivePartition_time based on logical bin to physical vm map and not based on Partition_PhysicalVM_Map

            if(len(logical_bin_to_PhysicalVM_mapping.keys()) != len(bins)):

                for unassigned_bin in (set(logical_bin.keys())-set(logical_bin_to_PhysicalVM_mapping.keys())):

                    logical_bin_to_PhysicalVM_mapping[unassigned_bin]=next_VMID_to_use

                    PhysicalVM_Partition_Map[next_VMID_to_use]=[]

                    Physical_VM_SS_active_map[next_VMID_to_use]=[superstep]

                    next_VMID_to_use=next_VMID_to_use+1



            ##################################################################################
            ################### COPUTING SEND & RECEIVE MAP FOR EACH VM #####################

            VM_partition_send_map={}

            VM_partition_receive_map={}

            for i in range(0,next_VMID_to_use):
                VM_partition_receive_map[i]=set()
                VM_partition_send_map[i]=set()


            for bin in logical_bin.keys():

                #get the VM to which it is mapped
                mapped_vm=logical_bin_to_PhysicalVM_mapping[bin]

                available_partition_on_vm=set(PhysicalVM_Partition_Map[mapped_vm])
                # print logical_bin[bin]
                for partition in logical_bin[bin]:

                    if(partition in available_partition_on_vm):
                        continue
                    else:
                        if(Partition_PhysicalVM_Map[partition]!= -1): #FIXME: this ensure that partitions are preloaded for first use
                            VM_partition_receive_map[mapped_vm].add(partition)
                            VM_partition_send_map[Partition_PhysicalVM_Map[partition]].add(partition)
                        else:
                            print "preload partition "+str(partition)+" on vm "+str(mapped_vm)
                            #FIXME: updating the mapping for preloaded partitions
                            Partition_PhysicalVM_Map[partition]=mapped_vm
                            if(mapped_vm in PhysicalVM_Partition_Map.keys()):
                                l=PhysicalVM_Partition_Map[mapped_vm]
                                l.append(partition)
                                PhysicalVM_Partition_Map[mapped_vm]=l
                            else:
                                PhysicalVM_Partition_Map[mapped_vm]=[partition]


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


            ##################################################################################
            ################### FIND THE VM CAUSING THE MIGRATION BOTTLENECK #####################

            #based on the max (send/receive for a given VM) ##TODO: verify whether we have duplex channel b/w : Rigel has full duplex channels "dmesg | grep -i duplex"
            max_send_receive_partition_count_for_vm=0
            bottleneck_vmid=-1
            send_bottleneck_flag=0  #1-send is bottleneck 0-receive is bottleneck

            for vm in VM_partition_send_map.keys():

                if( ((len(VM_partition_send_map[vm]) ) ) > max_send_receive_partition_count_for_vm ):

                    max_send_receive_partition_count_for_vm=((len(VM_partition_send_map[vm]) ))
                    bottleneck_vmid=vm
                    send_bottleneck_flag=1

            for vm in VM_partition_receive_map.keys():

                if( ( len(VM_partition_receive_map[vm])) > max_send_receive_partition_count_for_vm ):

                    max_send_receive_partition_count_for_vm=( len(VM_partition_receive_map[vm]))
                    bottleneck_vmid=vm
                    send_bottleneck_flag=0


            print "max_send_receive_partition_count_for_vm" +str(max_send_receive_partition_count_for_vm)
            migration_cost=((max_send_receive_partition_count_for_vm*PARTITION_SIZE)/BANDWIDTH) *1000

            ###################################################################################
            ############### get compute time summation for all partitions in the VM ##################################
            #FIXME: this should be computed based on bin mapping and not on Partition_PhysicalVM_Map

            vm_ActivePartition_time={}#key->VM value->sum of active partition compute time

            print "logical bin "
            print logical_bin

            for b in logical_bin.keys():

                for p in logical_bin[b]:

                    v = logical_bin_to_PhysicalVM_mapping[b]

                    if (v in vm_ActivePartition_time.keys()):

                        vm_ActivePartition_time[v]+=int(partTime[p])

                    else:
                        # print str(type(partTime[active_partition])) +" , "+ str(partTime[active_partition])

                        vm_ActivePartition_time[v]=int(partTime[p])


            ###################################################################################
            ############### check for violation of constraint ##################################

            constraint_violated_vm=[]

            UPPER_LIMIT=int(maxTime + (maxTime*(CONSTRAINT_VALUE/100.0)))

            print "UPPER_LIMIT "+str(UPPER_LIMIT)
            print "maxTime " +str(maxTime)
            print "migration_cost " +str(migration_cost)
            print "total_cost " +str(migration_cost+maxTime)

            if (migration_cost + maxTime <= UPPER_LIMIT):
                print "***************constraint not violated continue with FFD output*******************"

                #TODO: update the mapping of part->vm and vm->part + superstep increment

            ####update the partition->vm map and vm->partition map

                print "vm_ActivePartition_time"
                print vm_ActivePartition_time

                print "maxTime"
                print maxTime

                for bin in logical_bin.keys():

                    #get the VM to which it is mapped
                    mapped_vm=logical_bin_to_PhysicalVM_mapping[bin]

                    # print " bin "+str(bin)+" mapped to "+str(mapped_vm)

                    # available_partition_on_vm=set(Physical_VM_Map[mapped_vm])
                    # print logical_bin[bin]
                    for partition in logical_bin[bin]:

                        # print "processing partition "+str(partition)
                        #remove from the earlier VM and map to new VM
                        old_vm=Partition_PhysicalVM_Map[partition]

                        # print "old vm "+str(old_vm)
                        if(old_vm!=-1):

                            l_old=PhysicalVM_Partition_Map[old_vm]
                            # print "l_old "+str(l_old)
                            l_old.remove(partition)
                            PhysicalVM_Partition_Map[old_vm]=l_old

                        l_new=PhysicalVM_Partition_Map[mapped_vm]
                        l_new.append(partition)
                        PhysicalVM_Partition_Map[mapped_vm]=l_new

                        Partition_PhysicalVM_Map[partition]=mapped_vm


                superstep+=1

            else:
                print "****************constraint violated use loss gain approach*******************************"

                ############### LOSS GAIN APPROACH ############################################

                ##### calculate the score for each active partition in the  bottleneck VM

                #get the bin corresponding to the bottleneck_vm
                bottleneck_bin=-1 ##bin corresponding to the bottleneck VM

                for bin in logical_bin.keys():

                    if(logical_bin_to_PhysicalVM_mapping[bin]==bottleneck_vmid):

                        bottleneck_bin=bin
                        break

                partition_score={} ## key->partition value->score
                partition_to_compute_score=[] # partitions for which we need to compute the score (those are involved in migration)


                for p in logical_bin[bottleneck_bin]:

                    print "partition,"+str(p)+",prev_vmID,"+str(Partition_PhysicalVM_Map[p])+",mapped_to,"+str(bottleneck_vmid)
                    if(Partition_PhysicalVM_Map[p]==bottleneck_vmid):
                        pass #not involved in migration
                    else:
                        partition_to_compute_score.append(p)


                for p in VM_partition_send_map[bottleneck_vmid]:
                    print "need to send "+str(p)


                for p in VM_partition_receive_map[bottleneck_vmid]:
                    print "need to receive "+str(p)


                #TODO : compute the score for each partition involved in migration
                # 		Cost! = |P| /|B| + ( T(src +partition) - Tmax)

                print "partTime"
                print partTime

                print "vm_ActivePartition_time"
                print vm_ActivePartition_time

                print "logical_bin_to_PhysicalVM_mapping"
                print logical_bin_to_PhysicalVM_mapping
                #
                # print len(vm_ActivePartition_time.keys())
                # print len(logical_bin_to_PhysicalVM_mapping.keys())

                print "maxTime"
                print maxTime

                print "send_bottleneck_flag"
                print send_bottleneck_flag

                max_score_pid=-1
                max_score=-maxint-1

                if(send_bottleneck_flag):

                    for p_id in partition_to_compute_score:

                        if(p_id in VM_partition_send_map[bottleneck_vmid] ):

                            # Cost! = |P| /|B| + ( T(src +partition) - Tmax)

                            partition_score[p_id]=( ((PARTITION_SIZE/BANDWIDTH)*1000) -( (vm_ActivePartition_time[bottleneck_vmid]+partTime[p_id]) - maxTime) )
                            if(partition_score[p_id] >max_score):
                                max_score_pid=p_id

                    #TODO: get max score and check for constraint

                else: #TODO: handle the case where no migration causes spinning up a vm

                    for p_id in partition_to_compute_score:



                        if(p_id in VM_partition_receive_map[bottleneck_vmid] ):

                            #get the vm where the partition is residing before migration
                            sender_vm_id=Partition_PhysicalVM_Map[p_id]

                            #FIXME:compute the score only in case when sender_vm is running in this superstep
                            if(sender_vm_id in logical_bin_to_PhysicalVM_mapping.values()):
                                partition_score[p_id]=( ((PARTITION_SIZE/BANDWIDTH)*1000) -( (vm_ActivePartition_time[sender_vm_id]+partTime[p_id]) - maxTime) )
                                if(partition_score[p_id] >max_score):
                                    max_score_pid=p_id

                            else:#TODO: consider running this VM first
                                print "on not migrating partititon "+str(p_id)+" we have to keep running vm "+str(sender_vm_id)



                print partition_score

                # print logical_bin
                #TODO: get max score and check for constraint

                receiver_vm_id =-1
                sender_vm=-1

                if(send_bottleneck_flag):
                    #TODO: get the vm where pid is going to be hosted in current superstep decrement its runtime and increment sender vms runtime and check for constraint
                    for b in logical_bin:
                        if(max_score_pid in logical_bin[b]):
                            receiver_vm_id=logical_bin_to_PhysicalVM_mapping[b]
                            break

                    if(receiver_vm_id==-1):
                        print "receiver vm doe not exists"
                        exit()

                    vm_ActivePartition_time[receiver_vm_id]-=partTime[max_score_pid]
                    vm_ActivePartition_time[bottleneck_vmid]+=partTime[max_score_pid]

                    send_list=VM_partition_send_map[bottleneck_vmid]
                    send_list.remove(max_score_pid)
                    VM_partition_send_map[bottleneck_vmid]=send_list

                    receiver_list=VM_partition_receive_map[receiver_vm_id]
                    receiver_list.remove(max_score_pid)
                    VM_partition_receive_map[receiver_vm_id]=receiver_list

                else:

                    for v in PhysicalVM_Partition_Map.keys():

                        if(max_score_pid in PhysicalVM_Partition_Map[v]):
                            sender_vm=v

                    if(sender_vm==-1):
                        print "sender vm does not exist"
                        exit()


                    vm_ActivePartition_time[sender_vm]+= partTime[max_score_pid]
                    vm_ActivePartition_time[bottleneck_vmid]-=partTime[max_score_pid]

                    send_list=VM_partition_send_map[sender_vm]
                    send_list.remove(max_score_pid)
                    VM_partition_send_map[sender_vm]=send_list

                    receiver_list=VM_partition_receive_map[bottleneck_vmid]
                    receiver_list.remove(max_score_pid)
                    VM_partition_receive_map[bottleneck_vmid]=receiver_list


                #TODO: update the send receive map and get migration cost + max running time of a vm
                max_compute_time=max(vm_ActivePartition_time.values())

                print max_compute_time

                print VM_partition_send_map

                print VM_partition_receive_map


                max_migration_time=-1
                if(max(len(VM_partition_receive_map.values())) > max(len(VM_partition_send_map.values()))):
                    max_migration_time= (len(VM_partition_receive_map.values())*PARTITION_SIZE/BANDWIDTH)*1000
                else:
                    max_migration_time= (len(VM_partition_send_map.values())*PARTITION_SIZE/BANDWIDTH)*1000

                #constrint check:

                if((max_migration_time+max_compute_time) <= UPPER_LIMIT):

                    print "constrint satisfied"

                else:
                    print "constrint not  satisfied"

                #else
                #vm++

                exit()
                ## else vm++














