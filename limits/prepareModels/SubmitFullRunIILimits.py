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

bkgNormPerMassGroupDictionary = {
  "2016" : { "0" : "1.020", "1" :  "1.020", "2" :  "1.018", "3" :  "1.015", "4" :  "1.029", "none" : "1.010"},
  "2017" : { "0" : "1.016", "1" :  "1.017", "2" :  "1.020", "3" :  "1.015", "4" :  "1.018", "none" : "1.010"},
  "2018" : { "0" : "1.042", "1" :  "1.036", "2" :  "1.032", "3" :  "1.022", "4" :  "1.010", "none" : "1.010"},
}

#  mXandGroup = {300 : 0, 400 : 0, 500 : 0, 600 : 0, 700 : 1, 800 : 1, 900 : 2, 1000 : 2, 1100 : 3, 1200 : 3, 1400 : 3, 1600 : 4, 1800 : 4, 2000 : 4}
mXandGroup = { 400 : 0, 500 : 0, 600 : 0, 700 : 1, 800 : 1, 900 : 2, 1000 : 2, 1100 : 3, 1200 : 3, 1400 : 3, 1600 : 4}

parser = argparse.ArgumentParser(description='Command line parser of skim options')
parser.add_argument('--year'   , dest = 'year'   , help = 'year'           , required = True)
parser.add_argument('--tag'    , dest = 'tag'    , help = 'production tag' , required = True)
parser.add_argument('--group'  , dest = 'group'  , help = 'mass group'     , required = False, default = "none")
parser.add_argument('--impacts', dest = 'impacts', help = 'Measure impacts', action='store_true', default=False)
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
outputDir = eosLink + outputDirNoEos.format(username)
listOfSystematics = ["CMS_bkgnorm_YEAR", "CMS_bkgShape_YEAR", "lumi_13TeV_YEAR", "CMS_trg_eff_YEAR", "CMS_l1prefiring_YEAR", "CMS_eff_b_b_YEAR", "CMS_eff_b_c_YEAR", "CMS_eff_b_udsg_YEAR", "CMS_PU", "CMS_scale_j_Total_YEAR", "CMS_res_j_YEAR", "CMS_res_j_breg_YEAR",  "CMS_LHE_pdf", "CMS_PS_weights"] 

blindFlag = " --run blind "
if args.unblind: blindFlag = ""

LimitOptionsForImpacts = {}
for systematic in listOfSystematics:
    LimitOptionsForImpacts["freeze_%s" % (systematic.replace("_YEAR", ""))] = "--freezeParameters %s" % systematic
LimitOptionsForImpacts["freeze_autoMCStats"] = "--freezeNuisanceGroups autoMCStats"

tag = args.tag

groupString = ""
if args.group != 'none' and args.group != 'auto' : groupString = ('_massGroup' + args.group)
tag = tag + groupString

jobsDir                  = 'CondorJobs/jobsLimits_' + tag
outScriptNameBareProto   = 'job_{0}.sh'
outScriptNameProto       = (jobsDir + '/' + outScriptNameBareProto)
outFileNameProto         = 'Limit_{0}_{1}_{2}.root'
outFileDatacardProto     = 'datacard_{0}_{1}.txt'
outputFileName           = 'higgsCombineTest.AsymptoticLimits.mH120.root'
baseFolder               = outputDir + '/' + tag
baseFolderNoEos          = outputDirNoEos.format(username) + '/' + tag
plotFileFolderProtoNoEos = baseFolderNoEos + '/HistogramFiles_{0}/'
plotFileFolderProto      = baseFolder + '/HistogramFiles_{0}/'
#  LimitOptions             = { "statOnly" : "--freezeParameters allConstrainedNuisances", "syst" : "", "freezeBKGnorm": "--freezeParameters var{.*CMS_bkgnorm.*}" }
LimitOptions             = { "statOnly" : "--freezeParameters allConstrainedNuisances", "syst" : "" }
folderYearName           = "DatacardFolder_{0}"
folderRunIIName          = "DatacardFolder_RunII"
outPlotFileNameProto     = "outPlotter_{0}_{1}.root"

