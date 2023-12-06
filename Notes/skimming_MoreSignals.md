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

using:
./scripts/submitAllSkimsOnTier3_moreSignals_mX650.sh
based on the orig file discussed above:
./scripts/submitAllSkimsOnTier3_2017_moreSignals.sh

