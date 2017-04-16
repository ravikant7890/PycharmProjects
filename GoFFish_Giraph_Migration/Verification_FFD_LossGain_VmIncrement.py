#read output

#output format

#Arguments:
#mapping.txt
#superstep,pid,vmid

#migration.txt
#superstep,vmid,1,sent_pid  # 1 indicates send
#superstep,vmid,0,received_pid  #0 indicates receive
#NOTE only 1 partition per line

#partTime.txt
#PartitionID,SubgraphID,SuperStep,ComputeTime

#TODO
#1. collect the output for each superstep
#2. verify whether send and recive maps are correct and migration cost is correct
#3. cost for superstep is correct


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


if __name__ == '__main__':

    ##### input parsing #################################################
    #
    # if (len(sys.argv)!=5):
    #     print "Usage FDD_with_LossGain.py file_name source_partition number_of_partitions constraint_val"
    #     print "Example:"
    #     print "FDD_with_LossGain.py test.csv 4 40 20"
    #     print "columns in test.csv PartitionID,SubgraphID,SuperStep,ComputeTime"
    #     quit()

    ################################################

    mapping_file=sys.argv[1]
    migration_file=sys.argv[2]
    computetime_file=sys.argv[3]

    source_partition=sys.argv[4]

    no_of_supersteps=sys.argv[5]
    no_of_partitions=sys.argv[6]




    superstep=1


    Partition_VM_Mapping={}
    VM_send_map={}
    VM_receive_map={}



    while(superstep < no_of_supersteps+1):


        Partition_VM_Mapping.clear()


        maxTime=0

        #read the decision made by the algo

        # superstep,pid,vmid
        f = open(mapping_file)
        csv_f = csv.reader(f)
        for row in csv_f:
            # print row[2]
            if int(row[0]) == superstep :
                Partition_VM_Mapping[int(row[1])]=int(row[2])



        #migration.txt
        #superstep,vmid,1,sent_pid  # 1 indicates send
        #superstep,vmid,0,received_pid  #0 indicates receive
        #NOTE only 1 partition per line
        f = open(migration_file)
        csv_f = csv.reader(f)
        for row in csv_f:
            # print row[2]
            if int(row[0]) == superstep :
                if(int(row[2]))==0: #receive
                    vmid=int(row[1])



                else: #send case





        f = open(computetime_file)
        csv_f = csv.reader(f)
        for row in csv_f:
            # print row[2]
            if int(row[2]) == superstep and int(row[0]) == source_partition :
                maxTime+=int(row[3])




        #calculate the migration here and cost of migration


        #get the makespan for the superstep


        #get the

        superstep+=1

    #===============================================================#


        f = open(input_csv)
        csv_f = csv.reader(f)
        for row in csv_f:
            # print row[2]
            if int(row[2]) == 1 and int(row[0]) == source_partition :
                maxTime+=int(row[3])
