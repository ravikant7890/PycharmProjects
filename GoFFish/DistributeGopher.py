__author__ = 'ravikant'

import json
from pprint import pprint
import sys
import os
import shutil

if (len(sys.argv)!=3):
    print "Usage DistributeGopher.py json_config_file  gopher-core.jar_path"
    quit()

config_file=sys.argv[1]
gopher_core_jar=sys.argv[2]

with open(config_file) as data_file:
    config_data = json.load(data_file)
# pprint(config_data)


headnode= config_data["machines"]["headnode"]["address"]

print "##############################"
print "headnode addr is "+headnode

#node['address'] will give the required node id
node_arr = config_data['machines']['nodes']

print "datanodes :"
for node in node_arr:
    print node['address']

bin_path=config_data["paths"]["default"]["bin"]

print bin_path

print "distributiing gopher jars"


shutil.copyfile(gopher_core_jar, bin_path+"/gopher-bin/gopher-client/lib/gopher-core-2.6.jar")
shutil.copyfile(gopher_core_jar, bin_path+"/gopher-bin/gopher-server/lib/gopher-core-2.6.jar")

for node in node_arr:

    distribute_gopher_command=" scp  "+ gopher_core_jar+"   " + node['address']+":"+bin_path+"/gopher-bin/gopher-client/lib"

    print " executing command "+distribute_gopher_command

    os.system(distribute_gopher_command)

    distribute_gopher_command=" scp  "+ gopher_core_jar+"   " + node['address']+":"+bin_path+"/gopher-bin/gopher-server/lib"

    print " executing command "+distribute_gopher_command

    os.system(distribute_gopher_command)
