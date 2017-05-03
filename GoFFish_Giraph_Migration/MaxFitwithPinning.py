__author__ = 'ravikant'

#!/usr/bin/python
import sys
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import operator
import math
import time
########## Cost Function Calculation #############################
def costFunction(vmTime,superstep_time):

    #This function should be called for VMs which are inactive in this Superstep. It will decide whether to keep it running it not
    present_coreMin=math.ceil(vmTime/60000.0)

    if math.ceil( (vmTime + superstep_time)/60000.0) == present_coreMin:

        return True

    return False

######################MAIN ############################################################

if __name__ == '__main__':
    import random

    startTime = int(round(time.time() * 1000))
    if (len(sys.argv)!=3):
        print "Usage MaxFitWithPinning.py file_name source_partition"
        print "Example:"
        print "MaxFitWithPinning.py test.csv 4"
        quit()


    df = pd.DataFrame(columns=('Superstep', 'ActiveVM', 'MAX_TIME' ,'SUM_TIME','Total_TIME'))

    #Map SOurce Partition to VM id 1

    source_partition=int(sys.argv[2])

    input_csv=sys.argv[1]

    maxTime=0

    part_vm_mapping={}
    for i in range(0,40,1):
        part_vm_mapping[i]=-1


    vmCoreMin={}
    for i in range(0,40,1):
        vmCoreMin[i]=0

    partTime={}
    for i in range(0,40,1):
        partTime[i]=0


    SStimeMap={}

    vmSum={}
    for i in range(0,40,1):
        vmSum[i]=0

    activeVM=set()

################################### Calculation for Superstep 1 ################################
    f = open(input_csv)
    csv_f = csv.reader(f)
    for row in csv_f:
        if int(row[2]) == 1 and int(row[0])==source_partition :
            #print row[2] + "   "+row[0]+" "+row[3]
            maxTime+=int(row[3])

    part_vm_mapping[source_partition]=1

    #This map will hold the core mins required for execution till current superstep
    vmCoreMin[1]=maxTime


    #This map will hold the time for given superstep
    SStimeMap[1]=maxTime

    #This map will store the last sup[erstep index in which the VM was active (will be used in cost calculation)
    vmLastActiveSuperstep={}

    vmLastActiveSuperstep[1]=1


    df = df.T
    df[1]=[int(1),int(1),int(maxTime),int(maxTime),int(0)]
                    #df.append(superstep,vmid,partSum,maxCost)
    df = df.T

############################ Superstep 2 & onwards ##########################################

    superstep=2

    flag=True

    while flag ==True:

        vmLoad={}

        flag=False
        f = open(input_csv)
        csv_f = csv.reader(f)
        for row in csv_f:
            if int(row[2]) == superstep:

                     #print "Superstep is " +str(int(row[2]))
                     # if superstep==2 and int(row[0])==source_partition :
                     #     print "Source Partition is Active in Superstep 2"
                     #     print row
                     flag=True
                     if int(row[0]) in partTime:
                        # print partTime[int(row[0])] +" " +row[0]
                         initial=partTime[int(row[0])]
                         partTime[int(row[0])] =int(initial)  + int(row[3])
                        # print partTime[int(row[0])] +" " +row[0] +" "+row[3]
                     else:
                        partTime[int(row[0])] = row[3]


        #print " Superstep is " +str(superstep)+ "  timings are "+str(partTime)


        if flag==True:
            maxTime=0

            partSum=0


            #print partTime

            for k in partTime.keys():

                #SStimeList.append(int(partTime[k]))

                partSum=partSum+int(partTime[k])

                if maxTime<int(partTime[k]):
                    maxTime=int(partTime[k])

 ################################# Perform mapping defined in previous superstep #######################

            for v in part_vm_mapping.keys():
                #print v
                #print part_vm_mapping
                #Mapping only active partitions
                if part_vm_mapping[v]!=-1 and partTime[v]!=0:

                    activeVM.add(int(part_vm_mapping[v]))
                    vmSum[int(part_vm_mapping[v])]+=int(partTime[int(v)])
                    #print " Due to previous mapping : Superstep is: " +str(superstep)  +" Partition "+ str(v)+" is mapped to VM "+str(part_vm_mapping[v])+ " with time : "+str(partTime[int(v)])



            #Define the capacity of the VM
            maxVMSum=max(vmSum.values())
            #print "maxVMSum1 is"+ str(maxVMSum)
