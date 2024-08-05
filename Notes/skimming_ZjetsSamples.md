# Skimming for Z+jets files




scripts/calculateAllPileupHistograms.sh

rerun the skim:

bbbbAnalysis/scripts/submitAllSkimsOnTier3_2016.sh


inputFiles/2016_NMSSM_XYH_bbbb_Datasets/QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.txt

make sure the xs is correct
need to rerun pileup

pu weights:
https://github.com/akgrummer/bbbbAnalysis/blob/el9_cmssw10/scripts/computeAllPUWeights.sh
with correct txt file of filenames


https://github.com/akgrummer/bbbbAnalysis/blob/el9_cmssw10/scripts/submitAllSkimsOnTier3_2016.sh#L35


## get files from DAS

Got UL sample names from Jennet: nanoaod_zjets/2016_Zjets.json
Cross sections from Cristina's repo:
https://github.com/LPC-HH/HH4b/blob/main/src/HH4b/xsecs.py#L346-L349

inputFiles/Zjets/2016/
ZJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8

used this script to get file names after searching for the correct folders with:
dasgoclient -query="dataset=/ZJetsToQQ_HT*_TuneCP5_13TeV-madgraphMLM-pythia8/*UL17*/NANOAODSIM" |grep v9-v2
scripts/GetZjetsfiles.sh

had to make the year directories first:
mkdir inputFiles/Zjets/2016/
mkdir inputFiles/Zjets/2017/
mkdir inputFiles/Zjets/2018/
mkdir inputFiles/Zjets/2016preVFP/

## apply pileup weights with:

scripts/computeZjetsPUWeights.sh


run on el7image

output warnings
INFO] ... file list contains 44 files
[INFO] ... creating tree reader
Unable to load sec.protocol plugin libXrdSecztn.so
Warning in <TClass::Init>: no dictionary for class __pair_base<edm::Hash<1>,edm::ParameterSetBlob> is available
Info in <TCanvas::MakeDefCanvas>:  created default TCanvas with name c1
Unable to load sec.protocol plugin libXrdSecztn.so
Unable to load sec.protocol plugin libXrdSecztn.so

5 errors, reran the specific error files until fixed.


## skim submission:

run in el7image:
el9part="false"
and run in el9 with:
el9part="true"
./scripts/submitAllSkimsOnTier3_Zjets.sh

Set 1024M in:
scripts/t3el7submit

uses:
scripts/submitSkimOnTier3.py
and
scripts/submitSkimOnTier3_el9part.py




need correct xs numbers
need correct DeepCSV cuts:

from:
https://github.com/akgrummer/bbbbAnalysis/blob/el9_cmssw10/scripts/submitAllSkimsOnTier3_2016.sh#L35
python scripts/submitSkimOnTier3.py
    --input inputFiles/2016_NMSSM_XYH_bbbb_Datasets/QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.txt
    --tag=$1
    --cfg=config/Resonant_NMSSM_bbbb/skim_2016Resonant_NMSSM_XYH_bbbb.cfg
    --puWeight weights/2016_NMSSM_XYH_bbbb_weights/QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_PUweights.root
    --xs=1710000
    --njobs=100
    --no-tar
    --no-xrdcp-tar



## check for errors:

grep -irl -e "error" -e "zombie" CondorJobs/skimming/jobs_Zjets_*
grep -ir -e "error" CondorJobs/skimming/jobs_Zjets_*/ | awk '/error/ && !/Jet_nConstituents/'
grep -ir -e "** Warning - Branch" CondorJobs/skimming/jobs_Zjets_*/

grep -ir -e "error" CondorJobs/skimming/jobs_Zjets_*2/ | awk '/error/ && !/Jet_nConstituents/'
grep -ir -e "Segmentation fault" CondorJobs/skimming/jobs_Zjets_*2/

many files with  Jet_nConstituents branch type error
ignoring those three more errors:


CondorJobs/skimming/jobs_Zjets_2016_HT400to600/SKIM_ZJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/job_1.sh_33028601.stdout:Error in <TNetXNGFile::Open>: [ERROR] Server responded with an error: [3000] Unable to open - cannot determine the prefix path to use for the given filesystem id /store/mc/RunIISummer20UL16NanoAODv9/ZJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_mcRun2_asymptotic_v17-v2/2530000/E27C4F96-5612-A945-BACF-563B0A93708F.root; invalid argument

CondorJobs/skimming/jobs_Zjets_2016preVFP_HT400to600/SKIM_ZJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/job_1.sh_33028593.stdout:Error in <TBranch::GetBasket>: File: root://cmsxrootd.fnal.gov//store/mc/RunIISummer20UL16NanoAODAPVv9/ZJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v2/270000/9ECADDB1-E6D6-4E46-BB75-46E7BB24CE22.root at byte:40774272, branch:Pileup_nTrueInt, entry:21335, badread=4, nerrors=1, basketnumber=6

CondorJobs/skimming/jobs_Zjets_2017_HT200to400/SKIM_ZJetsToQQ_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/job_1.sh_33028607.stdout:Error in <TNetXNGFile::Open>: [ERROR] Server responded with an error: [3000] Unable to open - cannot determine the prefix path to use for the given filesystem id /store/mc/RunIISummer20UL17NanoAODv9/ZJetsToQQ_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_mc2017_realistic_v9-v2/50000/AB5FDBC9-7B01-0B42-8DC8-DF77302405CF.root; invalid argument

