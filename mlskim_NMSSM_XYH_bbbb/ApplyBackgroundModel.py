import numpy 
import os
import root_numpy
import pandas
import glob
import argparse
import sys
import subprocess
import ast
from  ConfigParser import *
from hep_ml import reweight
from root_numpy import root2array
from numpy.lib.recfunctions import stack_arrays
#My modules
import modules.datatools as data
import modules.plotter as plotter
import modules.bdtreweighter as bdtreweighter
import modules.selections as selector
import cPickle as pickle
from modules.ConfigurationReader import ConfigurationReader
import modules.Constants as const
from modules.ReweightModelAndTransferFactor import ReweightModelAndTransferFactor
# from ROOT import TFile, TTree, TBranch
import ROOT
import threading
import time

def CreatePredictionModel(reweightermodel,transferfactor,normalization,dataset_3bTag, backgroundWeightName):
    ############################################################################
    ##Let's slice data one more time to have the inputs for the bdt reweighting#
    ############################################################################
    original_weights = numpy.ones(dtype='float64',shape=len(dataset_3bTag))
    original_weights = numpy.multiply(original_weights,transferfactor)

    folding_weights= data.getmodelweights(dataset_3bTag,original_weights,reweightermodel,transferfactor,normalization)
    
    dataset_3bTag[backgroundWeightName] = folding_weights
    return dataset_3bTag[[backgroundWeightName]]


def getWeightsForBackground(dataset, theReweightModelAndTransferFactor, backgroundWeightName):
    
    reweightermodel      = theReweightModelAndTransferFactor.reweightMethod 
    transferfactor       = theReweightModelAndTransferFactor.transferFactor
    normalization        = theReweightModelAndTransferFactor.normalization

    #Get weights for the dataset
    weights = CreatePredictionModel(reweightermodel, transferfactor, normalization, dataset, backgroundWeightName)
    
    del dataset
    return weights 


def updateFile(fileName, theBackgroudWeights):
    data.pandas2root(theBackgroudWeights,'bbbbTree', fileName, mode='a')
    

def ApplyBDTweightsToFileList(fileList, treeName, trainingVariables, theReweightModelAndTransferFactor, backgroundWeightName, mode, seed):
    print "Staring with list of ", len(fileList), " files"
    for theRootFileName in fileList:
        theRootFile = ROOT.TFile.Open(theRootFileName)
        theTree = theRootFile.Get(const.treeName)
        if theTree.GetEntries() == 0 :
            print "Error: no entries in tree for file ", theRootFileName, " - skipping..."
            continue

        branchAlreadyExists = False
        for branch in theTree.GetListOfBranches():
            if branch.GetName() == backgroundWeightName :
                print "Error: branch ", backgroundWeightName, " already exists in file", theRootFileName, " skypping..."
                branchAlreadyExists = True
        theRootFile.Close()
        if branchAlreadyExists: continue


        theRootFileNameJustWeights = theRootFileName.replace("_v27/", "_v27_BDTsyst/seeds/seed%s/"%(seed))
        tmpFileName = theRootFileName.replace(const.eosPath, "")
        tmpFileName = tmpFileName.replace("/", "_")
        tmpFileNameJustWeights = tmpFileName + "_JustWeights"
        copyFromEosCommand = "xrdcp -f " + theRootFileName + " " + tmpFileName
        print copyFromEosCommand
        os.system(copyFromEosCommand)
        # time.sleep(2)
        singleListFile = [tmpFileName]
        theDataFile = data.root2pandas(singleListFile, treeName, branches=trainingVariables)
        theBackgroudWeights = getWeightsForBackground(theDataFile, theReweightModelAndTransferFactor, backgroundWeightName)
        if mode=="a":
            updateFile(tmpFileName, theBackgroudWeights)
            copyToEosCommand = "xrdcp -f " + tmpFileName + " " + theRootFileName
            os.system(copyToEosCommand)
        if mode=="w":
            data.pandas2root(theBackgroudWeights,'bbbbTree', tmpFileNameJustWeights)
            copyToEosCommand = "xrdcp -f " + tmpFileNameJustWeights + " " + theRootFileNameJustWeights
            os.system(copyToEosCommand)
            removeCommand = "rm " + tmpFileNameJustWeights
            os.system(removeCommand)
        removeCommand = "rm " + tmpFileName
        os.system(removeCommand)

    print "Done with list of ", len(fileList), " files"


