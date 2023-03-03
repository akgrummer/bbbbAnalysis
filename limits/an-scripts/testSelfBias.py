import subprocess as sp
import os
import argparse
from  ConfigParser import *
from StringIO import StringIO
import ast
import time

parser = argparse.ArgumentParser(description='Command line parser of skim options')
parser.add_argument('--config',    dest='cfgfile',        help='Name of config file with MC information',   required = True)
parser.add_argument('--signal',    dest='signal',         help='Name of the signal'                     ,   required = True)
parser.add_argument('--injRange',  dest='injRange' ,      help='signal injection injRange'              ,   required = True)
parser.add_argument('--group',     dest='group',          help='group'                                  ,   required = True)
args = parser.parse_args()
configFileName = args.cfgfile
signal         = args.signal
injRange       = args.injRange

with open(configFileName) as templateConfiguration:
	signalConfiguration = templateConfiguration.read()
signalConfiguration = signalConfiguration.replace("${signalTemplate}",args.signal)
cfgparser = ConfigParser()
cfgparser.optionxform = lambda option: option # preserve lower-upper case
cfgparser.readfp(StringIO(signalConfiguration))

folder       = ast.literal_eval(cfgparser.get("configuration","folder"))
categandobs  = ast.literal_eval(cfgparser.get("configuration","categandobs"))
datasetYear  = ast.literal_eval(cfgparser.get("configuration","dataset"))

os.system("rm -rf " + folder)
os.system("mkdir -p " + folder)

createFileTastCommand = "python prepareModels/prepareHistos.py  --config " + configFileName + " --signal " + signal + " --group " + args.group
createPlotTask = sp.Popen(createFileTastCommand.split(), stdout=sp.PIPE)
streamdata = createPlotTask.communicate()[0]
codeReturned = createPlotTask.returncode
if codeReturned != 0:
    print "createPlotTask failed, Aborting"
    print streamdata
    sys.exit(-1)

# create datacard and workspace
print "[INFO] Creating datacard and workspace . . ."

makeDatacardTaskCommand = "python prepareModels/makeDatacardsAndWorkspaces.py --config " + configFileName + " --no-comb --no-bbb --addScaleSignal --signal " + signal + " --bkgNorm 0"
makeDatacardTask = sp.Popen(makeDatacardTaskCommand.split(), stdout=sp.PIPE)
streamdata = makeDatacardTask.communicate()[0]
codeReturned = makeDatacardTask.returncode
if codeReturned != 0:
    print "makeDatacardTask failed, Aborting"
    print streamdata
    sys.exit(-1)

time.sleep(1)

if injRange == "1": injectionStrengthList   = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0]
if injRange == "2": injectionStrengthList   = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 12.0]
if injRange == "3": injectionStrengthList   = [2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0]
if injRange == "4": injectionStrengthList   = [3.0, 6.0, 9.0, 12.0, 15.0, 18.0, 21.0, 24.0, 27.0, 30.0]
if injRange == "5": injectionStrengthList   = [4.0, 8.0, 12.0, 16.0, 20.0, 24.0, 28.0, 32.0, 36.0, 40.0]
if injRange == "6": injectionStrengthList   = [8.0, 16.0, 24.0, 32.0, 40.0, 48.0, 56.0, 64.0, 72.0, 80.0]
toys     = 1000

# categandobs= [["selectionbJets_SignalRegion","HH_kinFit_m_H2_m"]]
# datasetYear='2016'
workSpaceName = "datacard" + datasetYear + "_" + categandobs[0][0] + ".root"
# folder='/uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/limits/SelfBiasTest2016/sig_NMSSM_bbbb_MX_400_MY_80'
mainDirectory = os.getcwd()
print("DEBUG: ",mainDirectory)
os.chdir(folder)
print("DEBUG: ",folder)
print "[INFO] Running limit . . ."
# workSpaceName = "SelfBiasTest2016/sig_NMSSM_bbbb_MX_400_MY_80/datacard2016_selectionbJets_SignalRegion.root"
# workSpaceName = "datacard2016_selectionbJets_SignalRegion.root"
makeLimitCommand = "combine -M AsymptoticLimits -D data_obs --run blind --setParameters r=1,myscale=0 --freezeParameters allConstrainedNuisances " + workSpaceName
makeLimitTask = sp.Popen(makeLimitCommand.split(), stdout=sp.PIPE)
streamdata = makeLimitTask.communicate()[0]
codeReturned = makeLimitTask.returncode