allLimitOptions = copy.deepcopy(LimitOptions)
if args.impacts: allLimitOptions.update(LimitOptionsForImpacts)
cmssw_base    = os.environ['CMSSW_BASE']
cmssw_version = os.environ['CMSSW_VERSION']
scram_arch    = os.environ['SCRAM_ARCH']

tarName      = 'LimitCalculator.tar.gz' #%s_tar.tgz' % cmssw_version
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
    print '** INFO: tar finished and saved in:', tarLFN
else:
    print '** INFO: Not going to tar executable folder, using', tarLFN


if os.path.isdir(jobsDir):
    print "... working folder", jobsDir, " already exists, exit"
    sys.exit()    

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

command = 'eos ' + eosLink + ' mkdir %s' % (baseFolderNoEos)
if os.system(command) != 0:
    print "... Not able to execute command \"", command, "\", exit"
    sys.exit()

for year in yearList:
    configfilename  = "prepareModels/config/LimitsConfig_%s.cfg" % year
    with open(configfilename) as templateConfiguration:
        signalConfiguration = templateConfiguration.read()
    cfgparser = ConfigParser()
    cfgparser.readfp(StringIO(signalConfiguration))
    directory   = ast.literal_eval(cfgparser.get("configuration","directory"))
    # tarEOSdestLFN.replace('root://cmseos.fnal.gov/', '/eos/uscms')

    command = 'eos ' + eosLink + ' mkdir %s' % (plotFileFolderProtoNoEos.format(year))
    if os.system(command) != 0:
        print "... Not able to execute command \"", command, "\", exit"
        sys.exit()

    if args.group != "auto":
        inputHistogramFile  = directory + "/outPlotter" + groupString + ".root"
        outputHistogramFile = plotFileFolderProto.format(year) + "/outPlotter.root"
        command = 'eos cp %s %s' % (inputHistogramFile, outputHistogramFile)
        if os.system(command) != 0:
            print "... Not able to execute command \"", command, "\", exit"
            sys.exit()

    else:
        inputHistogramFile  = directory + "/outPlotter_massGroup*.root"
        command = 'eos cp %s %s' % (inputHistogramFile, plotFileFolderProto.format(year))
        if os.system(command) != 0:
            print "... Not able to execute command \"", command, "\", exit"
            sys.exit()
    
