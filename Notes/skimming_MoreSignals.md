# Add 2017 mX,mY 1000,150 mass point

ADD PU file:

The mX,mY = 1000,150 point was missing in the orig analysis chain (some corruption in the production)

The PU weight files were produced (by Fabio) with the commands in:
scripts/calculateAllPileupHistograms.sh
to apply PU weights used: `scripts/computeAllPUWeights.sh`

for More Signals run
source ./scripts/computeMoreSignalsPUWeights.sh
should point to the correct PU weight files - based on year and up/down variation

points to
./bin/get_sample_PU_weights.exe
which is compiled from source:
looseFiles/FromFabio/test/get_sample_PU_weights.cpp

have to have setup b2 analysis area first

ADD skimming:

skim_ntuple.exe --cfg config/Resonant_NMSSM_bbbb/skim_2016Resonant_NMSSM_XYH_bbbb_Fast.cfg --input inputFiles/2016_NMSSM_XYH_bbbb_Datasets/NMSSM_XYH_bbbb_MX_700_NANOAOD_v7.txt --output test_NMSSM_XYH_bbbb_MC.root --is-signal --xs=1 --puWeight weights/2016_NMSSM_XYH_bbbb_weights/NMSSM_XYH_bbbb_MX_300_NANOAOD_v7_PUweights.root --maxEvt 100000

get_sample_PU_weights.exe --realPU weights/Collision17PileupHistogram.root --realPU_up weights/Collision17PileupHistogramUp.root --realPU_down weights/Collision17PileupHistogramDown.root --input inputFiles/2017_NMSSM_XYH_bbbb_Datasets/NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full.txt  --outputFolder=weights/2017_NMSSM_XYH_bbbb_weights

skim_ntuple.exe --cfg config/Resonant_NMSSM_bbbb/skim_2016Resonant_NMSSM_XYH_bbbb_Fast.cfg --input inputFiles/2016_NMSSM_XYH_bbbb_Datasets/NMSSM_XYH_bbbb_MX_700_NANOAOD_v7.txt --output test_NMSSM_XYH_bbbb_MC.root --is-signal --xs=1 --puWeight weights/2016_NMSSM_XYH_bbbb_weights/NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_PUweights.root --maxEvt 100000

skim_ntuple.exe --cfg config/Resonant_NMSSM_bbbb/skim_2016Resonant_NMSSM_XYH_bbbb_Fast.cfg --input inputFiles/2017_NMSSM_XYH_bbbb_Datasets/NMSSM_XYH_bbbb_MX_900_NANOAOD_v7.txt --output test_NMSSM_XYH_bbbb_MC.root --is-signal --xs=1 --puWeight weights/2017_NMSSM_XYH_bbbb_weights/NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_PUweights.root --maxEvt 100000 --yMassSelection=125

skim_ntuple.exe --input=inputFiles/2016_NMSSM_XYH_bbbb_Datasets/NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full.txt   --cfg=config/Resonant_NMSSM_bbbb/skim_2016Resonant_NMSSM_XYH_bbbb.cfg  --puWeight=weights/2016_NMSSM_XYH_bbbb_weights/NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_PUweights.root  --is-signal --xs=0.1   --output test_NMSSM_XYH_bbbb_MC.root --yMassSelection=125  --maxDeltaR=0.25 --maxEvt 100000


# Fabio submited these with:

scripts/submitAllSkimsOnTier3_2016.sh
scripts/submitAllSkimsOnTier3_2017.sh

python scripts/submitSkimOnTier3.py --input=inputFiles/2017_NMSSM_XYH_bbbb_Datasets/NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full.txt  --tag=$1 --append=_MY_150  --cfg=config/Resonant_NMSSM_bbbb/skim_2017Resonant_NMSSM_XYH_bbbb.cfg  --puWeight=weights/2017_NMSSM_XYH_bbbb_weights/NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_PUweights.root --is-signal --xs=0.01  --njobs=2 --yMassSelection=150  --no-tar --no-xrdcp-tar --maxDeltaR=0.25

