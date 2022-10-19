import os
import sys
import argparse
import getpass
import subprocess
from tqdm import tqdm

###########

outputFolderBase = "root://cmseos.fnal.gov//store/user/{0}/bbbb_BDT"

parser = argparse.ArgumentParser(description='Command line parser of skim options')
#  parser.add_argument('--cfg'       ,  dest = 'cfg'       ,  help = 'config file filelist'     ,  required = True        )
parser.add_argument('--tag'       ,  dest = 'tag'       ,  help = 'production tag'           ,  required = True        )
parser.add_argument('--year'       ,  dest = 'year'       ,  help = 'production tag'           ,  required = True        )

args = parser.parse_args()
yearIN = args.year
username = getpass.getuser()
print("... Welcome", username)

outputFolder = outputFolderBase.format(username) + "/"

commandmake = "mkdir BDTgridSubmit/runLocalOutput/{0}/seed{1}"
applyBDTcommand = 'python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --seed {1} --configFile mlskim_NMSSM_XYH_bbbb/config/outputskim_{0}_Full_kinFit.cfg --weightsDir BDTgridSubmit/%s/{0}/seed{1} >> BDTgridSubmit/runLocalOutput/{0}/seed{1}/out.txt 2>> BDTgridSubmit/runLocalOutput/{0}/seed{1}/err.txt'%(args.tag)

#  for seed in tqdm(range(2020,3020)):
years=[2016,2017,2018]
for year in years:
    for seed in tqdm(range(2025,3020)):
        if os.system(commandmake.format(year,seed)) != 0:
            print "... Not able to execute command \"", commandmake.format(year,seed), "\", exit"
            sys.exit()
        if os.system(applyBDTcommand.format(year,seed)) != 0:
            print "... Not able to execute command \"", applyBDTcommand.format(year,seed), "\", exit"
            sys.exit()
         