####################### Define the capacity of VM ###################################################
            if maxTime < maxVMSum:
                maxTime=maxVMSum


            SStimeMap[int(superstep)]=maxTime


            #*****************
            mapped_flag=False

            #Sort the partTime map to get the Current Rank

            # print "partitionTime is"+ str(partTime)
            sorted_currentRank = sorted(partTime.items(), key=operator.itemgetter(1), reverse=True)

            #print "Sorted Current Rank "+str(sorted_currentRank)

            #This map will contain available VM with thier available capacity
            AvailableVM={}

            #Sort the VM which are active because of pinning based on Available capacity & also append the inactive ones at the end of the List
            for vm in activeVM:
                #print "Active VM is "+ str(vm)
                AvailableVM[int(vm)]=int(maxTime-int(vmSum[int(vm)]))


            #TODO:THIS code can append same values multiple time Fix this:FIXED with new set for pinned_inactive_VM
            pinned_inactive_VM=set()

            for partition in part_vm_mapping.keys():
                if int(part_vm_mapping[partition]) !=-1 and  int(part_vm_mapping[partition]) not in activeVM:
                    pinned_inactive_VM.add(int(part_vm_mapping[partition]))


            if len(pinned_inactive_VM) !=0:
                for vm in pinned_inactive_VM:
                    AvailableVM[int(vm)]=maxTime




########################### Sort available VM based on current load they have :THIS IS NOT REQUIRED AS FINDING THE MAX IS ENOUGH################################
            #sorted_availableVM = sorted(AvailableVM.items(), key=operator.itemgetter(1), reverse=False)
                    # vmItem=(int(part_vm_mapping[partition]),0)
                    # sorted_availableVM.append(vmItem)

################################ Actual Algorithm ####################################################

            for p in sorted_currentRank:
                mapped_flag=False
                #print str(partTime[p]) +" "+str(part_vm_mapping[p])
                if partTime[int(p[0])]!=0 and part_vm_mapping[int(p[0])] ==-1:
                    #print "not mapped1"
                    #print "Sorted available VM "+str(sorted_availableVM)
                    #TODO:This sorting doesnt makes sense.Just find the maximum value and check whether the partitions fits , otherwise spin a new VM

                    #FInd the VM with maxCapacity
                    maxCapacity=-1
                    maxCapacityVMID=-1

                    # print "maxTIme "+str(maxTime)
                    # print "Available VM are " +str(AvailableVM)
                    for vm in AvailableVM.keys():
                        # print str(vm)+" "+str(AvailableVM[int(vm)])
                        if maxCapacity < AvailableVM[int(vm)]:
                            maxCapacity = AvailableVM[int(vm)]
                            maxCapacityVMID=int(vm)


                    # print vmSum

                    # print "maxCapacityVMID " +str(maxCapacityVMID)
                    #print "AvailableVM list is "+str(sorted_availableVM)

                    if maxCapacityVMID!=-1 and (int(vmSum[int(maxCapacityVMID)]) + int(partTime[int(p[0])]) )<= maxTime:

                        mapped_flag=True

                        part_vm_mapping[int(p[0])]=int(int(maxCapacityVMID))

                        vmSum[int(maxCapacityVMID)]+=int(partTime[int(p[0])])

                        activeVM.add(int(maxCapacityVMID))

                        AvailableVM[int(maxCapacityVMID)]=(maxTime-vmSum[int(maxCapacityVMID)])
                            #print " Superstep is: " +str(superstep)  +" Partition "+ str(p[0])+" is mapped to VM "+str((vm[0]))+ " with partition time : "+str(partTime[p[0]])

                            #TODO:Here the updated capacity is not reflected in the sorted_available_VM list. also pinned inactive VM would be lost??-FIXED BUT NOT TESTED



                    else:

                        vmid=int(max(part_vm_mapping.values()))+1

                        vmSum[int(vmid)]=int(partTime[int(p[0])])

                        #print " Superstep is: " +str(superstep)  +" Partition "+ str(p[0])+" is mapped to VM "+str(vmid)+ " with time : "+str(partTime[p[0]])
                        #print vmid
                        part_vm_mapping[int(p[0])]=int(vmid)

                        activeVM.add(int(vmid))

                        AvailableVM[int(vmid)]=int(maxTime-int((vmSum[int(vmid)])))




            #Update thte vmCoreMin value for active VM
