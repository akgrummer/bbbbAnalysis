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


#  mXandGroup = {300 : 0, 400 : 0, 500 : 0, 600 : 0, 700 : 1, 800 : 1, 900 : 2, 1000 : 2, 1100 : 3, 1200 : 3, 1400 : 3, 1600 : 4, 1800 : 4, 2000 : 4}
mXandGroup = { 400 : 0, 500 : 0, 600 : 0, 650: 1, 700 : 1, 800 : 1, 900 : 2, 1000 : 2, 1100 : 3, 1200 : 3, 1400 : 3, 1600 : 4}

parser = argparse.ArgumentParser(description='Command line parser of skim options')
parser.add_argument('--year'   , dest = 'year'   , help = 'year'           , required = True)
parser.add_argument('--tag'    , dest = 'tag'    , help = 'production tag' , required = True)
parser.add_argument('--tagid'    , dest = 'tagid'    , help = 'production tag' , required = True)
parser.add_argument('--samplelist'    , dest = 'samplelist'    , help = 'production tag' , required = True)
parser.add_argument('--group'  , dest = 'group'  , help = 'mass group'     , required = False, default = "none")
parser.add_argument('--fixsig'    , dest = 'fixsig'    , help = 'ability to set signal strength' , required = False, default= None)

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
outputDir = eosLink + outputDirNoEos.format(username)
cmsEnvTar = "cmssw10213.tar.gz" # need to remove the matching dir at end of script
cmssw_base    = os.environ['CMSSW_BASE']
cmssw_version = "CMSSW_10_2_13"# os.environ['CMSSW_VERSION']
scram_arch    = os.environ['SCRAM_ARCH']
listOfSystematics = ["CMS_bkgnorm_YEAR", "CMS_bkgShape_YEAR", "CMS_hourglassShape_YEAR", "lumi_13TeV_YEAR", "CMS_trg_eff_YEAR", "CMS_l1prefiring_YEAR", "CMS_eff_b_b_YEAR", "CMS_eff_b_c_YEAR", "CMS_eff_b_udsg_YEAR", "CMS_PU", "CMS_scale_j_Total_YEAR", "CMS_res_j_YEAR", "CMS_res_j_breg_YEAR",  "CMS_LHE_pdf", "CMS_PS_weights"]

LimitOptionsForImpacts = {}
for systematic in listOfSystematics:
    LimitOptionsForImpacts["freeze_%s" % (systematic.replace("_YEAR", ""))] = "--freezeParameters %s" % systematic
LimitOptionsForImpacts["freeze_autoMCStats"] = "--freezeNuisanceGroups autoMCStats"

tag = args.tag

groupString = ""
if args.group != 'none' and args.group != 'auto' : groupString = ('_massGroup' + args.group)
tag = tag + groupString

fixsigTag = "_sig{0}".format(args.fixsig) if args.fixsig is not None else ""
jobsDir                  = 'CondorJobs/FitDiagnostics/jobsLimits_{0}_{1}_{2}{3}'.format(tag, args.year, args.tagid, fixsigTag)
outScriptNameBareProto   = 'job_{0}.sh'
outScriptNameProto       = (jobsDir + '/' + outScriptNameBareProto)
outFileNameProto         = 'FitDiagnostics_{0}_{1}_id{2}{3}.root'
outFileDatacardProto     = 'datacard_{0}_{1}.txt'
outFileWorkspaceProto    = 'datacard_{0}_{1}.root'
# outputFileName           = 'higgsCombineTest.AsymptoticLimits.mH120.root'
# this file exists, but not copied down:
outputFileName           = 'higgsCombineTest.FitDiagnostics.mH125.root'
# this is the diagnostics file:
outputFitDiagName        = 'fitDiagnosticsTest.root'
baseFolder               = outputDir + '/' + tag
baseFolderNoEos          = outputDirNoEos.format(username) + '/' + tag
plotFileFolderProtoNoEos = baseFolderNoEos + '/HistogramFiles_{0}/'
plotFileFolderProto      = baseFolder + '/HistogramFiles_{0}/'
fitFileFolderProto      = baseFolder + '/fitFiles_{0}/'
#  LimitOptions             = { "statOnly" : "--freezeParameters allConstrainedNuisances", "syst" : "", "freezeBKGnorm": "--freezeParameters var{.*CMS_bkgnorm.*}" }
LimitOptions             = { "statOnly" : "--freezeParameters allConstrainedNuisances", "syst" : "" }
folderYearName           = "DatacardFolder_{0}"
folderRunIIName          = "DatacardFolder_RunII"
outPlotFileNameProto     = "outPlotter_{0}_{1}.root"


