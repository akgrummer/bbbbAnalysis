import ast
import os
import sys
import getpass
import argparse
from  ConfigParser import *
from StringIO import StringIO
import subprocess
import copy

t3SubmitScript = '/uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/scripts/t3submit'

def writeln(f, line):
    f.write(line + '\n')

parser = argparse.ArgumentParser(description='Command line parser of skim options')
parser.add_argument('--year'   , dest = 'year'   , help = 'year'           , required = True)
parser.add_argument('--tag'    , dest = 'tag'    , help = 'production tag' , required = True)
parser.add_argument('--samplelist'    , dest = 'samplelist'    , help = 'production tag' , required = True)
parser.add_argument('--unblind', dest = 'unblind', help = 'Unblind data'   , action='store_true', default=False)

args = parser.parse_args()

if args.year == "RunII":
    yearList = ["2016", "2017", "2018"]#, "All"]
else:
    yearList = [args.year]

if not args.tag:
    print "... please provide a non-empty tag name (are you using --tag=$1 without cmd line argument?)"
    sys.exit()

username = getpass.getuser()
print "... Welcome", username

outputDirNoEos = "/store/user/{0}/bbbb_limits/"
eosLink = "root://cmseos.fnal.gov/"
eosDir = eosLink + outputDirNoEos.format(username)
cmsEnvTar = "cmssw10213.tar.gz" # need to remove the matching dir at end of script
cmssw_base    = os.environ['CMSSW_BASE']
cmssw_version = "CMSSW_10_2_13"# os.environ['CMSSW_VERSION']
scram_arch    = os.environ['SCRAM_ARCH']
# listOfSystematics = ["CMS_bkgnorm_YEAR", "CMS_bkgShape_YEAR", "CMS_hourglassShape_YEAR", "lumi_13TeV_YEAR", "CMS_trg_eff_YEAR", "CMS_l1prefiring_YEAR", "CMS_eff_b_b_YEAR", "CMS_eff_b_c_YEAR", "CMS_eff_b_udsg_YEAR", "CMS_PU", "CMS_scale_j_Total_YEAR", "CMS_res_j_YEAR", "CMS_res_j_breg_YEAR",  "CMS_LHE_pdf", "CMS_PS_weights"]

# LimitOptionsForImpacts = {}
# for systematic in listOfSystematics:
    # LimitOptionsForImpacts["freeze_%s" % (systematic.replace("_YEAR", ""))] = "--freezeParameters %s" % systematic
# LimitOptionsForImpacts["freeze_autoMCStats"] = "--freezeNuisanceGroups autoMCStats"

tag = args.tag

blindFlag = " --run blind "
if args.unblind: blindFlag = ""

jobsDir                  = 'CondorJobs/Limits_fullPlane/jobsLimits_{0}_{1}'.format(tag, args.year)
outScriptNameBareProto   = 'job_{0}.sh'
outScriptNameProto       = (jobsDir + '/' + outScriptNameBareProto)
outFileNameProto         = 'Limit_{0}_{1}_{2}.root'
outFileWorkspaceProto    = 'datacard_{0}_{1}.root'
outputFileName           = 'higgsCombineTest.AsymptoticLimits.mH120.root'
baseFolder               = eosDir + '/' + tag
baseFolderNoEos          = outputDirNoEos.format(username) + '/' + tag
plotFileFolderProtoNoEos = baseFolderNoEos + '/genToysFiles_{0}/'
plotFileFolderProto      = baseFolder + '/HistogramFiles_{0}/'
LimitOptions             = { "statOnly" : "--freezeParameters allConstrainedNuisances", "syst" : "" }
folderYearName           = "DatacardFolder_{0}"
folderRunIIName          = "DatacardFolder_RunII"
outPlotFileNameProto     = "outPlotter_{0}_{1}.root"

tarName      = 'Limits_fullPlane_Calculator.tar.gz' #%s_tar.tgz' % cmssw_version
limitWorkDir = os.getcwd()
tarLFN       = limitWorkDir + '/' + tarName


### NOTE: I must be in bbbb
to_include = [
    'prepareModels/',
    'an-scripts/exe/'
]