### separate options used by Fabio
python scripts/submitSkimOnTier3.py
    --input=inputFiles/2017_NMSSM_XYH_bbbb_Datasets/NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full.txt
    --tag=$1
    --append=_MY_150
    --cfg=config/Resonant_NMSSM_bbbb/skim_2017Resonant_NMSSM_XYH_bbbb.cfg
    --puWeight=weights/2017_NMSSM_XYH_bbbb_weights/NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_PUweights.root
    --is-signal
    --xs=0.01
    --njobs=2
    --yMassSelection=150
    --no-tar
    --no-xrdcp-tar
    --maxDeltaR=0.25

### possible options for: python scripts/submitSkimOnTier3.py
--input
--tag
--append
--executable
--njobs
--outputName
--outputDir
--no-tar
--no-xrdcp-tar
--no-xrdcp-flist
--dry-run
--verbose
--force


### setup options for local skim
'skim_ntuple.exe
    --input=MoreSignals/NMSSM_XYH_bbbb_MX_1000_MY_150_NANOAOD_v7_2017.txt
    --cfg=config/Resonant_NMSSM_bbbb/skim_2017Resonant_NMSSM_XYH_bbbb.cfg
    --puWeight=weights/2017_NMSSM_XYH_bbbb_weights_MoreSignals/NMSSM_XYH_bbbb_MX_1000_MY_150_NANOAOD_v7_2017_PUweights.root
    --is-signal
    --xs=0.01
    --output NMSSM_XYH_bbbb_MX_1000_MY_150_NANOAOD_v7_2017.root
    --maxDeltaR=0.25
'

# For Skimming - 2023 Nov 1
Running everything in scripts/submitAllSkimsOnTier3_2017_moreSignals.sh
- because we also needed the jec, jer, bjer...

source ./scripts/submitAllSkimsOnTier3_2017_moreSignals.sh

# 2023 Dec 5: PU computation

## get dataset

used firefox to access DAS with grid certificate (installed on browser from P12 file)
maybe this website was also useful:
https://cms-pdmv-prod.web.cern.ch/grasp/
have to sort of guess the right search patterns - could not recreate the search
pattern from for the 2017 MX1000 files (which I found in Sept.) but from there
I was able to guess the MX650 file names. So I really only used the DAS website
this time around.

retreive file lists for datasets from DAS with dasgoclient:
./GetMX650files.sh

## pileup weights

compute the PU weights with:
source ./scripts/computeMoreSignalsPUWeights.sh

9 ERRORs after running computeMoreSignalsPUWeights:
    [3000] Unable to open - cannot determine the prefix path
    in 6 datasets
    all output listed in Notes/computePUerrors.md
    repeated the PU computation for these files until no errors reported


Comparing PU root files in TBrowser:
`root -l $(find weights/MX650_MoreSignals/ -name "*.root") weights/2016_NMSSM_XYH_bbbb_weights/NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_PUweights.root weights/2016_NMSSM_XYH_bbbb_weights/NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_PUweights.root weights/2017_NMSSM_XYH_bbbb_weights/NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_PUweights.root weights/2017_NMSSM_XYH_bbbb_weights/NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_PUweights.root weights/2018_NMSSM_XYH_bbbb_weights/NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_PUweights.root weights/2018_NMSSM_XYH_bbbb_weights/NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_PUweights.root`

## for skimming:

using:<br>
./scripts/submitAllSkimsOnTier3_moreSignals_mX650.sh<br>
based on the orig file discussed above:<br>
./scripts/submitAllSkimsOnTier3_2017_moreSignals.sh

!! future note - should have used the same submission tag for all signal mass points<br>
ie `submitTag="moreSignals_mX650_mY${mYval}_${year}"` should not have the mY or year in it<br>
- just results in busier output in the eosls bbbb_ntuples directory

## failed skim jobs

for MX650 signals started at 60 jobs with at least one error

