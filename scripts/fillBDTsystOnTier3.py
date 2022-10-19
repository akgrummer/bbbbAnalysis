import os
import sys
import argparse
import getpass
import subprocess

def writeln(f, line):
    f.write(line + '\n')

###########
# setup:
##########
## input

parser = argparse.ArgumentParser(description='Command line parser of skim options')
#  parser.add_argument('--cfg'       ,  dest = 'cfg'       ,  help = 'config file filelist'     ,  required = True        )
parser.add_argument('--tag'       ,  dest = 'tag'       ,  help = 'production tag'           ,  required = True        )
parser.add_argument('--year'       ,  dest = 'year'       ,  help = 'production tag'           ,  required = True        )

args = parser.parse_args()
year = args.year
username = getpass.getuser()
print("... Welcome", username)

outputFolderBase = "root://cmseos.fnal.gov//store/user/{0}/bbbb_BDT"
outputFolder = outputFolderBase.format(username) + "/"

jobsDir                = 'BDTfill/CondorJobs/%s/jobsBDT_%s'%(year,args.tag)
outScriptNameBareProto = 'job_year{0}_seed{1}_to_seed{2}.sh'
outScriptNameProto     = (jobsDir + '/' + outScriptNameBareProto)

cmssw_base    = os.environ['CMSSW_BASE']
cmssw_version = os.environ['CMSSW_VERSION']
scram_arch    = os.environ['SCRAM_ARCH']


tarName      = 'bbbbHistsBDTsyst.tar.gz' #%s_tar.tgz' % cmssw_version
bbbbWorkDir  = os.getcwd()
tarLFN       = bbbbWorkDir + '/tars/' + tarName

tarEOSdestLFN         = outputFolder + "tarBDT_" +args.tag + '/' + tarName


if os.path.isdir(jobsDir):
    print "... working folder", jobsDir, " already exists, exit"
    sys.exit()

cmd='mkdir -p ' + jobsDir
if os.system(cmd) != 0:
    print "... Not able to execute command \"", cmd, "\", exit"
    sys.exit()


### NOTE: I must be in bbbb
to_include = [
'bin/',
'lib/',
'config/',
'data/',
]

command = 'tar -zcf {0} '.format(tarLFN)
for ti in to_include:
    command += ti + ' '

print '** INFO: Going to tar executable folder into', tarName
if os.system(command) != 0:
    print "... Not able to execute command \"", command, "\", exit"
    sys.exit()
print '** INFO: tar finished and saved in:', tarLFN

command = 'xrdcp -f -s %s %s' % (tarLFN, tarEOSdestLFN)
if os.system(command) != 0:
    print "... Not able to execute command \"", command, "\", exit"
    sys.exit()
year="2016"
configFile = 'config/Resonant_NMSSM_bbbb/plotter_{0}Resonant_NMSSM_XYH_bbbb_systBDT_2022Apr.cfg'
selectionFile='config/Resonant_NMSSM_bbbb/selectionCfg_{0}Resonant_NMSSM_XYH_bbbb_all.cfg'
commandSED = "sed -i 's/2022Apr25_seed2025/2022Apr25_seed{0}/g' {1}"
commandSEDback = "sed -i 's/2022Apr25_seed{0}/2022Apr25_seed2025/g' {1}"
commandFill = 'fill_histograms.exe config/Resonant_NMSSM_bbbb/plotter_{0}Resonant_NMSSM_XYH_bbbb_systBDT_2022Apr.cfg'


##################################################
# write script
###
def writeScript(year, seed1,seed2):
    outScriptName  = outScriptNameProto.format(year,seed1,seed2)
    outScript      = open(outScriptName, 'w')
    #  buildBDTcommand = 'python mlskim_NMSSM_XYH_bbbb/BuildBackgroundModel.py --config mlskim_NMSSM_XYH_bbbb/config/outputskim_{0}_Full_kinFit.cfg --seed {1} --MWtraining True'
    #  copyPicklecommand = 'xrdcp -f BDToutput/fullSubmission_{0}_v27_BDTsyst_BDTweights_MassWindow_2022Apr25_seed{1}/reweighterModel.pkl  root://cmseos.fnal.gov//store/user/agrummer/bbbb_BDT/%s/{0}/seed{1}/reweighterModel.pkl'%(args.tag)
    copyWeightFile= "xrdcp -f -s root://cmseos.fnal.gov//store/user/agrummer/bbbb_BDT/%s/{0}/seed{1}/reweighterModel.pkl reweighterModel.pkl"%(args.tag)
    applyBDTcommand = 'python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --seed {1} --configFile mlskim_NMSSM_XYH_bbbb/config/outputskim_{0}_Full_kinFit.cfg --weightsDir ./'
    writeln(outScript,'#!/bin/bash')
    writeln(outScript,'{')
    writeln(outScript,'echo "... starting job on " `date` #Date/time of start of job')
    writeln(outScript,'echo "... running on: `uname -a`" #Condor job is running on this node')
    writeln(outScript,'echo "... system software: `cat /etc/redhat-release`" #Operating System on that node')
    writeln(outScript,'source /cvmfs/cms.cern.ch/cmsset_default.sh')
    writeln(outScript,'export SCRAM_ARCH=slc7_amd64_gcc700')
    writeln(outScript,'eval `scramv1 project CMSSW CMSSW_10_2_5`')
    writeln(outScript,'cd CMSSW_10_2_5/src')
    writeln(outScript,'eval `scramv1 runtime -sh`')
    writeln(outScript,'echo "... pip install"')
    writeln(outScript,'export CPP_BOOST_PATH=/cvmfs/sft.cern.ch/lcg/views/LCG_89/x86_64-slc6-gcc62-opt')
    writeln(outScript,'export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:./lib:${CPP_BOOST_PATH}/lib')

    for seed in range(2025,2028):
        commandSED.format(seed,configFile.format(year))
        commandSED.format(seed,selectionFile.format(year))
        commandFill.format(year)
        commandSEDback.format(seed,configFile.format(year))
        commandSEDback.format(seed,selectionFile.format(year))
    writeln(outScript, 'echo "... copy done with status $?"')
    writeln(outScript, 'cd ${_CONDOR_SCRATCH_DIR}')
    writeln(outScript, 'rm -rf %s' % cmssw_version)
    writeln(outScript, 'echo "... job finished with status $?"')
    writeln(outScript, 'echo "... finished job on " `date`')
    writeln(outScript, 'echo "... exiting script"')
    writeln(outScript, '} 2>&1') ## end of redirection
    outScript.close()


writeScript(year, seed1, seed2)
command = "%s/scripts/t3submit %s" % (bbbbWorkDir, outScriptNameProto.format(year,seed1,seed2))
if os.system(command) != 0:
    print "... Not able to execute command \"", command, "\", exit"
    sys.exit()
     
