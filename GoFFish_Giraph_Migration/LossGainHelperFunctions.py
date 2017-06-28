
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

    ########### LPT implementation ########################
def load_balance(values, number_of_bins):
    values = sorted(values, reverse=True)
    #print str(values)
    bins = []

    for i in range(0,number_of_bins):
        bin=Bin()
        bins.append(bin)

    for item in values:

        min_loaded_bin=bins[0]
        min_loaded_bin.append(item)
        bins[0]=min_loaded_bin
        bins=sorted(bins,key=lambda x: x.sum, reverse=False)

    return bins

##################################################################################
''' run FFD algo '''

#argument:
#partTime : dict key-> partition value-> compute time
#return
#bin_partition_map: key-> bin number value->list of partitions
def run_FFD(partTime):

    Partition_Time_Map=dict(partTime)

    values=[]

    bin_partition_map={}

    bin_number=-1

    maxtime=-1

    for partition in Partition_Time_Map.keys():

        values.append(Partition_Time_Map[partition])

        if(maxtime < Partition_Time_Map[partition]):

            maxtime= Partition_Time_Map[partition]


    bins = pack(values,maxtime)

    for bin in bins:
        # print bin
        bin_number=bin_number+1
        l=[]
        for item in bin.items:

            key_to_remove=-1

            for p in Partition_Time_Map.keys():
                if int(Partition_Time_Map[p])==item:
                    key_to_remove=p
                    l.append(p)
                    break

            Partition_Time_Map.pop(key_to_remove)

        bin_partition_map[bin_number]=l

    return bin_partition_map

##################################################################################
''' run FFD algo '''

#argument:
#partTime : dict key-> partition value-> compute time
#return
#bin_partition_map: key-> bin number value->list of partitions
def run_load_balance(partTime,number_of_bins):

    Partition_Time_Map=dict(partTime)

    values=[]

    bin_partition_map={}

    bin_number=-1

    maxtime=-1

    for partition in Partition_Time_Map.keys():

        values.append(Partition_Time_Map[partition])

        if(maxtime < Partition_Time_Map[partition]):

            maxtime= Partition_Time_Map[partition]

    # print "values"
    # print values
    # exit()

    bins = load_balance(values,number_of_bins)

    for bin in bins:
        # print bin
        bin_number=bin_number+1
        l=[]
        for item in bin.items:

            key_to_remove=-1

            for p in Partition_Time_Map.keys():
                if int(Partition_Time_Map[p])==item:
                    key_to_remove=p
                    l.append(p)
                    break

            Partition_Time_Map.pop(key_to_remove)

        bin_partition_map[bin_number]=l

    return bin_partition_map

##################################################################################


#function to get max send/receive partition count
#argument
#VM_partition_send_map key: vm value: list of partitions to send
#VM_partition_receive_map key: vm value: list of partitions to receive

def get_max_migration_partition_count(VM_partition_send_map, VM_partition_receive_map):

    max_send_receive_partition_count_for_vm=0

    for vm in VM_partition_send_map.keys():

        if( ((len(VM_partition_send_map[vm]) ) ) > max_send_receive_partition_count_for_vm ):

            max_send_receive_partition_count_for_vm=((len(VM_partition_send_map[vm]) ))
            # bottleneck_vmid=vm
            # send_bottleneck_flag=1

    for vm in VM_partition_receive_map.keys():

        if( ( len(VM_partition_receive_map[vm])) > max_send_receive_partition_count_for_vm ):

            max_send_receive_partition_count_for_vm=( len(VM_partition_receive_map[vm]))
            # bottleneck_vmid=vm
            # send_bottleneck_flag=0

    return max_send_receive_partition_count_for_vm
##########################################################################################

''' run hungarian algo '''