command = 'tar -zcf {0} '.format(tarLFN)
for ti in to_include:
    command += ti + ' '

print '** INFO: Going to tar executable folder into', tarName
if os.system(command) != 0:
    print "... Not able to execute command \"", command, "\", exit"
    sys.exit()
    print '** INFO: tar finished and saved in:', tarLFN
else:
    print '** INFO: Not going to tar executable folder, using', tarLFN


if os.path.isdir(jobsDir):
    print "... working folder", jobsDir, " already exists, exit"
    # sys.exit()

cmd='mkdir -p ' + jobsDir
if os.system(cmd) != 0:
    print "... Not able to execute command \"", cmd, "\", exit"
    sys.exit()

##############################
#### Ship the tarball and submit the jobs
tarEOSdestLFN         = eosDir + '/' + tag + '/combine_tar/' + tarName
# tarEOSdestLFN.replace('root://cmseos.fnal.gov/', '/eos/uscms')

print "** INFO: copying executables tarball to:", tarEOSdestLFN
command = 'xrdcp -f -s %s %s' % (tarLFN, tarEOSdestLFN)
if os.system(command) != 0:
    print "... Not able to execute command \"", command, "\", exit"
    sys.exit()

for year in yearList:
    command = 'eos ' + eosLink + ' mkdir %s' % (plotFileFolderProtoNoEos.format(year))
    if os.system(command) != 0:
        print "... Not able to execute command \"", command, "\", exit"
        sys.exit()

##################################################
### Main Script for job
##################################################

