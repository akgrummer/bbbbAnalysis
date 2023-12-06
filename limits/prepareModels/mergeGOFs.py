import os
import sys
import argparse
import getpass
import subprocess

parser = argparse.ArgumentParser(description='Command line parser of skim options')
parser.add_argument('--tag'       ,  dest = 'tag'       ,  help = 'production tag'           ,  required = True        )
parser.add_argument('--algo'       ,  dest = 'algo'       ,  help = 'production tag'           ,  required = True        )
parser.add_argument('--year'       ,  dest = 'year'       ,  help = 'production tag'           ,  required = True        )
# parser.add_argument('--sig'       ,  dest = 'sig'       ,  help = 'production tag'           ,  required = True        )
parser.add_argument('--samplelist'    , dest = 'samplelist'    , help = 'production tag' , required = True)

args = parser.parse_args()
# tag="2023Feb28_hourglass_VR_ws"
# sig="sig_NMSSM_bbbb_MX_700_MY_300"
# sig="sig_NMSSM_bbbb_MX_500_MY_200"
# year=2016
# algo="saturated"
tag = args.tag
algo = args.algo
year = args.year

username = getpass.getuser()
print "... Welcome", username


eosLink = "root://cmseos.fnal.gov/"
outputDirNoEos = "/store/user/{0}/bbbb_limits/"
outputDir = eosLink + outputDirNoEos.format(username) + tag + "/" + "gofFiles_{}".format(year)

def runCMD(cmd):
    if os.system(cmd) != 0:
        print "... Not able to execute command \"", cmd, "\", exit"
        sys.exit()

def mergeFiles(sig):
    folderName = "GOFfiles/GOFPlots_" + tag
    cmd='mkdir -p ' + folderName
    runCMD(cmd)
    outputFileName = folderName + "/GOF_{0}_{1}_{2}_TOYS.root".format(year,sig,algo)
    # excluded the sig zeroes - the fixed signal strenth runs
    haddCmd = "hadd -f0 " + outputFileName + " `xrdfs root://cmseos.fnal.gov ls -u /store/user/" + username + "/bbbb_limits/" + tag + "/" +"gofFiles_{}".format(year) + " | egrep 'GOF_{0}_{1}_{2}_NTOYS.*\.root'| grep -v 'sig0'`".format(year,sig,algo)
    runCMD(haddCmd)
    runCMD('xrdcp -f -s {0}/{1} {2}/{1}'.format(outputDir, 'GOF_{0}_{1}_{2}_DATA.root'.format(year,sig,algo), folderName))

limitWorkDir = os.getcwd()
for signalRaw in open(limitWorkDir+"/"+args.samplelist, 'rb').readlines():
    if '#' in signalRaw: continue
    signal = signalRaw[:-1]
    mergeFiles(signal)