########################################## VM CoreMin Calculation using cost function ######################################################################################

            # print "partiton-Vm mapping at Superstep "+str(superstep)+" is"

            # print part_vm_mapping

            #TODO: this code is using vm values from part_vm_mapping.values causing maxtime added to some VMs more than once. :FIXED THIS! Added two sets one for active VM and one for inactive VM
            for vm in activeVM:

                vmLastActiveSuperstep[int(vm)]=int(superstep)
                # print "TESTCOST: in SS "+str(superstep)+" updating VMCore Min for VM "+str(vm)
                vmCoreMin[int(vm)]+=maxTime

            #Update thte vmCoreMin value for inactive VMs
            #1.Find the inactive Set and then apply cost function
            inactive_vm=set()
            for vm in part_vm_mapping.values():
                if int(vm) !=-1  and (vm in activeVM) == False:
                    inactive_vm.add(int(vm))

            if len(inactive_vm) != 0:
                # print "TESTInactive VM"
                for vm in inactive_vm:
                    if costFunction(vmCoreMin[int(vm)],maxTime)==True:
                        vmCoreMin[int(vm)]+=maxTime
                        #We will not consider these VMs for utilization calculation
                        #activeVM.add(int(vm))
                        # print "Keep the VM " +str(vm) + " idle"

                    else:
                        # print "rounded off to nearest ceiling value. Terminate the VM "+str(vm)
                        #present_coreMin=math.ceil(vmTime/60000.0)
                        previous_CoreMins=math.ceil(vmCoreMin[int(vm)]/60000.0)
                        vmCoreMin[int(vm)]=int(previous_CoreMins)*60000.0

            #print "maxtime is "+str(maxTime)+ "  VMcore Mins are"
            #print vmCoreMin

                # print "calling test case"
                # if costFunction(1000,900)==True:
                #     print "Keep the VM idle"
                #         # vmCoreMin[int(vm)]+=maxTime
                # else:
                #         print "Terminate the VM.rounded off to nearest ceiling value"
                #         #present_coreMin=math.ceil(vmTime/60000.0)
                #         # previous_CoreMins=math.ceil(vmCoreMin[int(vm)]/60000.0)
                #         # vmCoreMin[int(vm)]=int(previous_CoreMins)*60000.0





            SStimeMap[int(superstep)]=maxTime


            #TODO: This code is appending the active VM value calculated before applying the cost function.
            df = df.T
            df[superstep]=[int(superstep),int(len(activeVM)),int(maxTime),int(partSum),int(0)]
                        #df.append(superstep,vmid,partSum,maxCost)
            df = df.T

           # print df


            superstep=superstep+1

####################################### Clear the variables defined for Superstep i ############################
            partTime={}

            for i in range(0,41,1):
                partTime[i]=0

            vmSum={}

            for i in range(0,41,1):
                vmSum[i]=0

            activeVM.clear()


######################################### END OF SuperSteps #####################################################

    makespan=0
    for i in range(1,df.Superstep.count()+1):
        if i>1:
            df.Total_TIME[i]=df.SUM_TIME[i]+df.Total_TIME[i-1]
            makespan+=df.MAX_TIME[i]
        else:
            df.Total_TIME[i]=df.SUM_TIME[i]
            makespan+=df.MAX_TIME[i]


    #print df
############################## PLot for Active VM ####################
    # plot=df.plot(x='Superstep', y='ActiveVM', kind='bar')
    # fig = plot.get_figure()
    # filename="FFDwithPinning-ActiveVM-"+sys.argv[1]+".png"
    # fig.savefig(filename)
    #
    # plt.close()

############################### PLot for Utilization #############################
    # df['Util'] = (df.SUM_TIME/ ( df.ActiveVM * df.MAX_TIME)).T

    # plot1=df.plot(x='Total_TIME',y= 'Util',kind='line')
    #
    # fig1 = plot1.get_figure()
    # filename1="FFDwithPinning-Util-"+sys.argv[1]+".png"
    # fig1.savefig(filename1)

############################### underutil calculation ################################

    # df['UnderUtil'] = ( ( df.ActiveVM * df.MAX_TIME) - df.SUM_TIME).T

    underutil=0

    # for i in range(1,df.Superstep.count()+1):
    #
    #     underutil+=df.UnderUtil[i]
    #
    #
    # for i in range(1,df.Superstep.count()+1):
    #
    #     df.UnderUtil[i]=math.ceil(df.UnderUtil[i]/60000.0)

    # plot2=df.plot(x='Superstep', y='UnderUtil', kind='bar')
    # fig2 = plot2.get_figure()
    # filename2="FFDwithPinning-UnderUtil-"+sys.argv[1]+".png"
    # fig2.savefig(filename2)
    #
    # plt.close()

    # print sum(vmCoreMin.values())
    #
    # print vmCoreMin

    for i in range(0,len(vmCoreMin),1):
        vmCoreMin[i]=math.ceil(vmCoreMin[i]/60000.0)


    # print vmCoreMin

    # print sum(vmCoreMin.values())
    # print makespan


    # print "vmCoreMin : "+ str(sum(vmCoreMin.values()))
    # print "makespan : "+  str(makespan)

    # print "Supersteps "+str(df.Superstep.count()) +" underUtil value "+str(underutil)


    df['VMCoreMilliSec'] = ( ( df.ActiveVM * df.MAX_TIME) ).T

    #print df

    vmCoreMilliSec=0
    for i in range(1,df.Superstep.count()+1):
        vmCoreMilliSec+=df.VMCoreMilliSec[i]

    # print "vmcoreMilliSec are "+str(vmCoreMilliSec)

    endTime = int(round(time.time() * 1000))

    # print "running time in ms "+str(endTime-startTime)

    print "MaxFit,Makespan,"+str(makespan/1000.0)+",Core-Mins,"+str(sum(vmCoreMin.values()))+",Core-Secs,"+str(vmCoreMilliSec/1000.0)+",UnderUtilization,"+str(math.ceil(underutil/60000.0))

    print str(makespan/1000.0)+","+str(sum(vmCoreMin.values()))+","+str(vmCoreMilliSec/1000.0)