def run_hungarian(bin_partition_map, PhysicalVM_Partition_Map,next_VMID_to_use):

    from munkres import Munkres, print_matrix

    cost_matrix=[]

    logical_bin_to_PhysicalVM_mapping={}

    for bin in bin_partition_map.keys():
        l=[]
        for vm in PhysicalVM_Partition_Map.keys():

            # print set(bin.items)-set(Physical_VM_Map[vm])
            # l.append(len(set(bin.items)-set(Physical_VM_Map[vm])))
            l.append(len(set(bin_partition_map[bin])-set(PhysicalVM_Partition_Map[vm])))

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


    # print 'total cost: %d' % total

    # print "logical_bin_to_PhysicalVM_mapping"
    # print logical_bin_to_PhysicalVM_mapping

    ##FIXME:spwan new VM in case all bins are not mapped and update the Physical_VM_SS_active_map
    #FIXME: we are not updating the partiton_to_physicalVM map here as we need to compute the send & receive map
    #FIXME: we have to compute the vm_ActivePartition_time based on logical bin to physical vm map and not based on Partition_PhysicalVM_Map

    if(len(logical_bin_to_PhysicalVM_mapping.keys()) != len(bin_partition_map.keys())):

        for unassigned_bin in (set(bin_partition_map.keys())-set(logical_bin_to_PhysicalVM_mapping.keys())):

            logical_bin_to_PhysicalVM_mapping[unassigned_bin]=next_VMID_to_use

            PhysicalVM_Partition_Map[next_VMID_to_use]=[]#FIXME: added new vm to the mapping

            next_VMID_to_use+=1


    return (logical_bin_to_PhysicalVM_mapping,next_VMID_to_use)

##########################################################################################################

''' compute send receive maps for vm '''

def get_send_receive_map(next_VMID_to_use,bin_vm_map,bin_partition_map,Partition_PhysicalVM_Map,PhysicalVM_Partition_Map):

    VM_partition_send_map={}

    VM_partition_receive_map={}

    for i in range(0,next_VMID_to_use):#FIXME : consider all vms that are spawned till this point
        VM_partition_receive_map[i]=set()
        VM_partition_send_map[i]=set()

    # print PhysicalVM_Partition_Map

    # print bin_partition_map
    for bin in bin_partition_map.keys():

        #get the VM to which it is mapped
        mapped_vm=bin_vm_map[bin]

        # print mapped_vm
        if(mapped_vm in PhysicalVM_Partition_Map.keys()):
            available_partition_on_vm=set(PhysicalVM_Partition_Map[mapped_vm])

        else:#FIXME: is this condition required? should have been taken care in mapping algo
            print "a vm where bin is mapped is not added to the PhysicalVM_Partition_Map"
            exit()
            available_partition_on_vm=[]
        # print logical_bin[bin]
        for partition in bin_partition_map[bin]:

            if(partition in available_partition_on_vm):
                continue
            else:
                if(Partition_PhysicalVM_Map[partition]!= -1): #FIXME: this ensure that partitions are preloaded for first use
                    VM_partition_receive_map[mapped_vm].add(partition)
                    VM_partition_send_map[Partition_PhysicalVM_Map[partition]].add(partition)
                else:
                    pass
                    # print "preload partition "+str(partition)+" on vm "+str(mapped_vm)
                    #FIXME: updating the mapping for preloaded partitions

                    #TODO: will this work for approaches other than FFD?--- looks ok as we are clearing the mapping at the start of new approach
                    # Partition_PhysicalVM_Map[partition]=mapped_vm
                    # if(mapped_vm in PhysicalVM_Partition_Map.keys()):
                    #     l=PhysicalVM_Partition_Map[mapped_vm]
                    #     l.append(partition)
                    #     PhysicalVM_Partition_Map[mapped_vm]=l
                    # else:
                    #     PhysicalVM_Partition_Map[mapped_vm]=[partition]


    # print "send map"
    # print VM_partition_send_map
    # print "receive map"
    # print VM_partition_receive_map

    return (VM_partition_send_map,VM_partition_receive_map)

##################################################################################

''' migration cost computation '''

def get_migration_cost(VM_partition_send_map,VM_partition_receive_map,PARTITION_SIZE,BANDWIDTH, SERIALIZATION_TIME,DESERIALIZATION_TIME):

    #FIXME: we are assuming duplex b/w

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


    # print "max_send_receive_partition_count_for_vm" +str(max_send_receive_partition_count_for_vm)
    if(max_send_receive_partition_count_for_vm==0):
        migration_cost=0
    else:
        migration_cost=(((max_send_receive_partition_count_for_vm*PARTITION_SIZE)/BANDWIDTH) *1000)+SERIALIZATION_TIME+DESERIALIZATION_TIME

    return (send_bottleneck_flag,migration_cost,bottleneck_vmid)