tarName      = 'FitDiagnosticsCalculator.tar.gz' #%s_tar.tgz' % cmssw_version
limitWorkDir = os.getcwd()
tarLFN       = limitWorkDir + '/' + tarName


### NOTE: I must be in bbbb
to_include = [
    'prepareModels/'
]

command = 'tar -zcf {0} '.format(tarLFN)
for ti in to_include:
    command += ti + ' '

print '** INFO: Going to tar executable folder into', tarName
if os.system(command) != 0:
    print "... Not able to execute command \"", command, "\", exit"
    sys.exit()
else:
    print '** INFO: tar finished and saved in:', tarLFN
    # print '** INFO: Not going to tar executable folder, using', tarLFN


if os.path.isdir(jobsDir):
    print "... working folder", jobsDir, " already exists - be careful... will override output files on eos"
    # sys.exit()

cmd='mkdir -p ' + jobsDir
if os.system(cmd) != 0:
    print "... Not able to execute command \"", cmd, "\", exit"
    sys.exit()

##############################
#### Ship the tarball and submit the jobs
tarEOSdestLFN         = outputDir + '/' + tag + '/combine_tar/' + tarName
# tarEOSdestLFN.replace('root://cmseos.fnal.gov/', '/eos/uscms')

print "** INFO: copying executables tarball to:", tarEOSdestLFN
command = 'xrdcp -f -s %s %s' % (tarLFN, tarEOSdestLFN)
if os.system(command) != 0:
    print "... Not able to execute command \"", command, "\", exit"
    sys.exit()

##################################################
### Main Script for job
##################################################

for signalRaw in open(limitWorkDir+"/"+args.samplelist, 'rb').readlines():
    if '#' in signalRaw: continue
    signal = signalRaw[:-1]
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
    writeln(outScript, 'xrdcp -f -s {0}/{1} {1}'.format(outputDir, cmsEnvTar))
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
        groupNumber =  args.group
        workspaceName = folderYearName.format(year) + "/datacard" + str(year) + "_selectionbJets_SignalRegion.root"
        outputWorkspaceFile  = plotFileFolderProto.format(year) + outFileWorkspaceProto.format(year,signal)
        writeln(outScript, 'xrdcp -s -f %s %s' % (outputWorkspaceFile, workspaceName)) ## no force overwrite output in destination
        plotFileName       = outPlotFileNameProto.format(year,signal)
        inputPlotFileName  = folderName + "/" + plotFileName
        outputPlotFileName = plotFileFolderProto.format(year) + "/" + plotFileName
        writeln(outScript, 'xrdcp -s -f %s %s' % (outputPlotFileName, inputPlotFileName)) ## no force overwrite output in destination

    for year in yearList:
        workspaceName = folderYearName.format(year) + "/datacard" + str(year) + "_selectionbJets_SignalRegion.root"
        # outputWorkspaceFile  = plotFileFolderProto.format(year) + outFileWorkspaceProto.format(year,signal)
        # writeln(outScript, 'xrdcp -s -f %s %s' % (workspaceName, outputWorkspaceFile)) ## no force overwrite output in destination
        writeln(outScript, 'echo "... running %s datacard"' % (year))
        # fit_options =' --autoBoundsPOIs r --X-rtd MINIMIZER_analytic --plots --saveShapes --saveWithUncertainties --X-rtd MINIMIZER_analytic'
        fit_options =' --autoBoundsPOIs r --X-rtd MINIMIZER_analytic --saveShapes --saveWithUncertainties'
        writeln(outScript, 'combine -M FitDiagnostics {0}  --mass 125.0 {1}'.format(workspaceName, fit_options))
        writeln(outScript, 'echo "... execution finished running TOYS with status $?"')
        writeln(outScript, 'find . -name "*FitDiagnostics*"')
        writeln(outScript, 'echo "... find command done with status $?"')
        # writeln(outScript, 'ls -ltr')
        # writeln(outScript, 'echo "... ls command done with status $?"')
        outputFitFile  = fitFileFolderProto.format(year) + outFileNameProto.format(year,signal,args.tagid, fixsigTag)
        writeln(outScript, 'echo "... copying output file %s to EOS in %s"' % (outputFitDiagName, outputFitFile))
        writeln(outScript, 'xrdcp -s -f %s %s' % (outputFitDiagName, outputFitFile)) ## no force overwrite output in destination
        writeln(outScript, 'echo "... copy done with status $?"')

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

