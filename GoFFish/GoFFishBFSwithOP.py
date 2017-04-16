import subprocess
import sys

__author__ = 'ravikant'


'''
 * client script for gopher
 * assumption is that the script will run only in head node
 *
 *
 * @author Ravikant Dindokar
 * @version 1.0
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

if __name__ == '__main__':

    if (len(sys.argv)!=8):
        print "Usage GoffishBFS.py json_config_file gopherapp_jar_file classpath graphID araguments  no_partition_per_machine output_folder"
        print "Example:"
        print "GoffishBFS.py '/data/datacloud/goffish-deploy/config/goffish-conf.json'  \"/home/gofs/ravikantStuff/Metagraph-1.0.jar\"  \"edu.usc.goffish.gopher.sample.Metagraph\" " \
              "\"LIVJFLAT2M8P\"  \"8589934592:5\"  8   /scratch/BFS/ORKT-5M-40P-F-METIS"
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

    print "datanodes :"
    for node in node_arr:
        print node['address']

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
        time.sleep(20)
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

    ts = time.time()

    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H:%M:%S')

    parent_folder=sys.argv[7]

    output_dir=parent_folder+"/"+application+"-"+jar_data["graph_id"] +"-"+jar_data["araguments"]+"-"+st

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
    app_file_path=bin_path+"/gopher-bin/gopher-server/app.log"

    ##TODO:files may get overrride
    for datanode in node_arr:
        copy_sglog_from_datanode_command_string=" ssh "+datanode['address']+" \"mv "+subgraph_file_path+" "+output_dir+"/subgraph"+datanode['address']+".log"  +"\" "
        copy_partlog_from_datanode_command_string=" ssh "+datanode['address']+" \"mv "+partition_file_path+" "+output_dir+"/partition"+datanode['address']+".log"  +"\" "
        copy_containerlog_from_datanode_command_string=" ssh "+datanode['address']+" \"mv "+container_file_path+" "+output_dir+"/container"+datanode['address']+".log"  +"\" "
        copy_containerout_from_datanode_command_string=" ssh "+datanode['address']+" \"mv "+containerout_file_path+" "+output_dir+"/container"+datanode['address']+".out"  +"\" "
        copy_applog_from_datanode_command_string=" ssh "+datanode['address']+" \"mv "+app_file_path+" "+output_dir+"/app"+datanode['address']+".log"  +"\" "

        print copy_containerout_from_datanode_command_string
        os.system(copy_sglog_from_datanode_command_string)
        os.system(copy_partlog_from_datanode_command_string)
        os.system(copy_containerlog_from_datanode_command_string)
        os.system(copy_containerout_from_datanode_command_string)
        os.system(copy_applog_from_datanode_command_string)


    ########################################### Kill the job ###################################################################
    #TODO: Kill the application after collecting the logs

    os.chdir(client+"/gopher-client")

    kill_command_string="python "+gopher_client_script_path+" KILL"

    os.system(kill_command_string)

    kill_gopher_run_process_command_string="kill -9 "+str(run_proc.pid)

    print "killing the run process with command : "+kill_gopher_run_process_command_string

    os.system(kill_gopher_run_process_command_string)

    find_gopherclient_process_command_string="ps -ef|grep GopherClient|awk '{print $2}'"

    result = subprocess.check_output(find_gopherclient_process_command_string,shell=True)


    print result

    for pid in os.popen(find_gopherclient_process_command_string).read().split("\n"):
        cmd="kill -9 " + str(pid)
        print cmd
        os.system(cmd)