###################################################################################

'''get compute time summation for all partitions in the VM'''

def get_vm_comute_time(bin_partition_map,bin_vm_map,partTime):

    vm_ActivePartition_time={}

    for b in bin_partition_map.keys():

        for p in bin_partition_map[b]:

            v = bin_vm_map[b]

            if (v in vm_ActivePartition_time.keys()):

                vm_ActivePartition_time[v]+=int(partTime[p])

            else:
                # print str(type(partTime[active_partition])) +" , "+ str(partTime[active_partition])

                vm_ActivePartition_time[v]=int(partTime[p])

    return vm_ActivePartition_time

############################################################

''' plot the vm time '''

def plot_compute_network_pervm(vm_ActivePartition_time,vm_send_map,vm_receive_map,PARTITION_SIZE,BANDWIDTH):

    import matplotlib.pyplot as plt
    import numpy as np

    #calculate the network cost using maps
    vm_network_cost={}
    network_cost_list=[]
    compute_cost_list=[]


    for vm in vm_send_map.keys():

        migration_count= max(len(vm_send_map[vm]),len(vm_receive_map[vm]))

        vm_network_cost[vm]= migration_count*(PARTITION_SIZE/BANDWIDTH)*1000

        network_cost_list.append(vm_network_cost[vm])
        if(vm in vm_ActivePartition_time.keys()):
            compute_cost_list.append(vm_ActivePartition_time[vm])
        else:
            compute_cost_list.append(0)

    ind =np.arange(len(network_cost_list))

    # my_randoms=[]
    # import random
    # for i in range (20):
    #
    #     my_randoms.append(random.randrange(1,10001,1))
    # print len(network_cost_list)
    # print len(vm_ActivePartition_time)
    # a=np.array(my_randoms)
    a=np.array(network_cost_list)
    b=np.array(compute_cost_list)

    fig = plt.figure()

    p1 = plt.bar(ind, a, 1, color='#ff3333')
    p2 = plt.bar(ind, b, 1, color='#33ff33', bottom=sum([max(network_cost_list)]))
    # p2 = plt.bar(ind, b, 1, color='#33ff33', bottom=sum([max(my_randoms)]))



    plt.show()


##########################################################################################

''' plot the vm time '''

def plot_compute_network_pervm1(vm_ActivePartition_time,vm_send_map,vm_receive_map,PARTITION_SIZE,BANDWIDTH,superstep,number_of_vm,pdf):

    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib.backends.backend_pdf

    # pdf = matplotlib.backends.backend_pdf.PdfPages( "test1.pdf")

    #calculate the network cost using maps
    vm_network_cost={}
    network_cost_list=[]
    compute_cost_list=[]


    for vm in vm_send_map.keys():

        migration_count= max(len(vm_send_map[vm]),len(vm_receive_map[vm]))

        vm_network_cost[vm]= migration_count*(PARTITION_SIZE/BANDWIDTH)*1000

        network_cost_list.append(vm_network_cost[vm])
        if(vm in vm_ActivePartition_time.keys()):
            compute_cost_list.append(vm_ActivePartition_time[vm])
        else:
            compute_cost_list.append(0)

    ind =np.arange(len(network_cost_list))


    # print "network_cost_list",network_cost_list
    # print "compute_cost_list",compute_cost_list

    # my_randoms=[]
    # import random
    # for i in range (20):
    #
    #     my_randoms.append(random.randrange(1,10001,1))
    # print len(network_cost_list)
    # print len(vm_ActivePartition_time)
    # a=np.array(my_randoms)
    # a=np.array(network_cost_list)
    # b=np.array(compute_cost_list)

    fig = plt.figure()
    #
    # p1 = plt.bar(ind, a, 1, color='#ff3333')
    # p2 = plt.bar(ind, b, 1, color='#33ff33', bottom=sum([max(network_cost_list)]))
    # p2 = plt.bar(ind, b, 1, color='#33ff33', bottom=sum([max(my_randoms)]))

    # s="superstep,"+str(superstep)+",number_of_vm,"+str(number_of_vm)
    # fig.suptitle(s,fontsize=18)
    # plt.ylabel("time in ms")
    # plt.xlabel("vm")

    # plt.show()
    # pdf.savefig(fig, bbox_inches='tight')
    # pdf.close()

    return fig

