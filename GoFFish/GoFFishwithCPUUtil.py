import subprocess
import sys
from pandas.lib import sanitize_objects

__author__ = 'ravikant'


'''
 * client script for gopher
 * assumption is that the script will run only in head node
 *
 *
 * @author Ravikant Dindokar
 * @version 1.1
 * @see <a href="http://www.dream-lab.in/">DREAM:Lab</a>
 *
 * Copyright 2014 DREAM:Lab, Indian Institute of Science, 2014
 *
 * Licensed under the Apache License, Version 2.0(the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.

 '''
#######ARGUMENTS:
# 1. path to the json config file:  e.g. '/data/datacloud/goffish-deploy/config/goffish-conf.json'
# 2. path to the gopherapp jar file e.g.  "/home/gofs/ravikantStuff/Metagraph-1.0.jar"
# 3. class path : "edu.usc.goffish.gopher.sample.Metagraph"
# 4. graphID : "LIVJFLAT2M8P"
# 5. araguments : "8589934592:5"
# 6. no_partition_per_machine: "8"

#ASSUMPTIONS:-
#Namenode should be running
#No container or coordinator running
#/scratch is accessible from all nodes
######################## for cpu utilization logging Assuming that cpu.sh is present at $GOFFISH_BIN/gopher-bin/gopher-server location

#INPUT:
#GOFFISH DEPLOYMENT PATH e.g  GOFFISH_CLIENT=/data/datacloud/goffish-deploy/client
#PATH to the json config file
#PATH to the gopher applicatioin jar file
#DATANODE Information: ---- not required Read the config file : /data/datacloud/goffish-deploy/config/goffish-conf.json


#INTermediate files generation: jar_data.json
# {
#         "jar_path" : "/home/gofs/ravikantStuff/Metagraph-1.0.jar",
#         "class_path" : "edu.usc.goffish.gopher.sample.Metagraph",
#         "graph_id" : "LIVJFLAT2M8P",
#         "araguments" : "NILL" ,
#         "no_partition_per_machine" : "8",
#         "iterations" : "0"
# }

import sys
import json
import os
import io
import time
import datetime
import shutil
import csv


def get_sec(s):
    l = s.split(':')
    return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])

