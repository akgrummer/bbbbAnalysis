## makeplots.py, authored by Aidan copied original pieces from BuildBackgroundModel
## this script is intended to help refine the plotting process
## hope to add a new module in plotter.py to use in BuildBackground in place of Draw1DHistosComparison
import numpy 
import os
import root_numpy
import pandas
import glob
import argparse
import sys
import subprocess
# from hep_ml import reweight
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
# from modules.ReweightModelAndTransferFactor import ReweightModelAndTransferFactor
import threading
from ROOT import TFile, TTree

def DrawPlots(data_4b, data_3b, trainingVariables, outputDirectory, modelFileName, analysisBackgroundArgument, analysisClassifierArgument):
	print "bTagDataSize     = ", len(data_4b)
	print "AntibTagDataSize = ", len(data_3b)
	print "[INFO] Processing predicted model"
	modelFileNameFullPath        = outputDirectory + '/' + modelFileName

	############################################################################
	##Let's slice data one more time to have the inputs for the bdt reweighting#
	############################################################################
	originalcr, targetcr, originalcr_weights, targetcr_weights, transferFactorOriginal = data.preparedataformodel(data_3b,data_4b,trainingVariables)
	print "transfer factor before reweight = ", transferFactorOriginal

	print originalcr_weights.mean()
	print targetcr_weights.mean()

	#######################################
	##Prepare data to create the model
	#######################################
	# plotter.rootplot_2samp_ratio(originalcr, targetcr, trainingVariables, originalcr_weights, outputDirectory,"original")	
	plotter.rootplot_2Dhist(originalcr, targetcr, originalcr_weights, 'HH_kinFit_m', 'H2_m', outputDirectory, "_nw")
	
	########################################
	## KS Test 
	########################################
	ksresult_original = bdtreweighter.ks_test(originalcr, targetcr, trainingVariables, originalcr_weights)
	ksresult_model    = bdtreweighter.ks_test(originalcr, targetcr, trainingVariables, foldingcr_weights)	
	bdtreweighter.ks_comparison(trainingVariables,ksresult_original,ksresult_model)
	ksresult_originalpy = bdtreweighter.ks_testpy(originalcr, targetcr, trainingVariables, originalcr_weights)
	ksresult_modelpy    = bdtreweighter.ks_testpy(originalcr, targetcr, trainingVariables, foldingcr_weights)	
	bdtreweighter.ks_comparison(trainingVariables,ksresult_originalpy,ksresult_modelpy)

#############COMMAND CODE IS BELOW ######################

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

enabledBranches= list(set(variables) | set(trainingVariables) | set(const.minVariableList))
skimFolderList = skimFolder.split('/')


# create output directory
outputDirectory = const.outputDirPrefix + skimFolderList[skimFolderList.index("bbbb_ntuples")+1] + '_' + backgroundWeightName

if os.path.isdir(outputDirectory):
	print "... working folder", outputDirectory, " already exists, exit"
	sys.exit()

cmd='mkdir -p ' + outputDirectory
if os.system(cmd) != 0:
	print "... Not able to execute command \"", cmd, "\", exit"
	sys.exit()

# orig_stdout = sys.stdout
# logFile = open(outputDirectory + '/' + const.logFileName, 'w+')
# sys.stdout = logFile

outputConfigFileNameFullPath = outputDirectory + '/' + const.outputConfigFileName

# Copy confid files into the output directory
cmd='cp ' + configFileName + ' ' + outputConfigFileNameFullPath
if os.system(cmd) != 0:
	print "... Not able to execute command \"", cmd, "\", exit"
	sys.exit()

# Read samples directly from skims
# data_4b_and_3b = []

# for i in range(len(skimFolder_4btag_and_3btag)):
# 	out = subprocess.Popen(['eos', const.eosPath, 'ls', skimFolder_4btag_and_3btag[i]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
# 	stdout,stderr = out.communicate()
# 	skimFileList = []
# 	for fileName in stdout.split():
# 		if ".root" in fileName:
# 			skimFileList.append(const.eosPath + "/" + skimFolder_4btag_and_3btag[i] + "/" + fileName)
# 	data_4b_and_3b.append( data.root2pandas(skimFileList, const.treeName, branches=enabledBranches) )

# type = ["4 btag", "3 btag"]
# # skim events
# for i in range(len(data_4b_and_3b)):
# 	print "   -Number of events in dataset ", type[i], " (before) = ",len(data_4b_and_3b[i]) 
# 	data_4b_and_3b[i]          = data_4b_and_3b[i][ (data_4b_and_3b[i].H1_b1_pt > minpt) & (data_4b_and_3b[i].H1_b2_pt > minpt) & (data_4b_and_3b[i].H2_b1_pt > minpt) & (data_4b_and_3b[i].H2_b2_pt > minpt)] 
# 	data_4b_and_3b[i]          = data_4b_and_3b[i][ (data_4b_and_3b[i].H1_b1_ptRegressed > minRegressedPt) & (data_4b_and_3b[i].H1_b2_ptRegressed > minRegressedPt) & (data_4b_and_3b[i].H2_b1_ptRegressed > minRegressedPt) & (data_4b_and_3b[i].H2_b2_ptRegressed > minRegressedPt)] 
# 	data_4b_and_3b[i]          = data_4b_and_3b[i][ (data_4b_and_3b[i].H1_b1_eta > minEta) & (data_4b_and_3b[i].H1_b2_eta > minEta) & (data_4b_and_3b[i].H2_b1_eta > minEta) & (data_4b_and_3b[i].H2_b2_eta > minEta)] 
# 	data_4b_and_3b[i]          = data_4b_and_3b[i][ (data_4b_and_3b[i].H1_b1_eta < maxEta) & (data_4b_and_3b[i].H1_b2_eta < maxEta) & (data_4b_and_3b[i].H2_b1_eta < maxEta) & (data_4b_and_3b[i].H2_b2_eta < maxEta)]
# 	data_4b_and_3b[i].query(preSelection, inplace = True)
# 	data_4b_and_3b[i].query(controlRegionSelection, inplace = True)
# 	print "   -Number of events in dataset ", type[i], " (after) = ",len(data_4b_and_3b[i]) 


out = subprocess.Popen(['eos', const.eosPath, 'ls', skimFolder], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
stdout,stderr = out.communicate()
skimFileList = []
for i, fileName in enumerate(stdout.split()):
	if i>1: continue
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
print "Number of events in dataset after cuts = ",len(dataset) 

# Run BDT reweight
DrawPlots(dataset.query(bTagSelection), dataset.query(antiBTagSelection), trainingVariables, outputDirectory, const.modelFileName, analysisBackgroundArgument, analysisClassifierArgument)

# sys.stdout = orig_stdout
# print(logFile.read())
# logFile.close()