import os
import sys
import argparse
import getpass
import subprocess
from tqdm import tqdm

outputFolderBase = "root://cmseos.fnal.gov//store/user/{0}/bbbb_BDT"

parser = argparse.ArgumentParser(description='Command line parser of skim options')
parser.add_argument('--year'       ,  dest = 'year'       ,  help = 'production tag'           ,  required = True        )
args = parser.parse_args()


commandmake = "mkdir seed{0}"
command = "xrdcp -f -s $EOS/store/user/agrummer/bbbb_BDT/2022Apr26_all/%s/seed{0}/reweighterModel.pkl seed{0}/reweighterModel.pkl"%(args.year)

for seed in tqdm(range(2020,3020)):
    if os.system(commandmake.format(seed)) != 0:
        print "... Not able to execute command \"", commandmake.format(seed), "\", exit"
        sys.exit()
    if os.system(command.format(seed)) != 0:
        print "... Not able to execute command \"", command.format(seed), "\", exit"
        sys.exit()

