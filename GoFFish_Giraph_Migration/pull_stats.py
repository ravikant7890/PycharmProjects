# First: source folder
# Second: destination folder
# Third: Prefix for each file
# python pull_stats.py /scratch/RavikantStuff/EURN-Giraph-SSSP/ /scratch/anirudh-ravi/eurn-stats-17042017/ ravi_EURN40_

from os import listdir
from os import system
from subprocess import check_output
import os
import sys

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

dir_name = sys.argv[1]
destination_dir = sys.argv[2]
prefix = sys.argv[3]

destination_prefix = os.path.join(destination_dir, prefix)
with cd(dir_name):
    for directory in listdir(dir_name):
        with cd(directory):
            out = check_output("grep -R SourceVertex | awk '{print $8}'", shell=True)
            print(out)
            out = out.split(':')
            source = out[1].split(',')[0]
            destination_file = destination_prefix + source + '.csv'
            system("grep -R SourceVertex | awk '{print $8}' > " + destination_file)
            system("echo superstep,partition,subgraphID,time >> $OUTPUT" + destination_file)
            system("grep -Ri Superstep,PartitionID,subgraphID,Time | awk '{print $8}' | awk -F \":\" '{print $2}' >> $OUTPUT" + destination_file)