##########################################################################################



''' compute partition score '''
def get_partition_score(bottleneck_vmid,bin_vm_map,bin_partition_map,Partition_PhysicalVM_Map,send_bottleneck_flag,partTime,vm_send_map,vm_receive_map,PARTITION_SIZE,BANDWIDTH):

    ##### calculate the score for each active partition in the  bottleneck VM
    import sys
    #get the bin corresponding to the bottleneck_vm
    bottleneck_bin=-1 ##bin corresponding to the bottleneck VM
    partition_score={} ## key->partition value->score
    partition_to_compute_score=[] # partitions for which we need to compute the score (those are involved in migration)

    max_score_pid=-1
    max_score=-(sys.maxint)-1

    for bin in bin_vm_map.keys():

        if(bin_vm_map[bin]==bottleneck_vmid):

            bottleneck_bin=bin
            break

    if(bottleneck_bin==-1): #FIXME: the case when the sender vm is dissapearing
        # print " the sender vm "+str(bottleneck_vmid) +" is dissapearing and receiving is bottleneck"
        return (partition_score,max_score_pid)



    #FIXME: this works only in case when receiving is the bottleneck
    if(send_bottleneck_flag==0):

        for p in bin_partition_map[bottleneck_bin]:

            # print "partition,"+str(p)+",prev_vmID,"+str(Partition_PhysicalVM_Map[p])+",mapped_to,"+str(bottleneck_vmid)
            if(Partition_PhysicalVM_Map[p]!=bottleneck_vmid):
                partition_to_compute_score.append(p)
        # else:
    if(send_bottleneck_flag):

        for p in vm_send_map[bottleneck_vmid]:

            partition_to_compute_score.append(p)



    # print "partition_to_compute_score"
    # print partition_to_compute_score

    # if(len(partition_to_compute_score)==0):
    #     print "bottleneck vm ",bottleneck_vmid
    #     print "bottleneck_bin",bottleneck_bin
    #     print "send_bottleneck_flag",send_bottleneck_flag
    #     print "partition in bottleneck bin ",bin_partition_map[bottleneck_bin]
    #     print "Partition_PhysicalVM_Map",Partition_PhysicalVM_Map
    #     exit()

    #TODO : compute the score for each partition involved in migration
    # 		Cost! = |P| /|B| + ( partTime[p)

    # print "send_bottleneck_flag"
    # print send_bottleneck_flag

    if(send_bottleneck_flag):

        for p_id in partition_to_compute_score:

            # print p_id

            if(p_id in vm_send_map[bottleneck_vmid] ):

                # Cost! = |P| /|B| + ( T(src +partition) - Tmax)

                partition_score[p_id]=( ((PARTITION_SIZE/BANDWIDTH)*1000) -( partTime[p_id] ) )
                if(partition_score[p_id] >max_score):
                    max_score_pid=p_id
                    max_score=partition_score[p_id]
                    # print "max_score",max_score
                    # print "max_score_pid",max_score_pid

        #TODO: get max score and check for constraint

    else: #TODO: handle the case where no migration causes spinning up a vm

        # print "partition_to_compute_score"
        # print partition_to_compute_score

        for p_id in partition_to_compute_score:



            if(p_id in vm_receive_map[bottleneck_vmid] ):

                #get the vm where the partition is residing before migration
                sender_vm_id=Partition_PhysicalVM_Map[p_id]

                #FIXME:compute the score only in case when sender_vm is running in this superstep
                if(sender_vm_id in bin_vm_map.values()):
                    partition_score[p_id]=( ((PARTITION_SIZE/BANDWIDTH)*1000) -( partTime[p_id] ))
                    if(partition_score[p_id] >max_score):
                        max_score_pid=p_id
                        max_score=partition_score[p_id]

                else:#sender vm is dissappearing
                    # print "on not migrating partititon "+str(p_id)+" we have to keep running vm "+str(sender_vm_id)
                    pass


    #TODO: if max_score_pid==-1 then directly go VM++ and leave loss gain at this point
    #FIXME: in above case goto line 822 else: ############constraint not satisfied after LossGain trying for VM++

    return (partition_score,max_score_pid)