#############COMMAND CODE IS BELOW ######################

###########OPTIONS
parser = argparse.ArgumentParser(description='Command line parser of skim options')
parser.add_argument('--dir'       , dest='bdtModelDir',  help='Name of config file',   required = False, default = True)
parser.add_argument('--mode'       , dest='mode',  help='write mode - append to files ("a"), just weights ("w")',   required = False, default = "a")
parser.add_argument('--seed'       , dest='seed', type=int,  help='BKG model seed - used in Build Background',   required = False, default = 0)
parser.add_argument('--signals'   , dest='signalPath' ,  help='Name of config file',   required = False, default = "None")
parser.add_argument('--singleFile', dest='singleFile' ,  help='Name of config file',   required = False, default = "None")
parser.add_argument('--configFile', dest='configFile' ,  help='Name of config file needs',   required = False, default = "None")
parser.add_argument('--weightsDir', dest='weightsDir' ,  help='Name of weights Pickle file',   required = False, default = "None")
args = parser.parse_args()
bdtModelDir = args.bdtModelDir
mode = args.mode
seed=args.seed
signalPath  = args.signalPath
singleFile  = args.singleFile

if args.configFile is not "None":
    configFileName = args.configFile
else:
    configFileName = bdtModelDir + "/" + const.outputConfigFileName
configFile = ConfigurationReader(configFileName)

backgroundWeightName        = const.weightBranchPrefix + configFile.backgroundWeightName
if seed !=0:
    backgroundWeightName=backgroundWeightName+"_seed%s"%(seed)
skimFolder                  = configFile.skimFolder
trainingVariables           = configFile.trainingVariables
threadNumber                = configFile.threadNumber

if args.weightsDir is not "None":
    modelFileName = args.weightsDir + "/" + const.modelFileName
else:
    modelFileName = bdtModelDir + "/" + const.modelFileName

if singleFile == "None":
    if signalPath == "None":
        if seed !=0:
            out = subprocess.Popen(['xrdfs', const.eosPath, 'ls', skimFolder], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:
            out = subprocess.Popen(['eos', const.eosPath, 'ls', skimFolder], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout,stderr = out.communicate()
        fileList = stdout.split()
        for fileNameIt in range(0,len(fileList)):
            if seed !=0:
                fileList[fileNameIt] = const.eosPath + "/" + fileList[fileNameIt]
            else:
                fileList[fileNameIt] = const.eosPath + "/" + skimFolder + "/" + fileList[fileNameIt]

    else:
        out = subprocess.Popen(['eos', const.eosPath, 'ls', signalPath], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdoutFirst,stderr = out.communicate()
        fileList = []
        for signalFolderName in stdoutFirst.split():
            if "SKIM_NMSSM_XYH_bbbb" in signalFolderName:
                signalOutputPath = signalPath + "/" + signalFolderName + "/output/"
                out = subprocess.Popen(['eos', const.eosPath, 'ls', signalOutputPath], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                stdoutSecond,stderr = out.communicate()
                for signalFileName in stdoutSecond.split():
                    fileList.append(const.eosPath + "/" + signalOutputPath + signalFileName)
else:
    fileList = [singleFile] 


# loading formula
with open(modelFileName) as reweighterInputFile:
    theReweightModelAndTransferFactor = pickle.load(reweighterInputFile)

skimFileListOfList = [[] for i in range(threadNumber)]

listNumber = 0
for fileName in fileList:
    if ".root" in fileName:
        skimFileListOfList[listNumber].append(fileName)
        listNumber = listNumber + 1
        if listNumber >= threadNumber: 
            listNumber = 0

threads = list()
for index in range(threadNumber):
    x = threading.Thread(target=ApplyBDTweightsToFileList, args=(skimFileListOfList[index], const.treeName, trainingVariables, theReweightModelAndTransferFactor, backgroundWeightName, mode, seed))
    threads.append(x)
    x.start()

for thread in threads:
    thread.join()

