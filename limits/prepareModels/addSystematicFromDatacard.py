import os
import argparse

parser = argparse.ArgumentParser(description='Command line parser of skim options')
parser.add_argument('--inputDatacard'     , dest='inputDatacard'     , help='Datacard to update'              , required = True)
parser.add_argument('--systematicDatacard', dest='systematicDatacard', help='Datacard with systematic to copy', required = True)
parser.add_argument('--systematicName'    , dest='systematicName'    , help='Name of systematic to copy'      , required = True)
args = parser.parse_args()
inputDatacardFileName      = args.inputDatacard
systematicDatacardFileName = args.systematicDatacard
systematicName             = args.systematicName

systematicDatacardFile = open(systematicDatacardFileName, 'r')
systematicDatacardLines = systematicDatacardFile.readlines()

lineToCopy = ""
for line in systematicDatacardLines:
    if systematicName in line:
        lineToCopy = line
        break

if lineToCopy == "":
    print "Systematic ", lineToCopy, " not found in file ", systematicDatacardFile
    exit()


inputDatacardFile = open(inputDatacardFileName, 'r+')

outputFileString = ""

for line in inputDatacardFile:
    if "autoMCStats" in line:
        outputFileString += lineToCopy
        outputFileString += "\n"
    outputFileString += line

inputDatacardFile.seek(0)
inputDatacardFile.write(outputFileString)