########################################################################################################################
''' avoid migration '''

def avoid_migration_for_partition(max_score_pid,send_bottleneck_flag,bin_partition_map,bin_vm_map,vm_send_map,vm_receive_map,partTime,vm_computetimesum_map,bottleneck_vmid,PhysicalVM_Partition_Map):

    #TODO: update the bin for the max_score_pid i.e. remove it from the bin mapped to bottleneck vm and add it to bin mapped to send/receiving vm
    #FIXME: one bin is mapped to exactly one vm and vice-versa

    receiver_vm_id =-1
    sender_vm=-1

    # print "vm_send_map",vm_send_map
    # print "vm_receive_map",vm_receive_map
    # print "bottleneck_vmid",bottleneck_vmid
    # print "send_bottleneck_flag",send_bottleneck_flag
    # print "max_score_pid",max_score_pid
    # print "PhysicalVM_Partition_Map",PhysicalVM_Partition_Map

    if(send_bottleneck_flag):
        #TODO: get the vm where pid is going to be hosted in current superstep decrement its runtime and increment sender vms runtime and check for constraint
        receiver_bin=-1


        for b in bin_partition_map.keys():
            if(max_score_pid in bin_partition_map[b]):
                receiver_vm_id=bin_vm_map[b]
                receiver_bin=b
                break

        if(receiver_vm_id==-1):
            # print "receiver vm doe not exists"
            # print "func: avoid_migration_for_partition"
            exit()

        # print "avoid migration for pid "+str(max_score_pid)+" do not send it from vmid "+str(bottleneck_vmid)+" to vmid "+str(receiver_vm_id)

        if(receiver_vm_id in vm_computetimesum_map.keys()):
            pass
        else:
            vm_computetimesum_map[receiver_vm_id]=0

        if(bottleneck_vmid in vm_computetimesum_map.keys()):
            pass
        else:
            vm_computetimesum_map[bottleneck_vmid]=0


        vm_computetimesum_map[receiver_vm_id]-=partTime[max_score_pid]
        vm_computetimesum_map[bottleneck_vmid]+=partTime[max_score_pid]

        send_list=vm_send_map[bottleneck_vmid]
        send_list.remove(max_score_pid)
        vm_send_map[bottleneck_vmid]=send_list

        receiver_list=vm_receive_map[receiver_vm_id]
        receiver_list.remove(max_score_pid)
        vm_receive_map[receiver_vm_id]=receiver_list

        ##add the max_score_pid to the bin mapped tp the bottleneck vmid and remove it from  bin mapped to receiver vmid
        sender_bin=-1

        for b in bin_vm_map.keys():
            if( bottleneck_vmid == bin_vm_map[b]):
                sender_bin=b
                break

        ## add the partition to the bin mapped to the sender vm(in this case the bottleneck vm)
        partition_list=bin_partition_map[sender_bin]
        partition_list.append(max_score_pid)
        bin_partition_map[sender_bin]=partition_list


        #remove the partition from the bin mapped to the receiver vm
        partition_list=bin_partition_map[receiver_bin]
        partition_list.remove(max_score_pid)
        bin_partition_map[receiver_bin]=partition_list

        if(sender_bin ==-1 or receiver_bin==-1):
            # print "error in bin updation in avoid_migration_for_partition()"
            exit()

    else:

        sender_bin=-1
        receiver_bin=-1


        #TODO:find the sender vm based on bin_vm_map as we might have changed bins because of avoiding migration
        for v in PhysicalVM_Partition_Map.keys():

            if(max_score_pid in PhysicalVM_Partition_Map[v]):
                sender_vm=v
                break
        #find bin which has max_score_pid
        # for b in bin_partition_map.keys():
        #     if(max_score_pid in bin_partition_map[b]):
        #         sender_vm=bin_vm_map[b]
        #         sender_bin=b
        #         break

        if(sender_vm==-1):
            # print "sender vm does not exist"
            # print "func: avoid_migration_for_partition"
            exit()

        # print "avoid migration for pid "+str(max_score_pid)+" do not send it from vmid "+str(sender_vm)+" to vmid "+str(bottleneck_vmid)
        if(sender_vm in vm_computetimesum_map.keys()):
            pass
        else:
            vm_computetimesum_map[sender_vm]=0

        if(bottleneck_vmid in vm_computetimesum_map.keys()):
            pass
        else:
            vm_computetimesum_map[bottleneck_vmid]=0



        vm_computetimesum_map[sender_vm]+= partTime[max_score_pid]
        vm_computetimesum_map[bottleneck_vmid]-=partTime[max_score_pid]

        # print "sender_vm",sender_vm
        # print "bottleneck_vmid",bottleneck_vmid
        send_list=vm_send_map[sender_vm]
        send_list.remove(max_score_pid)
        vm_send_map[sender_vm]=send_list

        receiver_list=vm_receive_map[bottleneck_vmid]
        receiver_list.remove(max_score_pid)
        vm_receive_map[bottleneck_vmid]=receiver_list

        ## find the bin mapped to sender vm
        for b in bin_vm_map.keys():
            if(bin_vm_map[b]==sender_vm):
                sender_bin=b
                break

        ###find the bin mapped to the receiver(bottleneck) vm
        for b in bin_vm_map.keys():
            if( bottleneck_vmid == bin_vm_map[b]):
                receiver_bin=b
                break

        ### move the max_score_pid from receiver bin to the sender bin

        #remove from the receiver bin
        partition_list=bin_partition_map[receiver_bin]
        partition_list.remove(max_score_pid)
        bin_partition_map[receiver_bin]=partition_list

        #add to the sender bin
        partition_list=bin_partition_map[sender_bin]
        partition_list.append(max_score_pid)
        bin_partition_map[sender_bin]=partition_list



        if(sender_bin ==-1 or receiver_bin==-1):
            print "error in bin updation in avoid_migration_for_partition()"
            exit()



    # print "-----------inside avoid_migration_for_partition()------------"
    # print "vm_send_map"
    # print vm_send_map
    # print "vm_receive_map"
    # print vm_receive_map
    # print "-----------call end avoid_migration_for_partition()------------"

    return