for signalRaw in open("prepareModels/listOfSamples.txt", 'rb').readlines():
    if '#' in signalRaw: continue
    signal = signalRaw[:-1]
    outScriptName  = outScriptNameProto.format(signal)
    outScript      = open(outScriptName, 'w')
    writeln(outScript, '#!/bin/bash')
    writeln(outScript, '{') ## start of redirection..., keep stderr and stdout in a single file, it's easier
    writeln(outScript, 'echo "... starting job on " `date` #Date/time of start of job')
    writeln(outScript, 'echo "... running on: `uname -a`" #Condor job is running on this node')
    writeln(outScript, 'echo "... system software: `cat /etc/redhat-release`" #Operating System on that node')
    writeln(outScript, 'source /cvmfs/cms.cern.ch/cmsset_default.sh')
    writeln(outScript, 'export SCRAM_ARCH=%s' % scram_arch)
    writeln(outScript, 'eval `scramv1 project CMSSW %s`' % cmssw_version)
    writeln(outScript, 'cd %s/src' % cmssw_version)
    writeln(outScript, 'eval `scramv1 runtime -sh`')
    writeln(outScript, 'git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit')
    writeln(outScript, 'cd HiggsAnalysis/CombinedLimit')
    writeln(outScript, 'git fetch origin')
    writeln(outScript, 'git checkout v8.2.0')
    writeln(outScript, 'scramv1 b clean; scramv1 b')
    writeln(outScript, 'echo "... retrieving bbbb executables tarball"')
    writeln(outScript, 'xrdcp -f -s %s .' % tarEOSdestLFN) ## force overwrite CMSSW tar
    writeln(outScript, 'echo "... uncompressing bbbb executables tarball"')
    writeln(outScript, 'tar -xzf %s' % tarName)
    writeln(outScript, 'rm %s' % tarName)
    writeln(outScript, 'echo "... retrieving filelist"')
    writeln(outScript, 'export CPP_BOOST_PATH=/cvmfs/sft.cern.ch/lcg/views/LCG_89/x86_64-slc6-gcc62-opt')
    writeln(outScript, 'export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:./lib:${CPP_BOOST_PATH}/lib')
    
    for year in yearList:
        writeln(outScript, 'echo "... preparing histos"')
        folderName = folderYearName.format(year)
        writeln(outScript, 'mkdir %s' % folderName)
        groupNumber =  args.group
        groupFlag = ""
        if args.group == "auto":
            massXstring =  signal[ signal.find("_MX_") + len("_MX_"): signal.find("_MY_" ) ]
            groupNumber = mXandGroup[int(massXstring)]
            groupFlag = " --group " + str(groupNumber)
        
        # print 'python prepareModels/prepareHistos.py              --config prepareModels/config/LimitsConfig_%s.cfg --signal %s --directory %s --folder %s'%(year,signal,plotFileFolderProto.format(year),folderName)
        writeln(outScript, 'python prepareModels/prepareHistos.py              --config prepareModels/config/LimitsConfig_%s.cfg --signal %s --directory %s --folder %s %s'%(year,signal,plotFileFolderProto.format(year),folderName, groupFlag))
        writeln(outScript, 'echo "... preparing datacard"')
        writeln(outScript, 'python prepareModels/makeDatacardsAndWorkspaces.py --config prepareModels/config/LimitsConfig_%s.cfg --card-only --no-comb --signal  %s --folder %s --bkgNorm %s'%(year,signal,folderName,bkgNormPerMassGroupDictionary[year][str(groupNumber)]))
        # writeln(outScript, 'python prepareModels/makeDatacardsAndWorkspaces.py --config prepareModels/config/LimitsConfig_%s.cfg --card-only --no-comb --signal  %s --folder %s --bkgNorm %s --addScaleSignal'%(year,signal,folderName,bkgNormPerMassGroupDictionary[year][str(groupNumber)]))

    #copying Pdf, scale and PS systematics from samples in which they are present
    folderName2016 = folderYearName.format(2016)
    folderName2017 = folderYearName.format(2017)
    folderName2018 = folderYearName.format(2018)

    writeln(outScript, "python prepareModels/addPDFSystematic.py --inputDatacard  %s/datacard%s_selectionbJets_SignalRegion.txt --sampleName %s" %(folderName2016, 2016, signal) )
    writeln(outScript, "python prepareModels/addPDFSystematic.py --inputDatacard  %s/datacard%s_selectionbJets_SignalRegion.txt --sampleName %s" %(folderName2017, 2017, signal) )
    writeln(outScript, "python prepareModels/addPDFSystematic.py --inputDatacard  %s/datacard%s_selectionbJets_SignalRegion.txt --sampleName %s" %(folderName2018, 2018, signal) )


    for year in yearList:
        folderName = folderYearName.format(year)
        writeln(outScript, 'text2workspace.py %s/datacard%s_selectionbJets_SignalRegion.txt' % (folderName, year))
        writeln(outScript, 'while [[ "$(ps aux | grep text2workspace.py | wc -l)" -gt "1" ]]; do echo "text2workspace.py still running..."; sleep 5; done')
        writeln(outScript, 'sleep 15')
        datacardName = folderName + "/datacard" + str(year) + "_selectionbJets_SignalRegion.txt"
        outputDatacardFile  = plotFileFolderProto.format(year) + outFileDatacardProto.format(year,signal)
        writeln(outScript, 'xrdcp -s -f %s %s' % (datacardName, outputDatacardFile)) ## no force overwrite output in destination
        plotFileName       = outPlotFileNameProto.format(year,signal)
        inputPlotFileName  = folderName + "/" + plotFileName
        outputPlotFileName = plotFileFolderProto.format(year) + "/" + plotFileName
        writeln(outScript, 'xrdcp -s -f %s %s' % (inputPlotFileName, outputPlotFileName)) ## no force overwrite output in destination

    if args.year == "RunII":
        writeln(outScript, 'mkdir %s' % folderRunIIName)
        writeln(outScript, 'combineCards.py c2016=DatacardFolder_2016/datacard2016_selectionbJets_SignalRegion.txt c2017=DatacardFolder_2017/datacard2017_selectionbJets_SignalRegion.txt c2018=DatacardFolder_2018/datacard2018_selectionbJets_SignalRegion.txt > %s/datacardRunII_selectionbJets_SignalRegion.txt' % folderRunIIName)
        outputDatacardFile  = plotFileFolderProto.format("RunII") + outFileDatacardProto.format("RunII",signal)
        datacardName = folderRunIIName + "/datacardRunII_selectionbJets_SignalRegion.txt"
        writeln(outScript, 'xrdcp -s -f %s %s' % (datacardName, outputDatacardFile)) ## no force overwrite output in destination
        writeln(outScript, 'text2workspace.py %s/datacardRunII_selectionbJets_SignalRegion.txt' % folderRunIIName)
        writeln(outScript, 'sleep 15')
    
    for year in yearList:
        workspaceName = folderYearName.format(year) + "/datacard" + str(year) + "_selectionbJets_SignalRegion.root"
        for option, combineCommand in allLimitOptions.items(): 
            # if "YEAR" in combineCommand:
            theRealCombineCommand = combineCommand.replace("YEAR", str(year))
            writeln(outScript, 'echo "... running %s %s datacard"' % (year,option))
            writeln(outScript, 'combine %s -M AsymptoticLimits --rMax 30 %s --X-rtd  MINIMIZER_analytic --X-rtd  FAST_VERTICAL_MORPH %s' % (workspaceName,blindFlag,theRealCombineCommand))
            writeln(outScript, 'echo "... execution finished with status $?"')
            outputLimitFile  = plotFileFolderProto.format(year) + outFileNameProto.format(year,signal,option)
            writeln(outScript, 'echo "... copying output file %s to EOS in %s"' % (outputFileName, outputLimitFile))
            writeln(outScript, 'xrdcp -s -f %s %s' % (outputFileName, outputLimitFile)) ## no force overwrite output in destination
            writeln(outScript, 'echo "... copy done with status $?"')
    
    if args.year == "RunII":
        workspaceName = folderRunIIName + "/datacardRunII_selectionbJets_SignalRegion.root"
        for option, combineCommand in LimitOptions.items(): 
            writeln(outScript, 'echo "... running RunII %s datacard"' % option)
            writeln(outScript, 'combine %s -M AsymptoticLimits --rMax 30 %s --X-rtd  MINIMIZER_analytic --X-rtd  FAST_VERTICAL_MORPH %s' % (workspaceName,blindFlag,combineCommand))
            writeln(outScript, 'echo "... execution finished with status $?"')
            outputLimitFile  = plotFileFolderProto.format("RunII") + outFileNameProto.format("RunII",signal,option)
            writeln(outScript, 'echo "... copying output file %s to EOS in %s"' % (outputFileName, outputLimitFile))
            writeln(outScript, 'xrdcp -s -f %s %s' % (outputFileName, outputLimitFile)) ## no force overwrite output in destination
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
for signalRaw in open("../../prepareModels/listOfSamples.txt", 'rb').readlines():
    if '#' in signalRaw: continue
    signal = signalRaw[:-1]
    command = "%s job_%s.sh" % (t3SubmitScript,signal)
    if os.system(command) != 0:
        print "... Not able to execute command \"", command, "\", exit"
        sys.exit()


