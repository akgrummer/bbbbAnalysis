import os
import argparse

pedestal   = 0.01
slope      = 2e-5
multiplier = 1.5


def getLineFormatted(txtarr, align='{:>25}', firstAlign = '{:<35}', secondAlign = '{:<6}', addEmptyAtIdx = None):
    if addEmptyAtIdx:
        txtarr = txtarr[0:addEmptyAtIdx] + [''] + txtarr[addEmptyAtIdx:]
    str_proto = ''
    for idx, txt in enumerate(txtarr):
        str_proto += '%s ' % (firstAlign if idx == 0 else secondAlign if idx == 1 else align)
    str_proto = str_proto[:-1] ## remove trailing space
    the_str = str_proto.format(*txtarr)
    return the_str

def getXmass(sampleName):
    begin = 'sig_NMSSM_bbbb_MX_'
    separator = "_MY_"
    mX = int(sampleName[len(begin) : sampleName.find(separator)])
    return mX


parser = argparse.ArgumentParser(description='Command line parser of skim options')
parser.add_argument('--inputDatacard', dest='inputDatacard', help='Datacard to update', required = True)
parser.add_argument('--sampleName'   , dest='sampleName'   , help='Sample name'       , required = True)

args = parser.parse_args()
inputDatacardFileName = args.inputDatacard
sampleName            = args.sampleName

inputDatacardFile = open(inputDatacardFileName, 'r+')

xMass = getXmass(sampleName)
uncertainty = ((pedestal + slope*xMass ) * multiplier) + 1

outputFileString = ""


line_tokens = ['CMS_LHE_pdf', 'lnN']
line_tokens.append('%.3f' % (uncertainty))
line_tokens.append('-')
systematicLine = getLineFormatted(line_tokens)

for line in inputDatacardFile:
    if "autoMCStats" in line:
        outputFileString += systematicLine
        outputFileString += "\n"
    outputFileString += line

inputDatacardFile.seek(0)
inputDatacardFile.write(outputFileString)