#############################################################################################################################################################


'''function to get max send/receive partition count '''
#helper functions

#function to get max send/receive partition count
#argument
#VM_partition_send_map key: vm value: list of partitions to send
#VM_partition_receive_map key: vm value: list of partitions to receive

def max_migration_partition_count(VM_partition_send_map, VM_partition_receive_map):

    max_send_receive_partition_count_for_vm=0

    for vm in VM_partition_send_map.keys():

        if( ((len(VM_partition_send_map[vm]) ) ) > max_send_receive_partition_count_for_vm ):

            max_send_receive_partition_count_for_vm=((len(VM_partition_send_map[vm]) ))
            # bottleneck_vmid=vm
            # send_bottleneck_flag=1

    for vm in VM_partition_receive_map.keys():

        if( ( len(VM_partition_receive_map[vm])) > max_send_receive_partition_count_for_vm ):

            max_send_receive_partition_count_for_vm=( len(VM_partition_receive_map[vm]))
            # bottleneck_vmid=vm
            # send_bottleneck_flag=0

    return max_send_receive_partition_count_for_vm



###################################################################################

''' update stats at the end of superstep '''

def update_stats_at_end_of_superstep(bin_partition_map,bin_vm_map,Partition_PhysicalVM_Map,PhysicalVM_Partition_Map):

    for bin in bin_partition_map.keys():

        #get the VM to which it is mapped
        mapped_vm=bin_vm_map[bin]

        # print " bin "+str(bin)+" mapped to "+str(mapped_vm)

        # available_partition_on_vm=set(Physical_VM_Map[mapped_vm])
        # print logical_bin[bin]
        for partition in bin_partition_map[bin]:

            # print "processing partition "+str(partition)
            #remove from the earlier VM and map to new VM
            old_vm=Partition_PhysicalVM_Map[partition]

            # print "old vm "+str(old_vm)
            if(old_vm!=-1):

                l_old=PhysicalVM_Partition_Map[old_vm]
                # print "l_old "+str(l_old)
                l_old.remove(partition)
                PhysicalVM_Partition_Map[old_vm]=l_old
            else:
                # pass
                # //input format partitionID,superstep,workerID
                print str(partition)+",1,"+str(mapped_vm)

            l_new=PhysicalVM_Partition_Map[mapped_vm]
            l_new.append(partition)
            PhysicalVM_Partition_Map[mapped_vm]=l_new

            Partition_PhysicalVM_Map[partition]=mapped_vm


    return

