import numpy 
import os
import root_numpy
import pandas
import glob
import argparse
import sys
import subprocess
from hep_ml import reweight
from root_numpy import root2array
from numpy.lib.recfunctions import *
#My modules
import modules.datatools as data
import modules.plotter as plotter
import modules.bdtreweighter as bdtreweighter
import modules.selections as selector
import cPickle as pickle
from modules.ConfigurationReader import ConfigurationReader
import modules.Constants as const
from modules.ReweightModelAndTransferFactor import ReweightModelAndTransferFactor
import threading
from ROOT import TFile, TTree

###########OPTIONS
parser = argparse.ArgumentParser(description='Command line parser of skim options')
parser.add_argument('--config', dest='cfgfile',  help='Name of config file',   required = True)
args = parser.parse_args()
configFileName = args.cfgfile
configFile = ConfigurationReader(configFileName)

backgroundWeightName        = configFile.backgroundWeightName   
minpt                       = configFile.minpt       
minRegressedPt              = configFile.minRegressedPt       
minEta                      = configFile.minEta       
maxEta                      = configFile.maxEta       
preSelection                = configFile.preSelection       
controlRegionSelection      = configFile.controlRegionSelection       
skimFolder                  = configFile.skimFolder
variables                   = configFile.variables   
trainingVariables           = configFile.trainingVariables
bTagSelection               = configFile.bTagSelection
antiBTagSelection           = configFile.antiBTagSelection
analysisBackgroundArgument  = configFile.analysisBackgroundArgument
analysisClassifierArgument  = configFile.analysisClassifierArgument
addSelection                = configFile.addSelection
year                        = configFile.year

enabledBranches= list(set(variables) | set(trainingVariables) | set(const.minVariableList))
skimFolderList = skimFolder.split('/')


# create output directory
outputDirectory = const.outputDirPrefix + skimFolderList[skimFolderList.index("bbbb_ntuples")+1] + '_SkimMassWindow_%s'%(year) 

if os.path.isdir(outputDirectory):
    print "... working folder", outputDirectory, " already exists, exit"
    sys.exit()

cmd='mkdir -p ' + outputDirectory
if os.system(cmd) != 0:
    print "... Not able to execute command \"", cmd, "\", exit"
    sys.exit()

orig_stdout = sys.stdout
logFile = open(outputDirectory + '/' + const.logFileName, 'w+')
sys.stdout = logFile

outputConfigFileNameFullPath = outputDirectory + '/' + const.outputConfigFileName

# Copy confid files into the output directory
cmd='cp ' + configFileName + ' ' + outputConfigFileNameFullPath
if os.system(cmd) != 0:
    print "... Not able to execute command \"", cmd, "\", exit"
    sys.exit()

out = subprocess.Popen(['eos', const.eosPath, 'ls', skimFolder], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
stdout,stderr = out.communicate()
skimFileList = []
for fileName in stdout.split():
    if ".root" in fileName:
        fullFileName = const.eosPath + "/" + skimFolder + "/" + fileName
        tmpFile = TFile.Open(fullFileName);
        if tmpFile.Get(const.treeName).GetEntries() == 0: continue
        skimFileList.append(fullFileName)
dataset = data.root2pandas(skimFileList, const.treeName, branches=enabledBranches)

print "Number of events in dataset before cuts = ",len(dataset)
dataset          = dataset[ (dataset.H1_b1_pt > minpt) & (dataset.H1_b2_pt > minpt) & (dataset.H2_b1_pt > minpt) & (dataset.H2_b2_pt > minpt)]
dataset          = dataset[ (dataset.H1_b1_ptRegressed > minRegressedPt) & (dataset.H1_b2_ptRegressed > minRegressedPt) & (dataset.H2_b1_ptRegressed > minRegressedPt) & (dataset.H2_b2_ptRegressed > minRegressedPt)]
dataset          = dataset[ (dataset.H1_b1_eta > minEta) & (dataset.H1_b2_eta > minEta) & (dataset.H2_b1_eta > minEta) & (dataset.H2_b2_eta > minEta)]
dataset          = dataset[ (dataset.H1_b1_eta < maxEta) & (dataset.H1_b2_eta < maxEta) & (dataset.H2_b1_eta < maxEta) & (dataset.H2_b2_eta < maxEta)]
dataset.query(preSelection, inplace = True)
dataset.query(controlRegionSelection, inplace = True)
# for mass window cut study:
if (addSelection is not ""): dataset.query(addSelection, inplace = True)
print "Number of events in dataset after cuts = ",len(dataset)
data.pandas2root(dataset, const.treeName, "MassWindowFile_%s.root"%(year), mode="w")
#  # Run BDT reweight
#  BuildReweightingModel(dataset.query(bTagSelection), dataset.query(antiBTagSelection), trainingVariables, outputDirectory, const.modelFileName, analysisBackgroundArgument, analysisClassifierArgument)
cmd = 'xrdcp -f -s MassWindowFile_{0}.root root://cmseos.fnal.gov//store/user/agrummer/bbbb_ntuples/fullSubmission_{0}_v27_BDTsyst/'
if os.system(cmd.format(year)) != 0:
    print "... Not able to execute command \"", cmd, "\", exit"
    sys.exit()
cmd = 'rm MassWindowFile_{0}.root'
if os.system(cmd.format(year)) != 0:
    print "... Not able to execute command \"", cmd, "\", exit"
    sys.exit()


sys.stdout = orig_stdout
print(logFile.read())
logFile.close()