if __name__ == '__main__':

    if (len(sys.argv)!=7):
        print "Usage GoffishBFS.py json_config_file gopherapp_jar_file classpath graphID araguments  no_partition_per_machine"
        print "Example:"
        print "GoffishBFS.py '/data/datacloud/goffish-deploy/config/goffish-conf.json'  \"/home/gofs/ravikantStuff/Metagraph-1.0.jar\"  \"edu.usc.goffish.gopher.sample.Metagraph\" " \
              "\"LIVJFLAT2M8P\"  \"8589934592:5\"  8  "
        quit()



    ###################################### Reaad the json config file ######################################################
    # Reading data back

    json_config_file=str(sys.argv[1])   #TODO : first argument
    with open(json_config_file, 'r') as f:
         config_data = json.load(f)

    headnode= config_data["machines"]["headnode"]["address"]

    print "##############################"
    print "headnode addr is "+headnode

    #node['address'] will give the required node id
    node_arr = config_data['machines']['nodes']

    slave_node_count=0
    print "datanodes :"
    for node in node_arr:
        print node['address']
        slave_node_count=slave_node_count+1

    username=config_data['username']['default']
    print username

    #Note that paths does not end with / symbol
    source=config_data["paths"]["default"]["source"]
    bin_path=config_data["paths"]["default"]["bin"]
    data=config_data["paths"]["default"]["data"]
    client=config_data["paths"]["default"]["client"]
    config=config_data["paths"]["default"]["config"]
    sample=config_data["paths"]["default"]["sample"]

    ################################################# Form the jar_data.json file for gopher job #############################

    jar_data={}
    #jar_path=sys.argv[1] #TODO: take the jar file path as input from user
    #class_path=sys.argv[1] #TODO: take the class path as input from user
    jar_data["jar_path"] = str(sys.argv[2])    #TODO: second arg
    jar_data["class_path"]= str(sys.argv[3])     #TODO: third arg
    application = jar_data["class_path"].split('.')[-1]
    jar_data["graph_id"] = str(sys.argv[4])                                  #TODO: fourth arg
    jar_data["araguments"] = str(sys.argv[5])                                         #TODO : fifth arg
    jar_data["no_partition_per_machine" ]= str(sys.argv[6])                              #TODO : sixth arg
    jar_data["iterations" ]= "0"

    outfile=client+"/gopher-client/jar_data.json"


    with open(outfile, 'w') as outfile:  ###This overrides the existing file : verified
        json.dump(jar_data, outfile)


    ################################################## Run the LOAD and RUN command...  ##########################################

    gopher_client_script_path=client+"/gopher-client/gopher-client.py"

    print gopher_client_script_path

    os.chdir(client+"/gopher-client")

    load_command_string="python "+gopher_client_script_path+" LOAD"

    # print load_command_string
    #subprocess.call(load_command_string,stderr=subprocess.STDOUT,shell=True)

    run_proc1=subprocess.Popen(load_command_string ,shell=True)

    subprocess.Popen.wait(run_proc1)

    kill_cmd="kill -9 "+str(run_proc1.pid)

    os.system(kill_cmd)

    #################################### before running the run command start the top command logging on each datanode ########################

    #get the pid of the goffish process running on the datanodes
    #maintain a hasmap process to node mapping and form the cpu.sh file accordingly
    node_pid_mapping={}
    ssh_array=[]

    for datanode in node_arr:
        get_pid_command_string=" ssh "+datanode['address']+" \"jps -l  |grep edu.usc.goffish.gopher.impl.Main \" "
        jps_result=subprocess.check_output(get_pid_command_string,shell=True)
        pid_command="echo "+jps_result[:-1]+" |awk '{print $1}'"
        pid= subprocess.check_output(pid_command, shell=True)

        prid=pid[:-1]
        node_pid_mapping[datanode['address']]=prid

        # pid_command="echo "+pid[:-1]+" |awk '{print $1}'"

        nodeid=datanode['address']
        # pid_node_mapping[nodeid]=int(pid[:-1])
        #form the cpu.sh file here and write it to the destination
        cpu_string="while [ 0 ]  "+"\n"+"do "+"\n\t"+"top -p "+pid[:-1]+" -b -n 120 -d 1  >>"+bin_path+"/gopher-bin/gopher-server/cpuUtil" +"\n"+"done"+"\n"
        path_to_cpu_util_file=bin_path+"/gopher-bin/gopher-server/"

        with open("cpu.sh", "w") as text_file:
            text_file.write("%s" % cpu_string)
        #copy this file to destination
        filename="cpu.sh"
        copy_cpu_file="scp "+filename+" "+username+"@"+nodeid+":"+path_to_cpu_util_file
        os.system(copy_cpu_file)

        #Added to get thread dump
        jvmtop_string="bash /scratch/jvmtop/jvmtop.sh "+pid[:-1]+"   >>"+bin_path+"/gopher-bin/gopher-server/threadjvmtop"
        path_to_jvmtop_file=bin_path+"/gopher-bin/gopher-server/"

        with open("threadutil.sh", "w") as text_file:
            text_file.write("%s" % jvmtop_string)
        #copy this file to destination
        filename="threadutil.sh"
        copy_thread_file="scp "+filename+" "+username+"@"+nodeid+":"+path_to_jvmtop_file
        os.system(copy_thread_file)






    path_to_cpu_util_file=bin_path+"/gopher-bin/gopher-server/cpu.sh"
    path_to_jvmtop_file=bin_path+"/gopher-bin/gopher-server/threadutil.sh"
    for datanode in node_arr:
        util_command_string=" ssh  "+datanode['address']+" \"bash  "+path_to_cpu_util_file+" \" "

        threadutil_command_string=" ssh  "+datanode['address']+" \"bash  "+path_to_jvmtop_file+" \" "
        print "executing "+util_command_string
        print "executing "+threadutil_command_string
        # os.system(util_command_string)
        run_proc1=subprocess.Popen(util_command_string ,shell=True)
        run_proc2=subprocess.Popen(threadutil_command_string ,shell=True)
        ssh_array.append(run_proc1.pid)
        ssh_array.append(run_proc2.pid)


    #################################### start the RUN command ####################################################

    run_command_string="python "+gopher_client_script_path
    run_proc=subprocess.Popen(['python',gopher_client_script_path ,'RUN'])

    print "run process pid is "+ str(run_proc.pid)
    # os.system(run_command_string)
    time.sleep(10)

    print "####################host for graph.log file"
    ############################################### Check for the non empty graph.log files on all worker nodes ###################

    os.chdir(bin_path+"/gopher-bin/gopher-server")
    path_to_graphlog_file=bin_path+"/gopher-bin/gopher-server/graph.log"

    print path_to_graphlog_file

    for datanode in node_arr:
        wordcount_command_string=" ssh "+datanode['address']+" \"wc -l "+path_to_graphlog_file+"\" |awk '{print $1}'"
        print "executing "+wordcount_command_string

        result = subprocess.check_output(wordcount_command_string, shell=True)

        if int(result) > 1:
            print "host found "+str(datanode)
            host_for_graphlog_file=datanode['address']


    print "####################host for graph.log file"
    print host_for_graphlog_file

    # wait for some random time and check for  "PERF.CTRL.TOTAL_TIME" string

    match_string="PERF.CTRL.TOTAL_TIME"

    grep_command_string=" ssh "+host_for_graphlog_file+" \"grep "+match_string+"  " +path_to_graphlog_file+"\" "

    print grep_command_string

    zenda=False

    while zenda==False:
        time.sleep(1)
        try:
            result = subprocess.check_output(grep_command_string,shell=True)
        except subprocess.CalledProcessError as ex:
            continue

        print "result "+str(result)
        if len(result)> 1:
            zenda=True
        # os.system(grep_command_string)
        # if int(os.system("echo $?")) == 0:
        #     zenda=True


    ########################################### Collect the output files in /scratch and delete the orirginal files that is move the files########################################################

    #stop this utilization script on each datanode
    for datanode in node_arr:
        get_pid_for_cpufile=" ssh "+datanode['address']+" \"ps -ef |grep cpu |head -1\" "
        print "executing "+get_pid_for_cpufile

        ps_result=subprocess.check_output(get_pid_for_cpufile,shell=True)

        # print result

        pid_command="echo "+ps_result[:-1]+" |awk '{print $2}'"
        pid= subprocess.check_output(pid_command, shell=True)
        kill_string=" ssh "+datanode['address']+" \" kill -9 "+ pid[:-1]+ "  \" "
        os.system(kill_string)



        get_pid_for_threadfile=" ssh "+datanode['address']+" \"ps -ef |grep threadutil |head -1\" "
        print "executing "+get_pid_for_threadfile

        ps_result=subprocess.check_output(get_pid_for_threadfile,shell=True)

        # print result

        pid_command="echo "+ps_result[:-1]+" |awk '{print $2}'"
        pid= subprocess.check_output(pid_command, shell=True)
        kill_string=" ssh "+datanode['address']+" \" kill -9 "+ pid[:-1]+ "  \" "
        os.system(kill_string)






    ts = time.time()

    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H:%M:%S')

    parent_folder="/scratch/testUtil/withthread/1/"

    output_dir=parent_folder+application+"-"+jar_data["graph_id"] +"-"+jar_data["araguments"]+"-"+st

    create_outdir_command_string="mkdir  -p "+output_dir

    os.system(create_outdir_command_string)

    print " created output dir "+output_dir
    ##From headnode collect manager.out and coordinator.out
    manager_file_path=bin_path+"/gopher-bin/gopher-server/bin/manager.out"
    coordinator_file_path=bin_path+"/gopher-bin/gopher-server/bin/coordinator.out"


    print "files from headnode are copied"
    #copy_from_headnode_command_string=" cp "+manager_file_path+" "+coordinator_file_path+" "+output_dir

    #os.system(copy_from_headnode_command_string)

    shutil.copyfile(manager_file_path,output_dir+"/manager.out")
    shutil.copyfile(coordinator_file_path,output_dir+"/coordinator.out")

    #Collect the graph.log file

    collect_graphlog_command_string=" ssh "+host_for_graphlog_file+" \"mv "+"  " +path_to_graphlog_file+"  " + output_dir+"/graph.log"  + "\" "

    print "collecting graph.log"

    print collect_graphlog_command_string

    os.system(collect_graphlog_command_string)

    print "graph.log is copied"

    ##From datanode collect { subgraph partition container} .log file
    subgraph_file_path=bin_path+"/gopher-bin/gopher-server/subgraph.log"
    partition_file_path=bin_path+"/gopher-bin/gopher-server/partition.log"
    container_file_path=bin_path+"/gopher-bin/gopher-server/container.log"
    containerout_file_path=bin_path+"/gopher-bin/gopher-server/bin/container.out"
    #also collect the cpuUtil file
    logFileWorker_path=bin_path+"/gopher-bin/gopher-server/cpuUtil"
    threadutil_path=bin_path+"/gopher-bin/gopher-server/threadjvmtop"

    output_files_path=bin_path+"/gopher-bin/gopher-server/from-*"

    ##TODO:files may get overrride
    for datanode in node_arr:
        copy_sglog_from_datanode_command_string=" ssh "+datanode['address']+" \"mv "+subgraph_file_path+" "+output_dir+"/subgraph"+datanode['address']+".log"  +"\" "
        copy_partlog_from_datanode_command_string=" ssh "+datanode['address']+" \"mv "+partition_file_path+" "+output_dir+"/partition"+datanode['address']+".log"  +"\" "
        copy_containerlog_from_datanode_command_string=" ssh "+datanode['address']+" \"mv "+container_file_path+" "+output_dir+"/container"+datanode['address']+".log"  +"\" "
        copy_containerout_from_datanode_command_string=" ssh "+datanode['address']+" \"mv "+containerout_file_path+" "+output_dir+"/container"+datanode['address']+".out"  +"\" "
        copy_logFileWorker_from_datanode_command_string=" ssh "+datanode['address']+" \"mv "+logFileWorker_path+" "+output_dir+"/cpuUtil"+datanode['address']+".txt"  +"\" "
        copy_threadutil_from_datanode_command_string=" ssh "+datanode['address']+" \"mv "+threadutil_path+" "+output_dir+"/threadutil"+datanode['address']+".txt"  +"\" "
        copy_output_files_from_datanode_command_string=" ssh "+datanode['address']+" \"mv "+ output_files_path  +"   "   +output_dir+"/\" "

        print copy_containerout_from_datanode_command_string
        os.system(copy_sglog_from_datanode_command_string)
        os.system(copy_partlog_from_datanode_command_string)
        os.system(copy_containerlog_from_datanode_command_string)
        os.system(copy_containerout_from_datanode_command_string)
        os.system(copy_logFileWorker_from_datanode_command_string)
        os.system(copy_threadutil_from_datanode_command_string)
        os.system(copy_output_files_from_datanode_command_string)

    ########################################### Kill the job ###################################################################
    #TODO: Kill the application after collecting the logs

    os.chdir(client+"/gopher-client")

    kill_command_string="python "+gopher_client_script_path+" KILL"

    os.system(kill_command_string)

    kill_gopher_run_process_command_string="kill -9 "+str(run_proc.pid)

    print "killing the run process with command : "+kill_gopher_run_process_command_string

    os.system(kill_gopher_run_process_command_string)

    find_gopherclient_process_command_string="ps -ef|grep GopherClient.sh|awk '{print $2}'"

    result = subprocess.check_output(find_gopherclient_process_command_string,shell=True)


    print result

    for pid in ssh_array:
        cmd="kill -9 " + str(pid)
        print cmd
        os.system(cmd)

    for pid in os.popen(find_gopherclient_process_command_string).read().split("\n"):
        cmd="kill -9 " + str(pid)
        print cmd
        os.system(cmd)

    os.chdir(output_dir)

