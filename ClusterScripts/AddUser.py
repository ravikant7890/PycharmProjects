# __author__ = 'ravikant'


import os
import crypt
import subprocess

import os
import crypt
import subprocess
import csv
import sys

f = open(sys.argv[1])
csv_f = csv.reader(f)

for row in csv_f:
    # print row
    username=row[0]
    password=row[1]
    print username
    print password
    home_dir="/home/" + username
    encPass = crypt.crypt(password,"22")
    print encPass
    # hostname="sslcluster.serc.iisc.in"
    hostname="rigel.serc.iisc.in"
    os.system("useradd -p "+encPass+" " + username)

    os.chdir('/var/yp')

    # os.system('make')
    run_proc3=subprocess.Popen('make' ,shell=True)

    subprocess.Popen.wait(run_proc3)

    print " ########### make in /var/yp ################"

    change_user_command='su -c'+ " " + username

    #os.system(change_user_command)
    change_user="su --command="

    #for i in range(1,12,1):
    #    os.system("su --command=" + "' ssh -oStrictHostKeyChecking=no " +" node"+ str(i) + " exit'")

    command="'ssh-keygen -t rsa '" + " " +username
    os.system(change_user + command)
    command="'cat " + home_dir + "/.ssh/id_rsa.pub >" +home_dir+  "/.ssh/authorized_keys '" + " " +username
    os.system(change_user + command )
    command="'chmod 644 " + home_dir + "/.ssh/authorized_keys '" +" " + username
    os.system(change_user + command)
    command="'ssh -oStrictHostKeyChecking=no " + " " + hostname + " exit' " + username
    os.system(change_user + command )

    for i in range(1,12,1):
       print(change_user + "' ssh -oStrictHostKeyChecking=no " +"n"+ str(i) + " exit' " + username)
       # os.system(change_user + "' ssh -oStrictHostKeyChecking=no " +"n"+ str(i) + " exit' " + username)
       run_proc=subprocess.Popen(change_user + "' ssh -oStrictHostKeyChecking=no " +"n"+ str(i) + " exit' " + username,shell=True)
       subprocess.Popen.wait(run_proc)
       #a=raw_input(i)

    command="setfacl -R -m u:"+username+":rx /home/se256"
    os.system(command)