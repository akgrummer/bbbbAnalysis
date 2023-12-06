# Notes for filling histograms

Submitted a fill on 2023Feb28
- The BDT names are messed up in 2017 and 2018 - the wrong weight names were saved in the root file:
They are:
`Weight_forBackground_BDTweights_2028Feb28`
`Weight_forBackground_BDTweights_2028Feb28_shapeUp`
`Weight_forBackground_BDTweights_2028Feb28_shapeDown`
- note the 2028 is not 2023.
The 2016 versions are correct with 2023Feb28


## resubmitting jobs:

To get the status:
python scripts/getTaskStatus.py --dir CondorJobs/jobsFill_fullSubmission_2018_BDTweights_2023Feb28/ --long

To get the resubmission script
python scripts/getTaskStatus.py --dir CondorJobs/jobsFill_fullSubmission_2018_BDTweights_2023Feb28/ --resubCmd

This script is suppose to issue the resubmission - but it send the same command 2 times. So I prefered to print the command and run it separately.
python scripts/getTaskStatus.py --dir CondorJobs/jobsFill_fullSubmission_2018_BDTweights_2023Feb28/ --issueCmd

Had to re-run 2 jobs, one of them twice, for signals:
sig_NMSSM_bbbb_MX_900_MY_250_3bScaled
sig_NMSSM_bbbb_MX_1400_MY_150_3bScaled


# Partial fills 2023Mar1

use a couple of signals, but all important analysis variables.

Weight_forBackground_BDTweights_2023Feb28_sans_mXmY
Weight_forBackground_BDTweights_2023Feb28_only_mXmY
Weight_forBackground_BDTweights_2023Feb28_sans_dfd
Weight_forBackground_BDTweights_2023Feb28_shapeUp_sans_dfd
Weight_forBackground_BDTweights_2023Feb28_shapeDown_sans_dfd

Weight_forBackground_BDTweights_2028Feb28_sans_mXmY
Weight_forBackground_BDTweights_2028Feb28_only_mXmY
Weight_forBackground_BDTweights_2028Feb28_sans_dfd
Weight_forBackground_BDTweights_2028Feb28_shapeUp_sans_dfd
Weight_forBackground_BDTweights_2028Feb28_shapeDown_sans_dfd


# for offshell:
submit with the submitAllfill
then
source ./scripts/mergeHistograms.sh 2023Mar23_offShell

source ./scripts/mergeHistograms.sh 2023Mar23_offShell_rebin

# Fill for 2023Jul5
edit and submit with the submitAllfillonTier3_RunII.sh
in the shell script submitAllfillonTier3_RunII.sh:
need to edit the (1) cfg file and (2) the tag accordingly
now submitting jobs for both the Limits plotting and Variable Plots at the same time

Submitting the jobs takes ~30 min - would be nicer to run the submissions in screen. Jobs don't take very long to complete.  Would be faster to tar the compiled cmssw and ship it with the jobs instead of compile each separately (like done in the GoF)

for Variable plots:
config/Resonant_NMSSM_bbbb/plotter_2016Resonant_NMSSM_XYH_bbbb_vars.cfg
for plots for Limits:
config/Resonant_NMSSM_bbbb/plotter_2016Resonant_NMSSM_XYH_bbbb_Full.cfg

using the same selection cfg files for both sets of jobs

Memory request in t3submit script is set to 512M

Then: main merge takes ~10/15 min
source ./scripts/mergeHistograms.sh 2023Jul5
source ./scripts/mergeHistograms.sh 2023Jul5_vars

# for 2023Jul5_binX4

edited the bin arrays for the 2D plots (not the corresponding 1D plots)
in the selection config files
use the same:
config/Resonant_NMSSM_bbbb/plotter_2016Resonant_NMSSM_XYH_bbbb_Full.cfg

Memory request in t3submit script is set to 512M

Then: main merge takes ~10/15 min
source ./scripts/mergeHistograms.sh 2023Jul5_binX4

# for 2023Jul5_binMYx2

same instructions as binX4
and change tag here
scripts/submitAllFillOnTier3_RunII.sh

source ./scripts/mergeHistograms.sh 2023Jul5_binMYx2

# for 2023Jul5_binMYx2_MXx2

same instructions as binX4
and change tag here
scripts/submitAllFillOnTier3_RunII.sh

source ./scripts/mergeHistograms.sh 2023Jul5_binMYx2_MXx2

# for 2023Nov1_binMYx2_add2017Sig

added new Signal MC for 2017 mX=1000, mY=150
edited config/Resonant_NMSSM_bbbb/sampleCfg_2017Resonant_NMSSM_XYH_bbbb_all.cfg
added: sig_NMSSM_bbbb_MX_1000_MY_150  = plotterListFiles/2017Resonant_NMSSM_XYH_bbbb/Signal/FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_150_rerun.txt

edited the bin arrays for the 2D plots for all years (not the corresponding 1D plots)
in the selection config files
-> nominal mX bins, mY bins x2


for plotter script, I think this was just for a study:
removed sig_NMSSM_bbbb_*_3bScaled
config/Resonant_NMSSM_bbbb/plotter_2016Resonant_NMSSM_XYH_bbbb_Full.cfg

and change tag here
scripts/submitAllFillOnTier3_RunII.sh

source ./scripts/mergeHistograms.sh 2023Nov1_binMYx2_add2017Sig

