from goto import with_goto
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
import operator
import LossGainHelperFunctions as hf

'''
In this approach we get one additional parameter Umax, while we call the constraint value as Umin.

We try to map partitions to VMs s.t. Umin is satisfied using (FFD_LossGain_VMIncreament) approach.

If satisfied:
    superstep++
else:
    while(constraint is not satisfied )

        increase the threshould by delta

        run FFD_LossGain_VMIncreament

        if(constraint satisfied)
            superstep++
            break

        else if (threshold > Umax)
            exit
'''
if __name__ == '__main__':

    ##### input parsing #################################################
    startTime = int(round(time.time() * 1000))

    if (len(sys.argv)!=10):
        print "Usage FDD_with_LossGain.py file_name source_partition number_of_partitions min_constraint_val max_constraint_val DEFAULT_MAKESPAN partition_size serialization_time deserialization_time"
        print "Example:"
        print "FDD_with_LossGain.py test.csv 4 40 10 100 20000 11032 30773"
        print "columns in test.csv PartitionID,SubgraphID,SuperStep,ComputeTime"
        quit()

    vmCoreMins={}

    df = pd.DataFrame(columns=('Superstep','ActivePartitions' ,'ActiveVM','MigrationCost' ,'P_MAX','V_MAX' ,'Total_TIME'))

    source_partition=int(sys.argv[2])

    input_csv=sys.argv[1]

    number_of_partitions=int(sys.argv[3])

    MIN_CONSTRAINT_VALUE=int(sys.argv[4])

    MAX_CONSTRAINT_VALUE=int(sys.argv[5])

    DEFAULT_MAKESPAN=float(sys.argv[6])

    PARTITION_SIZE=float(sys.argv[7]) #MB

    SERIALIZATION_TIME=float(sys.argv[8])

    DESERIALIZATION_TIME=float(sys.argv[9])


    ######################### METRICS+ DS TO BE USED #######################

    Superstep_time_map={}#old metric can be used for default case

    Superstep_activeVM_map={}

    PhysicalVM_Partition_Map={} #this map contains mapping of VM->partitions assigned to it. NUmber of keys will denote the number of VMs we have used till now.

    Partition_PhysicalVM_Map={}

    next_VMID_to_use=0

    for i in range(0,number_of_partitions+1):
        Partition_PhysicalVM_Map[i]=-1


    DELTA=0.0

    CONSTRAINT_VALUE=MIN_CONSTRAINT_VALUE+DELTA

    # DELTA+=10

    vm_ss_active_map={}##map gives a given VM(key)--> is active in which SS(value)
    vm_migration_ss_map={}##VM->SS will indicate supersteps in which VMs need to send/receive partitions
    ss_migration_cost={} ##stores the migration cost for the SS


    BANDWIDTH=float(60.0) #MB/s

    sstime_with_migration={}##key:ss value: total time required for ss(max_compute + max_migration)

    makespan_with_migration=0 ##makespan of the application add the default SS time + migration cost

    core_seconds_with_migration=0 #for each ss, sum( active vm * superstep time)

    core_mins_with_migration=0 #use billing constraint i.e. per minute billing

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
    df[1]=[int(1),int(1),int(1),int(0),int(maxTime),int(maxTime),int(maxTime)]
    #(columns=('Superstep','ActivePartitions' ,'ActiveVM','MigrationCost' ,'MAX_TIME','MAX_TIME_with_binPacking' ,'Total_TIME'))
    df = df.T

    # print df

    sstime_with_migration[1]=maxTime

    makespan_with_migration+=maxTime
    PhysicalVM_Partition_Map[next_VMID_to_use]=[source_partition] #Assigned source partition to VM 1
    Partition_PhysicalVM_Map[source_partition]=next_VMID_to_use

    vm_ss_active_map[next_VMID_to_use]=[1]#value is list of supersteps in which the vm is active (for computation)

    next_VMID_to_use+=1
    # print PhysicalVM_Partition_Map


    ################# From Superstep 2 onwards ######################################

    partTime={}
    superstep=2
    flag=1

    prevSuperstep=1


    ##################Read the input data####################
    while flag ==1: #while there are more supersteps

        partTime.clear()

        if(superstep==prevSuperstep):
            DELTA+=10
        else:
            DELTA=MIN_CONSTRAINT_VALUE
            prevSuperstep=superstep


        CONSTRAINT_VALUE=DELTA

        print "CONSTRAINT_VALUE",CONSTRAINT_VALUE,"superstep",superstep

        if(CONSTRAINT_VALUE==MAX_CONSTRAINT_VALUE):
            print "ERROR can not schedule with constraint "+str(MAX_CONSTRAINT_VALUE)+" for superstep "+str(superstep)
            exit()



        flag=0
        f = open(sys.argv[1])
        csv_f = csv.reader(f)
        for row in csv_f:
            if (int(row[2]) == superstep and int(row[3]) >0):   ##check if atleast one partition is active
                     flag=1
                     if int(row[0]) in partTime:
                        # print partTime[int(row[0])] +" " +row[0]
                         initial=partTime[int(row[0])]
                         partTime[int(row[0])] =int(initial)  + int(row[3])   ##this is because a given partition can have multiuple subgraphs
                        # print partTime[int(row[0])] +" " +row[0] +" "+row[3]
                     else:
                        partTime[int(row[0])] = int(row[3])

        #inv_map = {v: k for k, v in partTime.items()}
        if(flag==1):#while there are more supersteps

            print "===================Superstep"+str(superstep)+"================"

            print "PhysicalVM_Partition_Map",PhysicalVM_Partition_Map
            print "partTime",partTime

            # x=raw_input()

            # if(superstep==8):
            #     print "partTime",partTime
            #     print "PhysicalVM_Partition_Map",PhysicalVM_Partition_Map
            #     print "Partition_PhysicalVM_Map",Partition_PhysicalVM_Map



            next_VMID_to_use_at_ss_start=next_VMID_to_use
            PhysicalVM_Partition_Map_atStart=dict(PhysicalVM_Partition_Map)
            Partition_PhysicalVM_Map_atStart=dict(Partition_PhysicalVM_Map)

            maxTime=0
            partSum=0
            SStimeList=[]



            for k in partTime.keys():
                SStimeList.append(int(partTime[k]))
                partSum=partSum+int(partTime[k])
                if maxTime<int(partTime[k]):
                    maxTime=int(partTime[k])

            UPPER_LIMIT=float(maxTime + (maxTime*(CONSTRAINT_VALUE/100.0)))

            ####################################CASE WHEN maxTime< 1% of default makespan #########################################################################
            #TODO: remove the constraint when the maxTime is <= 1% of the default makespan
            #TODO: handle the case when a partition is not mapped yet.
            if(maxTime<=((DEFAULT_MAKESPAN*1000/100.0)*1)):
                #TODO: form a bin_partition_map and bin_vm_map such that there is no migration and existing methods can be used
                bin_partition_map={}
                bin_vm_map={}

                #FIXME: this for loop will fail for partitions which are active for the first time
                for vm in PhysicalVM_Partition_Map.keys():

                    active_plist=[]

                    for p in PhysicalVM_Partition_Map[vm]:

                        if(p in partTime.keys() and partTime[p]>0):
                            active_plist.append(p)

                    if(len(active_plist)):
                        bin_partition_map[vm]=active_plist
                        bin_vm_map[vm]=vm

                # print active_plist
                # print "bin_vm_map",bin_vm_map
                # print "bin_partition_map",bin_partition_map

                vm_computetimesum_map={}

                vm_computetimesum_map=hf.get_vm_comute_time(bin_partition_map,bin_vm_map,partTime)

                result=hf.get_send_receive_map(next_VMID_to_use,bin_vm_map,bin_partition_map,Partition_PhysicalVM_Map,PhysicalVM_Partition_Map)

                vm_send_map=result[0]
                vm_receive_map=result[1]

                migration_cost=0.0


                # print "bin_vm_map",bin_vm_map
                # print "bin_partition_map",bin_partition_map


                #TODO: update the local matrix and paas the migration cost as it is not recomputed

                hf.update_metrics_at_end_of_ss(superstep,vm_ss_active_map,vm_migration_ss_map,ss_migration_cost,sstime_with_migration,makespan_with_migration,maxTime,0,Superstep_time_map,Superstep_activeVM_map,partSum,vm_computetimesum_map,bin_vm_map,bin_partition_map,vm_send_map,vm_receive_map)
                                #              (superstep,vm_ss_active_map,vm_migration_ss_map,ss_migration_cost,sstime_with_migration,makespan_with_migration,maxTime,migration_cost,Superstep_time_map,Superstep_activeVM_map,partSum,vm_computetimesum_map,bin_vm_map,bin_partition_map,vm_send_map,vm_receive_map)

                makespan_with_migration+=( max(vm_computetimesum_map.values()))


                df = df.T
                df[superstep]=[int(superstep),int(len(partTime.keys())),int(len(bin_partition_map.keys())),int(0),int(maxTime),int(max(vm_computetimesum_map.values())),int(max(vm_computetimesum_map.values()))]
                #(columns=('Superstep','ActivePartitions' ,'ActiveVM','MigrationCost' ,'MAX_TIME','MAX_TIME_with_binPacking' ,'Total_TIME'))
                df = df.T



                superstep+=1
                continue

            ########################################################################################################################################################

            ''' Preference 1 : RUN FFD '''
            print "running Preference 1 : RUN FFD"

            bin_partition_map={}

            bin_partition_map=hf.run_FFD(partTime)

            ########### get mapping using hungarian algorithm ############

            bin_vm_map={}

            result=hf.run_hungarian(bin_partition_map,PhysicalVM_Partition_Map,next_VMID_to_use)

            bin_vm_map=result[0]
            next_VMID_to_use=result[1]

            ######### migration cost computation ###########################

            #compute send and receive maps for each vm
            vm_send_map={}
            vm_receive_map={}

            result=hf.get_send_receive_map(next_VMID_to_use,bin_vm_map,bin_partition_map,Partition_PhysicalVM_Map,PhysicalVM_Partition_Map)

            vm_send_map=result[0]
            vm_receive_map=result[1]


            result=hf.get_migration_cost(vm_send_map,vm_receive_map,PARTITION_SIZE,BANDWIDTH,SERIALIZATION_TIME,DESERIALIZATION_TIME)

            send_bottleneck_flag=result[0]
            migration_cost=result[1]
            bottlneck_vmid=result[2]

            ######### get compute time summation for all partitions in the VM######

            print "bin_vm_map",bin_vm_map
            print "bin_partition_map",bin_partition_map
            print "UPPER_LIMIT",UPPER_LIMIT
            print migration_cost
            print maxTime

            vm_computetimesum_map={}

            vm_computetimesum_map=hf.get_vm_comute_time(bin_partition_map,bin_vm_map,partTime)

            ################constraint check ########################

            if(migration_cost + maxTime <= UPPER_LIMIT): ##FFD check for constraint

                print "**FFD solution satisfied the constraint**"

                ## TODO: implement a function to update metrics update: PhysicalVM_Partition_Map & Partition_PhysicalVM_Map
                hf.update_stats_at_end_of_superstep(bin_partition_map,bin_vm_map,Partition_PhysicalVM_Map,PhysicalVM_Partition_Map)

                #TODO: update the local matrix and paas the migration cost as it is not recomputed

                hf.update_metrics_at_end_of_ss(superstep,vm_ss_active_map,vm_migration_ss_map,ss_migration_cost,sstime_with_migration,makespan_with_migration,maxTime,migration_cost,Superstep_time_map,Superstep_activeVM_map,partSum,vm_computetimesum_map,bin_vm_map,bin_partition_map,vm_send_map,vm_receive_map)
                                #              (superstep,vm_ss_active_map,vm_migration_ss_map,ss_migration_cost,sstime_with_migration,makespan_with_migration,maxTime,migration_cost,Superstep_time_map,Superstep_activeVM_map,partSum,vm_computetimesum_map,bin_vm_map,bin_partition_map,vm_send_map,vm_receive_map)
                makespan_with_migration+=(migration_cost + maxTime)


                df = df.T
                df[superstep]=[int(superstep),int(len(partTime.keys())),int(len(bin_partition_map.keys())),int(migration_cost),int(maxTime),int(maxTime),int(migration_cost + maxTime)]
                #(columns=('Superstep','ActivePartitions' ,'ActiveVM','MigrationCost' ,'MAX_TIME','MAX_TIME_with_binPacking' ,'Total_TIME'))
                df = df.T



                superstep+=1
                continue


            else:##FFD violated the constraint -- switching to avoid migration approach

                ''' Preference 2: LOSS GAIN APPROACH by avoiding migration '''
                #FIXME: updates made in FFD are still valid here
                print "******************Preference 2: LOSS GAIN APPROACH by avoiding migration*************"

                #continue till no more partition with positive score is found or constrint is satisfied
                positive_score_flag=1
                vm_increment_flag=0


                #find bottleneck vmid  ..compute the score for each partition and avoid its migration
                #FIXME: computing send and receive maps should be done only once before the loop as these maps will be updated in the loop, as a result of avoiding migratin

                vm_send_map={}
                vm_receive_map={}

                result=hf.get_send_receive_map(next_VMID_to_use,bin_vm_map,bin_partition_map,Partition_PhysicalVM_Map,PhysicalVM_Partition_Map)

                vm_send_map=result[0]
                vm_receive_map=result[1]

                while(positive_score_flag):### avoid migration approach --loop until there are partitions with positive scores in the bottleneck VM

                    #FIXME: recalculating the bottleneck vm every time
                    result=hf.get_migration_cost(vm_send_map,vm_receive_map,PARTITION_SIZE,BANDWIDTH,SERIALIZATION_TIME,DESERIALIZATION_TIME)

                    send_bottleneck_flag=result[0]
                    migration_cost=result[1]
                    bottlneck_vmid=result[2]

                    ######## compute score for each partition ###############

                    partition_score={} ## key->partition value->score

                    result=hf.get_partition_score(bottlneck_vmid,bin_vm_map,bin_partition_map,Partition_PhysicalVM_Map,send_bottleneck_flag,partTime,vm_send_map,vm_receive_map,PARTITION_SIZE,BANDWIDTH)

                    partition_score=result[0]
                    max_score_pid=result[1]

                    # print "partition_score"
                    # print partition_score

                    #TODO: in case when the sender vm is dissapear we need to switch to the vm++ case or no more positive score
                    if(max_score_pid==-1 or partition_score[max_score_pid] <=0 ):
                        vm_increment_flag=1
                        positive_score_flag=0
                        # hf.plot_compute_network_pervm(vm_computetimesum_map,vm_send_map,vm_receive_map,PARTITION_SIZE,BANDWIDTH)
                        vm_increment_flag=True

                        # print" number of bins in avoid_migration approach "+str(len(bin_partition_map.keys()))
                        break #FIXME: jump to vm++ case from here


                    #### avoid the migration of max score pid and check for constraint

                    hf.avoid_migration_for_partition(max_score_pid,send_bottleneck_flag,bin_partition_map,bin_vm_map,vm_send_map,vm_receive_map,partTime,vm_computetimesum_map,bottlneck_vmid,PhysicalVM_Partition_Map)

                    max_compute_time=max(vm_computetimesum_map.values())

                    # print "max_compute_time"
                    # print max_compute_time

                    migration_count=hf.max_migration_partition_count(vm_send_map, vm_receive_map)


                    if(migration_count==0):
                        max_migration_time=0
                    else:
                        max_migration_time=((migration_count* PARTITION_SIZE/BANDWIDTH) *1000)+DESERIALIZATION_TIME+SERIALIZATION_TIME

                    ######## check for constraint #########################

                    if(max_migration_time+ max_compute_time <=UPPER_LIMIT):

                        print "LossGain : Avoid migration satisfied the constrained"

                        #TODO: update the metrics post execution of superstep
                        hf.update_stats_at_end_of_superstep(bin_partition_map,bin_vm_map,Partition_PhysicalVM_Map,PhysicalVM_Partition_Map)


                        #TODO: update the local matrix and paas the migration cost as it is not recomputed : here==> max_migration_time

                        hf.update_metrics_at_end_of_ss(superstep,vm_ss_active_map,vm_migration_ss_map,ss_migration_cost,sstime_with_migration,makespan_with_migration,maxTime,max_migration_time,Superstep_time_map,Superstep_activeVM_map,partSum,vm_computetimesum_map,bin_vm_map,bin_partition_map,vm_send_map,vm_receive_map)
                                                    #(superstep,vm_ss_active_map,vm_migration_ss_map,ss_migration_cost,sstime_with_migration,makespan_with_migration,maxTime,migration_cost,Superstep_time_map,Superstep_activeVM_map,partSum,vm_computetimesum_map,bin_vm_map,bin_partition_map,vm_send_map,vm_receive_map)

                        active_vm_count=0
                        for v in vm_computetimesum_map.keys():
                            if(vm_computetimesum_map[v]>0):
                                active_vm_count+=1


                        df = df.T
                        df[superstep]=[int(superstep),int(len(partTime.keys())),int((active_vm_count)),int(max_migration_time),int(maxTime),int(max_compute_time),int(max_migration_time+max_compute_time)]
                        #(columns=('Superstep','ActivePartitions' ,'ActiveVM','MigrationCost' ,'MAX_TIME','MAX_TIME_with_binPacking' ,'Total_TIME'))
                        df = df.T

                        makespan_with_migration+=(max_migration_time+max_compute_time)

                        superstep+=1

                        break
                    elif(positive_score_flag):
                        continue


                if(vm_increment_flag):### vm increment approach

                    ''' Preference 3 VM++ '''


                    print " *********************** using Preference 3 VM++ superstep "+str(superstep)+" *************************"

                    ### reset all parameter as at the start of the superstep
                    next_VMID_to_use=next_VMID_to_use_at_ss_start
                    PhysicalVM_Partition_Map=dict(PhysicalVM_Partition_Map_atStart)
                    Partition_PhysicalVM_Map=dict(Partition_PhysicalVM_Map_atStart)

                    # print "UPPER_LIMIT"
                    # print UPPER_LIMIT
                    #
                    # print "maxTime,"+str(maxTime)

                    while(True): ### vm increment approach, increase the number of VMs until the constraint is satisfied

                        #added this here because for partitions that are loaded for the first time are added to Partition_PhysicalVM_Map in mapping algo which can make the send receive calculation inconsistent
                        PhysicalVM_Partition_Map=dict(PhysicalVM_Partition_Map_atStart)
                        Partition_PhysicalVM_Map=dict(Partition_PhysicalVM_Map_atStart)

                        #incrementing the number of vm to be used by 1 comapred to prev run
                        number_of_vm=len(bin_partition_map.keys())+1

                        #FIXME: the numbe of vms when reaches the number of partitions the avoid migration approach should end up with no migration
                        if(number_of_vm>number_of_partitions):
                            print "in vm++ approach number of VMs passed 40 with constraint at superstep ",superstep," and constraint ",CONSTRAINT_VALUE
                            #FIXME: re-evaluate the mapping with updated constrinat
                            next_VMID_to_use=next_VMID_to_use_at_ss_start
                            PhysicalVM_Partition_Map=dict(PhysicalVM_Partition_Map_atStart)
                            Partition_PhysicalVM_Map=dict(Partition_PhysicalVM_Map_atStart)

                            break

                        next_VMID_to_use=next_VMID_to_use_at_ss_start

                        # print "number of machines to be used "+str(number_of_vm)
                        #
                        # print "partTime",partTime

                        bin_partition_map.clear()
                        bin_vm_map.clear()

                        bin_partition_map=hf.run_load_balance(partTime,number_of_vm)

                        ########### get mapping using hungarian algorithm ############

                        result=hf.run_hungarian(bin_partition_map,PhysicalVM_Partition_Map,next_VMID_to_use)

                        bin_vm_map=result[0]
                        next_VMID_to_use=result[1]


                        print "partTime",partTime
                        print "PhysicalVM_Partition_Map",PhysicalVM_Partition_Map

                        print "bin_partition_map"
                        print bin_partition_map

                        print "bin_vm_map"
                        print bin_vm_map

                        ######### migration cost computation ###########################

                        #compute send and receive maps for each vm
                        vm_send_map={}
                        vm_receive_map={}

                        result=hf.get_send_receive_map(next_VMID_to_use,bin_vm_map,bin_partition_map,Partition_PhysicalVM_Map,PhysicalVM_Partition_Map)

                        vm_send_map=result[0]
                        vm_receive_map=result[1]


                        result=hf.get_migration_cost(vm_send_map,vm_receive_map,PARTITION_SIZE,BANDWIDTH,SERIALIZATION_TIME,DESERIALIZATION_TIME)

                        send_bottleneck_flag=result[0]
                        migration_cost=result[1]
                        bottlneck_vmid=result[2]

                        ######### get compute time summation for all partitions in the VM######

                        vm_computetimesum_map.clear()

                        vm_computetimesum_map=hf.get_vm_comute_time(bin_partition_map,bin_vm_map,partTime)

                        ##plotting of compute+network cost per vm
                        # hf.plot_compute_network_pervm(vm_computetimesum_map,vm_send_map,vm_receive_map,PARTITION_SIZE,BANDWIDTH)
                        max_compute_time=max(vm_computetimesum_map.values())

                        ################constraint check ########################

                        #FIXME: maxTime may not be equal to the  max(vm_computetimesum_map.values())
                        if(migration_cost + max_compute_time <= UPPER_LIMIT): ### vm++ approach ==>check for constraint

                            print "constraint satisfied by VM++ "

                            #TODO: update the metrics post superstep
                            hf.update_stats_at_end_of_superstep(bin_partition_map,bin_vm_map,Partition_PhysicalVM_Map,PhysicalVM_Partition_Map)

                            #TODO: update the local matrix and paas the migration cost as it is not recomputed

                            hf.update_metrics_at_end_of_ss(superstep,vm_ss_active_map,vm_migration_ss_map,ss_migration_cost,sstime_with_migration,makespan_with_migration,maxTime,migration_cost,Superstep_time_map,Superstep_activeVM_map,partSum,vm_computetimesum_map,bin_vm_map,bin_partition_map,vm_send_map,vm_receive_map)
                                                         #(superstep,vm_ss_active_map,vm_migration_ss_map,ss_migration_cost,sstime_with_migration,makespan_with_migration,maxTime,migration_cost,Superstep_time_map,Superstep_activeVM_map,partSum,vm_computetimesum_map,bin_vm_map,bin_partition_map,vm_send_map,vm_receive_map)


                            active_vm_count=0
                            for v in vm_computetimesum_map.keys():
                                if(vm_computetimesum_map[v]>0):
                                    active_vm_count+=1


                            df = df.T
                            df[superstep]=[int(superstep),int(len(partTime.keys())),int((active_vm_count)),int(migration_cost),int(maxTime),int(max_compute_time),int(migration_cost+max_compute_time)]
                            #(columns=('Superstep','ActivePartitions' ,'ActiveVM','MigrationCost' ,'MAX_TIME','MAX_TIME_with_binPacking' ,'Total_TIME'))
                            df = df.T

                            makespan_with_migration+=(migration_cost+max_compute_time)

                            superstep+=1

                            break

                        else: ### vm++approach ===>using avoid migration approach inside

                            ## try the avoid migration approach
                            # print "In VM++ approach trying the avoid migration approach with "+str(number_of_vm)+" vms and "+str(len(partTime.keys()))+" partitions and already spawned "+str(next_VMID_to_use)+" vms superstep"+str(superstep)

                            # print "PhysicalVM_Partition_Map"
                            # print PhysicalVM_Partition_Map

                            if(hf.run_avoid_migration_approach(next_VMID_to_use,partTime,bin_vm_map,bin_partition_map,vm_computetimesum_map,Partition_PhysicalVM_Map,PhysicalVM_Partition_Map,PARTITION_SIZE,BANDWIDTH,UPPER_LIMIT,superstep,number_of_vm,vm_send_map,vm_receive_map,SERIALIZATION_TIME,DESERIALIZATION_TIME)):
                                continue
                            else:
                                hf.update_stats_at_end_of_superstep(bin_partition_map,bin_vm_map,Partition_PhysicalVM_Map,PhysicalVM_Partition_Map)
                                #
                                result=hf.get_migration_cost(vm_send_map,vm_receive_map,PARTITION_SIZE,BANDWIDTH,SERIALIZATION_TIME,DESERIALIZATION_TIME)
                                #return (send_bottleneck_flag,migration_cost,bottleneck_vmid)
                                migration_cost=result[1]
                                #TODO: update the local matrix and paas the migration cost as it is not recomputed

                                hf.update_metrics_at_end_of_ss(superstep,vm_ss_active_map,vm_migration_ss_map,ss_migration_cost,sstime_with_migration,makespan_with_migration,maxTime,migration_cost,Superstep_time_map,Superstep_activeVM_map,partSum,vm_computetimesum_map,bin_vm_map,bin_partition_map,vm_send_map,vm_receive_map)
                                                             #(superstep,vm_ss_active_map,vm_migration_ss_map,ss_migration_cost,sstime_with_migration,makespan_with_migration,maxTime,migration_cost,Superstep_time_map,Superstep_activeVM_map,partSum,vm_computetimesum_map,bin_vm_map,bin_partition_map,vm_send_map,vm_receive_map)

                                max_compute_time=max(vm_computetimesum_map.values())

                                active_vm_count=0
                                for v in vm_computetimesum_map.keys():
                                    if(vm_computetimesum_map[v]>0):
                                        active_vm_count+=1

                                df = df.T
                                df[superstep]=[int(superstep),int(len(partTime.keys())),int((active_vm_count)),int(migration_cost),int(maxTime),int(max_compute_time),int(migration_cost+max_compute_time)]
                                #(columns=('Superstep','ActivePartitions' ,'ActiveVM','MigrationCost' ,'MAX_TIME','MAX_TIME_with_binPacking' ,'Total_TIME'))
                                df = df.T

                                makespan_with_migration+=(migration_cost+max_compute_time)

                                superstep+=1

                                break


    ########################################################################################################################################################################

    '''METRIC CALCULATION at the end of all supersteps'''

    print "'''METRIC CALCULATION at the end of all supersteps'''"

    print "vm_migration_ss_map",vm_migration_ss_map

    print "vm_ss_active_map",vm_ss_active_map

    print "ss_migration_cost",ss_migration_cost


    #core_seconds_with_migration  ##for each vm get seconds in active SS + time when it is active only for migration

    total_supersteps=superstep-1

    for vm in vm_ss_active_map:



        vm_min=0
        vm_msec=0

        current_vm_msec=0

        #to avoid exception in condition check ss in vm_migration_ss_map[vm]
        if(vm in vm_migration_ss_map.keys()):
            pass
        else:
            vm_migration_ss_map[vm]=[]


        # vmTime=0

        active_list_for_vm=vm_ss_active_map[vm]

        flag=0 ##vm not started

        #TODO: update billing at end of loop

        for ss in range(1,total_supersteps+1):

            if (ss in active_list_for_vm):##case when vm is active

                current_vm_msec= current_vm_msec + sstime_with_migration[ss]
                if(flag==0):
                    flag=1

            elif(ss in vm_migration_ss_map[vm] ):#case when migration is required

                if(math.ceil(current_vm_msec/60000.0)==math.ceil((current_vm_msec+sstime_with_migration[ss])/60000.0)):

                    current_vm_msec+=sstime_with_migration[ss]

                    flag=1

                else:
                    current_vm_msec+=ss_migration_cost[ss]
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
    # print "VM CoreMin"
    # print Physical_VM_CoreMin_map
    #
    # print "VM CoreSec"
    # print Physical_VM_CoreSec_map
    #
    #
    # print "total core_Min"
    # print sum(Physical_VM_CoreMin_map.values())
    core_min=sum(Physical_VM_CoreMin_map.values())

    # print "total core_sec"
    # print sum(Physical_VM_CoreSec_map.values())/1000.0

    core_sec=sum(Physical_VM_CoreSec_map.values())/1000.0

    print df

    # print "makespan_with_migration",makespan_with_migration

    # df.to_csv("info.csv")
    print str(makespan_with_migration/1000.0)+","+str(core_min)+","+str(core_sec)