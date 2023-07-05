data GoF:
run in screen
need to reinstantiate environment
from /localCombineRuns/CombineGoF_2023May9/2016

mkdir MX_900_MY_600
eoscp root://cmseos.fnal.gov//store/user/agrummer/bbbb_limits/2023Feb28_hourglass/HistogramFiles_2016/datacard_2016_sig_NMSSM_bbbb_MX_900_MY_600.txt MX_900_MY_600/
eoscp root://cmseos.fnal.gov//store/user/agrummer/bbbb_limits/2023Feb28_hourglass/HistogramFiles_2016/datacard_2016_sig_NMSSM_bbbb_MX_900_MY_600.root MX_900_MY_600/

text2workspace.py datacard.txt

combine -M GoodnessOfFit -n 2016_MX_900_MY_600 2016/datacard_2016_sig_NMSSM_bbbb_MX_900_MY_600.txt --algo=saturated >> Sat_2016_sig_NMSSM_bbbb_MX_900_MY_600_data.txt

combine -M GoodnessOfFit -n _2016_MX_400_MY_125 2016/datacard_2016_sig_NMSSM_bbbb_MX_400_MY_125.root --algo=saturated >> sat_2016_sig_NMSSM_bbbb_MX_400_MY_125_data.txt

toys:

started at 2:21
combine -M GoodnessOfFit -n _2016_MX_900_MY_600_TF 2016/datacard_2016_sig_NMSSM_bbbb_MX_900_MY_600.root --algo=saturated -t 1000 -s 12345 --toysFreq >> TFsat_2016_sig_NMSSM_bbbb_MX_900_MY_600_data.txt &






MX_400_MY_125
MX_600_MY_400
MX_700_MY_60
MX_800_MY_600
MX_900_MY_600
MX_1000_MY_800
MX_1200_MY_300
MX_1400_MY_900
MX_1600_MY_125
MX_1600_MY_700

to submit the jobs:
run:
from screen
source an-scripts/GoFsubmit2016.sh
source an-scripts/GoFsubmit2017.sh
source an-scripts/GoFsubmit2018.sh


for GRID submit:

python prepareModels/SubmitGoF.py --tag 2023Feb28_hourglass_VR_ws --tagid 1 --year 2016 --group auto

python scripts/getTaskStatus.py --dir CondorJobs/jobsLimits_2023Feb28_hourglass_VR_ws/ --long



!!!!In order to Run Workspaces on the grid:!!!!
1. need to have limits config up to date.
2. Need to have the prepareModels/listOfSamples.txt ready
3. Need to used the correct tag in the SubmitAllWorkspaces.sh
source prepareModels/SubmitAllWorkspaces.sh


for GOF jobs:

Need to have the right tag:
source prepareModels/SubmitAllGoF.sh