most (54) errors are that file is not able to open<br>
`Server responded with an error: [3000] Unable to open` one of the dataset files<br>
(sometimes the number 3000 is slightly different

found failed jobs with grep<br>
`grep -irl -e "Server responded with an error" -e "zombie" CondorJobs/skimming/`
```
CondorJobs/skimming/jobs_moreSignals_mX650_mY450_2018_Total_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-450_2018/job_1.sh_79737930.stdout:Error in <TNetXNGFile::Open>: [ERROR] Server responded with an error: [3000] Unable to open - cannot determine the prefix path to use for the given filesystem id /store/mc/RunIIAutumn18NanoAODv7/NMSSM_XToYHTo4B_MX-650_MY-450_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/Nano02Apr2020_102X_upgrade2018_realistic_v21-v2/70000/88076FDF-9AFF-BF40-BFC8-526FF3328832.root; invalid argument
```

additionally, some (7) errors are:<br>
`matrix is singular, 0 diag elements < tolerance of 2.2204e-16`
```
Error in <TDecompLU::DecomposeLUCrout>: matrix is singular
Error in <TDecompLU::InvertLU>: matrix is singular, 0 diag elements < tolerance of 2.2204e-16
```
but I think these are for single events - because it happens during event processing<br>
- so probably very minimal impact.<br>
files with the issue:<br>
```
>>> grep -irl "matrix is singular" CondorJobs/skimming/
CondorJobs/skimming/jobs_moreSignals_mX650_mY70_2016_bjer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-70_2016/job_0.sh_79737874.stdout
CondorJobs/skimming/jobs_moreSignals_mX650_mY100_2016_bjer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-100_2016/job_0.sh_79737875.stdout
CondorJobs/skimming/jobs_moreSignals_mX650_mY190_2016_bjer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-190_2016/job_0.sh_79737876.stdout
CondorJobs/skimming/jobs_moreSignals_mX650_mY250_2016_bjer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-250_2016/job_0.sh_79737877.stdout
CondorJobs/skimming/jobs_moreSignals_mX650_mY300_2016_bjer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-300_2016/job_1.sh_79737878.stdout
CondorJobs/skimming/jobs_moreSignals_mX650_mY500_2016_bjer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-500_2016/job_0.sh_79737880.stdout
CondorJobs/skimming/jobs_moreSignals_mX650_mY60_2017_bjer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-60_2017/job_1.sh_79737881.stdout
```

resubmitted failed skim jobs with<br>
`./Resub_2023Dec6.sh`<br>
(until file not found errors go away)<br>
- copies the log, stdout and stderr files to another folder and<br>
- then resubmits the sh script

- could also consider increasing the number of jobs (so there are fewer files to look up per job)<br>
in orignal submission: `./scripts/submitAllSkimsOnTier3_moreSignals_mX650.sh`<br>

### rsubmitting mX650_mY450_2018_Total_down

after 5 resubmissions got to one job failing. so rewrote `./scripts/submitAllSkimsOnTier3_moreSignals_mX650.sh` to `./scripts/submitAllSkimsOnTier3_moreSignals_mX650_mY450_2018_Total_down.sh`<br>
and resubmitted it with 6 jobs (3files per job) instead of 2 jobs <br>

no errors after resubmit:
```
[cmslpc117 Dec06 15:08:57 bbbbAnalysis]$ grep -ir -e "Server responded with an error" -e "zombie" CondorJobs/skimming/jobs_moreSignals_mX650_mY450_2018_njobs6_Total_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-450_2018/
[cmslpc117 Dec06 15:09:01 bbbbAnalysis]$ grep -ir "error" CondorJobs/skimming/jobs_moreSignals_mX650_mY450_2018_njobs6_Total_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-450_2018/
[cmslpc117 Dec06 15:09:14 bbbbAnalysis]$
```

files for this job:
`eosls -ltrh /store/user/agrummer/bbbb_ntuples/moreSignals_mX650_mY450_2018_njobs6_Total_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-450_2018/output`

### also resubmit mX650_mY350_2018_jer_up

one file is corrupted on the save for this (Error message in the skim output)

used:
`./scripts/submitAllSkimsOnTier3_moreSignals_mX650_mY350_2018_jer_up.sh`<br>

now with 6 jobs
grep -ir "error" CondorJobs/skimming/jobs_moreSignals_mX650_mY350_2018_jer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-350_2018/
grep -ir "error" CondorJobs/skimming/jobs_moreSignals_mX650_mY350_2018_njobs6_jer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-350_2018/

