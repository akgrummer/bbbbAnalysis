import os
import sys
import argparse

parser = argparse.ArgumentParser(description='Command line parser of skim options')
parser.add_argument('--cfg'       ,  dest = 'cfg'       ,  help = 'config file filelist'     ,  required = True        )
parser.add_argument('--tag'       ,  dest = 'tag'       ,  help = 'production tag'           ,  required = True        )

args = parser.parse_args()

jobsDir                = 'CondorJobs/jobsFill_' + args.tag
outScriptNameBareProto = 'job_{0}.sh'
outScriptNameProto     = (jobsDir + '/' + outScriptNameBareProto)

sampleFileName    = "sampleCfg.cfg"
selectionFileName = "selectionCfg.cfg"
configFileName    = "config.cfg"
listOfSampleTypes = ["data", "datadriven", "backgrounds", "signals"]
outputHistogramFolder = "DataPlots"

def getMergedSampleList(inputCfgName):
    listOfMergedSamples = []
    isInMergedSession = False
    with open(inputCfgName) as inputFile:
        for line in inputFile.readlines():
            if "[merge]" in line:
                isInMergedSession = True
                continue
            if not isInMergedSession: continue
            key, value = line.rstrip("\n").split("=")
            key = ''.join(key.split())
            listOfSamples = value.split(",")
            theNewListOfSamples = []
            for sample in listOfSamples:
                sample = ''.join(sample.split())
                theNewListOfSamples.append(sample)
            listOfMergedSamples.append((key, theNewListOfSamples))
        inputFile.close()
    return listOfMergedSamples

def getSampleList(inputCfgName):
    listOfMergedSamples = getMergedSampleList(inputCfgName)
    typeOfMergedSample = {}
    for mergedSample in listOfMergedSamples:
        typeOfMergedSample[mergedSample[0]] = ""
    listOfSamples = []

    with open(inputCfgName) as inputFile:
        for line in inputFile.readlines():
            if "=" not in line: continue
            if "#" in line: continue
            key, value = line.rstrip("\n").split("=")
            key = ''.join(key.split())
            if key not in listOfSampleTypes: continue
            currentistOfSamples = value.split(",")
            for sample in currentistOfSamples:
                sample = ''.join(sample.split())
                isAmongMerged = False
                for mergedSample in listOfMergedSamples:
                    if sample in mergedSample[1]:
                        isAmongMerged = True
                        if typeOfMergedSample[mergedSample[0]] == "": typeOfMergedSample[mergedSample[0]] = key
                        if typeOfMergedSample[mergedSample[0]] != key:
                            print( "Merged samples are of different type!!!")
                            exit(1)
                        break
                if isAmongMerged: continue
                listOfSamples.append( (key, [sample], "", [""]) )
                # print( listOfSamples[-1][0], listOfSamples[-1][1], listOfSamples[-1][2], listOfSamples[-1][3])
        inputFile.close()

    for mergedSample in listOfMergedSamples:
        listOfSamples.append((typeOfMergedSample[mergedSample[0]], mergedSample[1], mergedSample[0], mergedSample[1]))
        # print( listOfSamples[-1][0], listOfSamples[-1][1], listOfSamples[-1][2], listOfSamples[-1][3])

    return listOfSamples

theListOfSamples = getSampleList(args.cfg)
bbbbWorkDir  = os.getcwd()

for sample in theListOfSamples:
    sampleName = sample[1][0]
    if sample[2] != "":  sampleName = sample[2]
    command = "%s/scripts/t3el7submit %s" % (bbbbWorkDir, outScriptNameProto.format(sampleName))
    if os.system(command) != 0:
        print( "... Not able to execute command \"", command, "\", exit")
        sys.exit()