CondorJobs/skimming/jobs_Zjets_2016_HT400to600/SKIM_ZJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/job_1.sh
CondorJobs/skimming/jobs_Zjets_2016preVFP_HT400to600/SKIM_ZJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/job_1.sh
CondorJobs/skimming/jobs_Zjets_2017_HT200to400/SKIM_ZJetsToQQ_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/job_1.sh

resubmitted 3 jobs


repeated errors on second run:
CondorJobs/skimming/jobs_Zjets_2016_HT400to600/SKIM_ZJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/job_1.sh_33028601.stdout
CondorJobs/skimming/jobs_Zjets_2016_HT400to600/SKIM_ZJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/job_1.sh_3452688.stdout

CondorJobs/skimming/jobs_Zjets_2017_HT200to400/SKIM_ZJetsToQQ_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/job_1.sh_33028607.stdout
CondorJobs/skimming/jobs_Zjets_2017_HT200to400/SKIM_ZJetsToQQ_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/job_1.sh_3452690.stdout
CondorJobs/skimming/jobs_Zjets_2017_HT200to400/SKIM_ZJetsToQQ_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/job_1.sh_3452690.stdout



rerun, with many jobs:

CondorJobs/skimming/jobs_Zjets_2016_HT400to6002/SKIM_ZJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/job_20.sh_3452717.stdout:Error in <TNetXNGFile::Open>: [ERROR] Server responded with an error: [3000] Unable to open - cannot determine the prefix path to use for the given filesystem id /store/mc/RunIISummer20UL16NanoAODv9/ZJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_mcRun2_asymptotic_v17-v2/2530000/E27C4F96-5612-A945-BACF-563B0A93708F.root; invalid argument

CondorJobs/skimming/jobs_Zjets_2017_HT200to4002/SKIM_ZJetsToQQ_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/job_34.sh_3452823.stdout:Error in <TNetXNGFile::Open>: [ERROR] Server responded with an error: [3000] Unable to open - cannot determine the prefix path to use for the given filesystem id /store/mc/RunIISummer20UL17NanoAODv9/ZJetsToQQ_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_mc2017_realistic_v9-v2/50000/AB5FDBC9-7B01-0B42-8DC8-DF77302405CF.root; invalid argument

CondorJobs/skimming/jobs_Zjets_2017_HT200to4002/SKIM_ZJetsToQQ_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/job_32.sh_3452821.stdout:Error in <TNetXNGFile::Open>: [ERROR] Server responded with an error: [3000] Unable to open - cannot determine the prefix path to use for the given filesystem id /store/mc/RunIISummer20UL17NanoAODv9/ZJetsToQQ_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_mc2017_realistic_v9-v2/40000/F920CD7B-6B1F-0C44-928E-2CBEE6FB6E13.root; invalid argument

CondorJobs/skimming/jobs_Zjets_2018_HT600to8002/SKIM_ZJetsToQQ_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/job_42.sh_3453059.stdout:Error in <TNetXNGFile::Open>: [ERROR] Server responded with an error: [3000] Unable to open - cannot determine the prefix path to use for the given filesystem id /store/mc/RunIISummer20UL18NanoAODv9/ZJetsToQQ_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/80000/DD9A4215-A473-E244-B748-B9A1A0F21E4D.root; invalid argument


CondorJobs/skimming/jobs_Zjets_2016_HT400to6002/SKIM_ZJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/job_20.sh_3452717.stdout

CondorJobs/skimming/jobs_Zjets_2017_HT200to4002/SKIM_ZJetsToQQ_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/job_34.sh_3452823.stdout

CondorJobs/skimming/jobs_Zjets_2017_HT200to4002/SKIM_ZJetsToQQ_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/job_32.sh_3452821.stdout

CondorJobs/skimming/jobs_Zjets_2018_HT600to8002/SKIM_ZJetsToQQ_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/job_42.sh_3453059.stdout

dasgoclient -query="dataset=/ZJetsToQQ_HT*_TuneCP5_13TeV-madgraphMLM-pythia8/*UL17*/NANOAODSIM" |grep v9-v2
dasgoclient -query="filename=/RunIISummer20UL16NanoAODv9/ZJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_mcRun2_asymptotic_v17-v2/2530000/E27C4F96-5612-A945-BACF-563B0A93708F.root"


CondorJobs/skimming/jobs_Zjets_2016_HT400to6002/SKIM_ZJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/job_20.sh_3452717.stdout

CondorJobs/skimming/jobs_Zjets_2017_HT200to4002/SKIM_ZJetsToQQ_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/job_34.sh_3452823.stdout

CondorJobs/skimming/jobs_Zjets_2017_HT200to4002/SKIM_ZJetsToQQ_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/job_32.sh_3452821.stdout

CondorJobs/skimming/jobs_Zjets_2018_HT600to8002/SKIM_ZJetsToQQ_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/job_42.sh_3453059.stdout

CondorJobs/skimming/jobs_Zjets_2018_HT600to8002/SKIM_ZJetsToQQ_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/job_42.sh_65372808.stdout

grep -ir -e "Segmentation fault" CondorJobs/skimming/jobs_Zjets_2018*2/

