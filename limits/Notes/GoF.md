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

# to submit the jobs (LOCALLY)
run:
from screen
source an-scripts/GoFsubmit2016.sh
source an-scripts/GoFsubmit2017.sh
source an-scripts/GoFsubmit2018.sh


# for GRID submit:

python prepareModels/SubmitGoF.py --tag 2023Feb28_hourglass_VR_ws --tagid 1 --year 2016 --group auto
python prepareModels/SubmitGoF.py --tag 2023Jul5_VR --tagid 1 --year 2016 --group auto

python scripts/getTaskStatus.py --dir CondorJobs/jobsLimits_2023Feb28_hourglass_VR_ws/ --long



# !!!!In order to Run Workspaces on the grid:!!!!
1. need to have limits config up to date.
2. Need to have the prepareModels/listOfSamples.txt ready
3. Need to used the correct tag in the SubmitAllWorkspaces.sh
- make sure normalization values are correct in both Workspaces submit and GOF submit scripts
source prepareModels/SubmitAllWorkspaces.sh

For workspaces all mass points are about at the limit of 512 (so some are held)
ran all mass points at
1024 MB


# for GOF jobs:

need right diretory in config file
Need to have the right tag, and point to correct samplelist:
source prepareModels/SubmitAllGoF.sh


# for Plotting:

need correct tag and run:
source prepareModels/mergeAllGOFs.sh

# Added fixsig option to GoF jobs
use
--fixsig <value>
where value will probabaly always be 0
a new jobs dir is created, output GOF root files will have a "_sig<value>" tag added to the name

- have to exclude the sig0 files from the hadd
sig0 files need to be moved to a separate folder on eos


# !!!!In order to Run Workspaces on the grid:!!!!
1. need to have limits config up to date.
2. Need to have the prepareModels/listOfSamples.txt ready
3. Need to used the correct tag in the prepareModels/SubmitAllWorkspaces.sh
- make sure normalization values are correct in both Workspaces submit and GOF submit scripts
source prepareModels/SubmitAllWorkspaces.sh

USED 1024M in t3 script
(a few jobs hit the 512 limit)

for nonClosureMCStats:
    removed hourglass unc lines from config files

# for GOF jobs:

1. need right diretory in config file
2. Need to have the right tag, and point to correct samplelist:
3. USED 512M in t3 script
source prepareModels/SubmitAllGoF.sh

after jobs are done - run:
Use the right tags (for comparison and new one):
source ./prepareModels/mergeAllGOFs.sh

# for FitDiagnositics:

1. Need to have the right tag, and point to correct samplelist:
2. USED 512M in t3 script
doesn't depend on limitConfig files (but probably needs the workspace run first)
source ./prepareModels/SubmitAllFitDiagnostic.sh


# 2023 Dec 11

already have submitted limits for SR - but STILL need to submit workspace (!)
2023Dec7_binMYx2_addMX650_10ev_SR

## followed workspace submit instructions above for VR

task status doesn't work for workspace jobs

tag="2023Dec7_binMYx2_addMX650_10ev"; region="VR"; ayear=2018; grep -Eir --color=always "error" CondorJobs/jobsLimits_${tag}_${region} | egrep -v "is zero" | egrep -v "*ignored*" | egrep -iv "Analysing"| egrep -iv "Notes" | egrep -iv "CMSHistErrorPropagator"

followed GOF submit for VR - won't look at output though. (not actually interested)
acually - just canceled these jobs.

## submitted fit diagnostics for VR

followed instructions above
ERRORS in 2016 and 2017 mx1600, my=125 - probably because the bins are cut there
tag="2023Dec7_binMYx2_addMX650_10ev"; region="VR"; ayear=2018; grep -ir "error" CondorJobs/FitDiagnostics/jobsLimits_${tag}_${region}_${ayear}_0_sig0/

## submitted fit diagnostics for SR

followed instructions above
(needed to run workspace for SR even tho limits were already done)

no errors, some warnings
tag="2023Dec7_binMYx2_addMX650_10ev"; region="SR"; ayear=2018; grep -ir "error" CondorJobs/FitDiagnostics/jobsLimits_${tag}_${region}_${ayear}_0_sig0/
tag="2023Dec7_binMYx2_addMX650_10ev"; region="SR"; ayear=2018; grep -ilr "warning" CondorJobs/FitDiagnostics/jobsLimits_${tag}_${region}_${ayear}_0_sig0/

```
CondorJobs/FitDiagnostics/jobsLimits_2023Dec7_binMYx2_addMX650_10ev_SR_2018_0_sig0/job_sig_NMSSM_bbbb_MX_1000_MY_800.sh_4014454.stdout:[WARNING]: Unable to determine uncertainties on all fit parameters in s+b fit. The option --saveWithUncertainties will be ignored as it would lead to incorrect results. Have a look at https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/part3/nonstandard/#fit-parameter-uncertainties for more information.
```
not sure how problematic this is...