################################### Added for CPU utilization calculation #######################################
    for datanode in node_arr:

        filename="cpuUtil"+datanode['address']+".txt"

        sanity_command=" sed -i 's/top/\\ntop/g' "+ filename

        # os.system(sanity_command)
        print filename

        run_proc2=subprocess.Popen(sanity_command ,shell=True)

        subprocess.Popen.wait(run_proc2)

        print " sed executed for node "+datanode['address']

        # a=raw_input()


    for datanode in node_arr:
        filename="cpuUtil"+datanode['address']+".txt"
        utilfile=datanode['address']+"util.txt"
        pid=node_pid_mapping[ datanode['address']]
        # util_file_command="egrep -w 'top|" +node_pid_mapping[ datanode['address']] +"'  cpuUtil"+datanode['address']+".txt   "      +"|awk 'NR % 2 == 1 { o=$0 ; next } { print o \"<sep>\" $0 }'  >> "+ filename+" "

        # print util_file_command
        # os.system(util_file_command)
        #sanitize the file with sed 's/COMMANDtop/COMMAND\ntop/g'

        # sanity_command=" sed -i 's/top/\ntop/g' "+filename

        # os.system(sanity_command)

        # run_proc2=subprocess.Popen(sanity_command ,shell=True)

        # subprocess.Popen.wait(run_proc2)



        # sanity_command=" sed -i 's/nTHtop/nTH\\ntop/g' "+filename

        # os.system(sanity_command)




        util_file_command="egrep  -w "+ pid +"  "+ filename  +"   -B 8 | egrep -w 'top|"+pid+"' |awk 'NR % 2 == 1 { o=$0 ; next } { print o \"<sep>\" $0 }' |awk '{print $3,$23}'|awk '{$1=$1}1' OFS=\",\"  >> "+utilfile

        print util_file_command

        os.system(util_file_command)


    #calculating utilization

    #first filter SS 1 to 30
    #egrep 'START_SS|END_SS' partitionnode20.log | awk -F"," '$4 >0 && $4 <31 {print $0}'


    #egrep 'START_SS|END_SS' partitionnode20.log | awk '{print $2}'|awk -F"." '{print $1}'

    # egrep 'START_SS|END_SS' partitionnode20.log | awk -F"," '$4 >0 && $4 <31 {print $0}'|awk '{print $2}'|awk -F"." '{print $1}'|awk 'NR % 2 == 1 { o=$0 ; next } { print o "," $0 }'


    #FIXME : ss timings are hardcoded for PR fix it before using it for BFS
    util_values=[]
    
    for datanode in node_arr:
        filename="partition"+datanode['address']+".log"
        timingfile=datanode['address']+"SStime.txt"
        utilfile=datanode['address']+"util.txt"

        sstime_command="egrep 'START_SS|END_SS' "+ filename+ "| awk -F\",\" '$4 >0 && $4 <31 {print $0}'|awk '{print $2}'|awk -F\".\" '{print $1}'|awk 'NR % 2 == 1 { o=$0 ; next } { print o \",\" $0 }' >>"+timingfile

        print "command is "+sstime_command

        run_proc3=subprocess.Popen(sstime_command ,shell=True)



        subprocess.Popen.wait(run_proc3)

        print "generated timing file for " +datanode['address']
        # os.system(sstime_command)



    #Read the above file ie 30 lines with start and end timestamp
        #
        # f1=open(utilfile)
        # csv_f1 = csv.reader(f1)
        #
        # f = open(timingfile)
        # csv_f = csv.reader(f)
        # for row in csv_f:
        #     start_time=row[0]
        #     end_time=row[1]
        #
        #     zenda=False
        #     for row_utiil in csv_f1:
        #
        #         if zenda==False:
        #             if get_sec(start_time) < get_sec(row_utiil[0]):
        #                 zenda=True
        #                 util_values.append(float(row_utiil[1]))
        #
        #         if zenda==True:
        #             util_values.append(float(row_utiil[1]))
        #         if row_utiil[0]==start_time:
        #             zenda=True
        #             util_values.append(float(row_utiil[1]))
        #         if row_utiil[0]==end_time:
        #             break
        #
        #
        # f1.close()
        # f.close()

        #Instead rean the first and last line and get the start and end time and sum up all utilization values from file timingfile
        first_line_command="head -1 "+output_dir+ "/"+timingfile
        first_line=subprocess.check_output(first_line_command,shell=True)
        start_time=first_line[:-1].split(",")[0]

        last_line_command="tail -1 "+output_dir+ "/"+timingfile

        last_line=subprocess.check_output(last_line_command,shell=True)
        end_time=last_line[:-1].split(",")[1]



        print start_time
        print end_time

        f1=open(utilfile)
        csv_f1 = csv.reader(f1)

        zenda=False
        for row_utiil in csv_f1:

            if zenda==False:
                if get_sec(start_time) < get_sec(row_utiil[0]):
                    zenda=True
                    util_values.append(float(row_utiil[1]))

            if zenda==True:
                util_values.append(float(row_utiil[1]))
            if row_utiil[0]==start_time:
                zenda=True
                util_values.append(float(row_utiil[1]))
            if row_utiil[0]==end_time:
                break


        f1.close()
        # f.close()

        #remove empty lines from threadutil file
        # thread_file_name=output_dir+"/threadutil"+datanode['address']+".txt"
        # with open(thread_file_name,'rw') as file:
        #     for line in file:
        #         if line.strip():
        #             file.write(line)



    #read the graph.log file to get the toatl time @controller

    controller_time_command="grep PERF.CTRL.SS_TIME graph.log | awk -F\",\" '$4 >0 && $4 <31 {print $0}'|awk -F\",\" '{print $10}' | awk '{s+=$1} END {print s}' "

    controller_time_string=subprocess.check_output(controller_time_command,shell=True)

    controller_time1=controller_time_string[:-1]

    controller_time=float(controller_time1)/1000.0

    MeanUtilization=float(sum(util_values))/(float(slave_node_count)*  float(controller_time) )


    print "meanUtilization"
    print MeanUtilization

    print "sum of util values "+str(sum(util_values))

    print "controller total time "+str(controller_time)



    finalUtilval=parent_folder+application+"-"+jar_data["graph_id"] +"-"+jar_data["araguments"]+"-"+st

    utilfile=output_dir+"/MeancpuUtil.txt"

    with open(utilfile, "w") as text_file:
        text_file.write("%f" % MeanUtilization)