for signalRaw in open(limitWorkDir+"/"+args.samplelist, 'rb').readlines():
    if '#' in signalRaw: continue
    signal = signalRaw[:-1]
    massXstring =  signal[ signal.find("_MX_") + len("_MX_"): signal.find("_MY_" ) ]
    massYstring =  signal[ signal.find("_MY_") + len("_MY_"): ]
    massX = int(massXstring)
    massY = int(massYstring)
    outScriptName  = outScriptNameProto.format(signal)
    outScript      = open(outScriptName, 'w')
    writeln(outScript, '#!/bin/bash')
    writeln(outScript, '{') ## start of redirection..., keep stderr and stdout in a single file, it's easier
    writeln(outScript, 'echo "... starting job on " `date` #Date/time of start of job')
    writeln(outScript, 'echo "... running on: `uname -a`" #Condor job is running on this node')
    writeln(outScript, 'echo "... system software: `cat /etc/redhat-release`" #Operating System on that node')
    ##New setup
    writeln(outScript, 'echo "New Setup Commands"')
    writeln(outScript, 'source /cvmfs/cms.cern.ch/cmsset_default.sh')
    writeln(outScript, 'xrdcp -f -s {0}/{1} {1}'.format(eosDir, cmsEnvTar))
    writeln(outScript, 'tar -xzf %s' % cmsEnvTar)
    writeln(outScript, 'rm %s' % cmsEnvTar)
    writeln(outScript, 'export SCRAM_ARCH=%s' % scram_arch)
    writeln(outScript, 'cd {0}/src'.format(cmssw_version))
    writeln(outScript, 'scramv1 b ProjectRename')
    writeln(outScript, 'cd HiggsAnalysis/CombinedLimit/')
    writeln(outScript, 'eval `scramv1 runtime -sh`')
    writeln(outScript, '')
    writeln(outScript, 'echo "... retrieving bbbb executables tarball"')
    writeln(outScript, 'xrdcp -f -s %s .' % tarEOSdestLFN) ## force overwrite CMSSW tar
    writeln(outScript, 'echo "... uncompressing bbbb executables tarball"')
    writeln(outScript, 'tar -xzf %s' % tarName)
    writeln(outScript, 'rm %s' % tarName)
    writeln(outScript, 'echo "... retrieving filelist"')
    writeln(outScript, 'export CPP_BOOST_PATH=/cvmfs/sft.cern.ch/lcg/views/LCG_89/x86_64-slc6-gcc62-opt')
    writeln(outScript, 'export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:./lib:${CPP_BOOST_PATH}/lib')

    for year in yearList:
        folderName = folderYearName.format(year)
        writeln(outScript, 'mkdir %s' % folderName)

        workspaceName = folderName + "/datacard" + str(year) + "_selectionbJets_SignalRegion.root"
        eosWorkspaceFile  = plotFileFolderProto.format(year) + outFileWorkspaceProto.format(year,signal)
        writeln(outScript, 'xrdcp -s -f %s %s' % (eosWorkspaceFile, workspaceName)) ## no force overwrite output in destination

    if args.year == "RunII":
        year = "RunII"
        folderName = folderYearName.format(year)
        writeln(outScript, 'mkdir %s' % folderName)

        workspaceName = folderName + "/datacard" + str(year) + "_selectionbJets_SignalRegion.root"
        eosWorkspaceFile  = plotFileFolderProto.format(year) + outFileWorkspaceProto.format(year,signal)
        writeln(outScript, 'xrdcp -s -f %s %s' % (eosWorkspaceFile, workspaceName)) ## no force overwrite output in destination

    for year in yearList:
        workspaceName = folderYearName.format(year) + "/datacard" + str(year) + "_selectionbJets_SignalRegion.root"
        for option, combineOption in LimitOptions.items():
            theRealCombineCommand = combineOption.replace("YEAR", str(year))
            writeln(outScript, 'echo "... running %s %s datacard"' % (year,option))
            writeln(outScript, 'combine {0} -M AsymptoticLimits --rMax 30 {1} --X-rtd  MINIMIZER_analytic --X-rtd  FAST_VERTICAL_MORPH {2}'.format(workspaceName,blindFlag, combineOption))
            writeln(outScript, 'echo "... execution finished with status $?"')
            outputLimitFile  = plotFileFolderProto.format(year) + outFileNameProto.format(year,signal,option)
            writeln(outScript, 'echo "... copying output file %s to EOS in %s"' % (outputFileName, outputLimitFile))
            writeln(outScript, 'xrdcp -s -f %s %s' % (outputFileName, outputLimitFile)) ## no force overwrite output in destination
            writeln(outScript, 'echo "... copy done with status $?"')

    if args.year == "RunII":
        workspaceName = folderRunIIName + "/datacardRunII_selectionbJets_SignalRegion.root"
        for option, combineOption in LimitOptions.items():
            writeln(outScript, 'echo "... running RunII %s datacard"' % option)
            writeln(outScript, 'combine {0} -M AsymptoticLimits --rMax 30 {1} --X-rtd  MINIMIZER_analytic --X-rtd  FAST_VERTICAL_MORPH {2}'.format(workspaceName,blindFlag,combineOption))
            writeln(outScript, 'echo "... execution finished with status $?"')
            outputLimitFile  = plotFileFolderProto.format("RunII") + outFileNameProto.format("RunII",signal,option)
            writeln(outScript, 'echo "... copying output file %s to EOS in %s"' % (outputFileName, outputLimitFile))
            writeln(outScript, 'xrdcp -s -f %s %s' % (outputFileName, outputLimitFile)) ## no force overwrite output in destination
            writeln(outScript, 'echo "... copy done with status $?"')

    writeln(outScript, 'echo "... execution finished running full plane limits with status $?"')
    writeln(outScript, 'echo "... copy done with status $?"')
    writeln(outScript, 'pwd')
    writeln(outScript, 'ls -ltrh')
    writeln(outScript, 'cd ${_CONDOR_SCRATCH_DIR}')
    writeln(outScript, 'rm -rf %s' % cmssw_version)
    writeln(outScript, 'echo "... job finished with status $?"')
    writeln(outScript, 'echo "... finished job on " `date`')
    writeln(outScript, 'echo "... exiting script"')
    writeln(outScript, '} 2>&1') ## end of redirection
    outScript.close()



## set directory to job directory, so that logs will be saved there
os.chdir(jobsDir)
for signalRaw in open(limitWorkDir+"/"+args.samplelist, 'rb').readlines():
    if '#' in signalRaw: continue
    signal = signalRaw[:-1]
    command = "%s job_%s.sh" % (t3SubmitScript,signal)
    if os.system(command) != 0:
        print "... Not able to execute command \"", command, "\", exit"
        sys.exit()