##########################################################################

'''update new metrics'''

def update_metrics_at_end_of_ss(superstep,vm_ss_active_map,vm_migration_ss_map,ss_migration_cost,sstime_with_migration,makespan_with_migration,maxTime,migration_cost,Superstep_time_map,Superstep_activeVM_map,partSum,vm_computetimesum_map,bin_vm_map,bin_partition_map,vm_send_map,vm_receive_map):

    #FIXME: migration cost is based on the argument paassed ..make sure it is based on the updated send and receive maps
    '''active vm count '''
    #determine the active vms for compute based on bin_vm_map
    #FIXME: each bin is mapped to exactly one vm and each vm has only bin assigned to it
    #update vm_ss_active_map
    for b in bin_vm_map.keys():

        if (len(bin_partition_map[b])>0):

            mapped_vm=bin_vm_map[b]

            if(mapped_vm in vm_ss_active_map.keys()):

                l=vm_ss_active_map[mapped_vm]
                l.append(superstep)
                vm_ss_active_map[mapped_vm]=l
            else:

                vm_ss_active_map[mapped_vm]=[superstep]

        else:
            pass
            # print "empty bin in ss ",superstep
            # print bin_partition_map
    #determine the vms involved in migration based on send and receive maps
    migration_set=set()

    for vm in vm_send_map.keys():
        if(len(vm_send_map[vm]) > 0 or len(vm_receive_map[vm]) > 0 ):
            migration_set.add(vm)

    for vm in vm_receive_map.keys():
        if(len(vm_send_map[vm]) > 0 or len(vm_receive_map[vm]) > 0 ):
            migration_set.add(vm)

    for vm in migration_set:
        if(vm in vm_migration_ss_map.keys()):
            l=vm_migration_ss_map[vm]
            l.append(superstep)
            vm_migration_ss_map[vm]=l
        else:
            vm_migration_ss_map[vm]=[superstep]
    #TODO: update ss_migration_cost={} sstime_with_migration={}
    #FIXME: migration cost is based on the argument paassed ..make sure it is based on the updated send and receive maps
    ss_migration_cost[superstep]=migration_cost
    sstime_with_migration[superstep]=max(vm_computetimesum_map.values())+migration_cost

    makespan_with_migration+=max(vm_computetimesum_map.values())+migration_cost

    print "SS,"+str(superstep)+",ss_time,"+str(sstime_with_migration[superstep])+",migrationCost,"+str(migration_cost)

    return makespan_with_migration
#####################################################################

''' run avoid migration approach '''
#NOTE: if return value is false, then the constrained is satisfied no need to increment vm, Return value true indicates constrained value not satisfied increment the vm

def run_avoid_migration_approach(next_VMID_to_use,partTime,bin_vm_map,bin_partition_map,vm_computetimesum_map,Partition_PhysicalVM_Map,PhysicalVM_Partition_Map,PARTITION_SIZE,BANDWIDTH,UPPER_LIMIT,superstep,number_of_vm,vm_send_map,vm_receive_map,SERIALIZATION_TIME,DESERIALIZATION_TIME):

    # print "vm_computetimesum_map"+ str(vm_computetimesum_map)

    ''' Preference 2: LOSS GAIN APPROACH by avoiding migration '''

    #continue till no more partition with positive score is found or constrint is satisfied
    positive_score_flag=1
    vm_increment_flag=False
    #find bottleneck vmid  ..compute the score for each partition and avoid its migration
    #FIXME: not reassigning send and receive maps as this is breaking the call by reference

    # result=get_send_receive_map(next_VMID_to_use,bin_vm_map,bin_partition_map,Partition_PhysicalVM_Map,PhysicalVM_Partition_Map)

    # vm_send_map=result[0]
    # vm_receive_map=result[1]

    import matplotlib.backends.backend_pdf

    # name="superstep "+str(superstep)+",vm,"+str(number_of_vm)
    # pdf = matplotlib.backends.backend_pdf.PdfPages( name+".pdf")

    while(positive_score_flag):

        # print "------------------------------------------------------------------------------------"
        result=get_migration_cost(vm_send_map,vm_receive_map,PARTITION_SIZE,BANDWIDTH,SERIALIZATION_TIME,DESERIALIZATION_TIME)

        send_bottleneck_flag=result[0]
        migration_cost=result[1]
        bottlneck_vmid=result[2]

        ######## compute score for each partition ###############

        partition_score={} ## key->partition value->score

        result=get_partition_score(bottlneck_vmid,bin_vm_map,bin_partition_map,Partition_PhysicalVM_Map,send_bottleneck_flag,partTime,vm_send_map,vm_receive_map,PARTITION_SIZE,BANDWIDTH)

        partition_score=result[0]
        max_score_pid=result[1]

        # print "partition_score"
        # print partition_score
        #
        # print "bottlneck_vmid",bottlneck_vmid
        #
        # print "max_score_pid",max_score_pid


        # if(len(partition_score.keys())==0):
        #     print "bottlneck_vmid"
        #     print bottlneck_vmid
        # #     # print
        #     print "no partition scores computed"
        #     print "vm_send_map"
        #     print vm_send_map
        #     print "vm_receive_map"
        #     print vm_receive_map
        #     print "vm_computetimesum_map"
        #     print vm_computetimesum_map
        # #     exit()


        # print "calling avoid migration"
        #TODO: in case when the sender vm is dissapear we need to switch to the vm++ case or no more positive score
        if(max_score_pid==-1 or partition_score[max_score_pid] <=0 ):

            #FIXME: the approach failed and need to increment the vm

            positive_score_flag=0
            # hf.plot_compute_network_pervm(vm_computetimesum_map,vm_send_map,vm_receive_map,PARTITION_SIZE,BANDWIDTH)
            vm_increment_flag=True

            # print" number of bins in avoid_migration approach "+str(len(bin_partition_map.keys()))
            # pdf.close()
            break #FIXME: jump to vm++ case from here

        # print "calling avoid migration"

        avoid_migration_for_partition(max_score_pid,send_bottleneck_flag,bin_partition_map,bin_vm_map,vm_send_map,vm_receive_map,partTime,vm_computetimesum_map,bottlneck_vmid,PhysicalVM_Partition_Map)

        max_compute_time=max(vm_computetimesum_map.values())

        # print "max_compute_time"
        # print max_compute_time

        migration_count=max_migration_partition_count(vm_send_map, vm_receive_map)

        max_migration_time=((migration_count* PARTITION_SIZE/BANDWIDTH) *1000)+SERIALIZATION_TIME+DESERIALIZATION_TIME

        ##plotting of compute+network cost per vm
        # pdf.savefig(plot_compute_network_pervm1(vm_computetimesum_map,vm_send_map,vm_receive_map,PARTITION_SIZE,BANDWIDTH,superstep,number_of_vm,pdf))


        ### add plotting function here
        # hf.plot_compute_network_pervm()

        ######## check for constraint #########################



        if(max_migration_time+ max_compute_time <=UPPER_LIMIT):
            #in case of constraint satisfaction return from the function with vm_increment flag false
            # pdf.close()
            # if(superstep==6):
            #     print "inside run approach"
            #     print "vm_send_map",vm_send_map

            return False

        else:
            continue


    # pdf.close()
    return vm_increment_flag
