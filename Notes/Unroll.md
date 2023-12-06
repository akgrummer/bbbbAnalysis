# Notes for Unrolling:

(1) Unrolling for the full analysis study is done with:
`source ./scripts/UnrollAllSubdir.sh`
Edit the Tag in that script
This unrolls the signal region and the validation region

- Unrolling should be done in screen (takes ~4-5 hrs)
- max Mem is 6.8GB, can this be done better??
- used ~/memorylog.sh in a separate screen session to monitor mem usages

(2) Next need to calculate normalization uncertainty:
also in vim-sessions/NormUnc.vim
```
.L scripts/MeasureBackgroundSystematic.C++
doMeasureNorm("2023Feb28_3", 2016)
doMeasureNorm("2023Feb28_3", 2017)
doMeasureNorm("2023Feb28_3", 2018)
```

(3) For Validation test: use
root -l './scripts/modifyAllPlotForValidationTest.C("v34_aidan_2021Dec21")'
root -l -q './scripts/modifyAllPlotForValidationTest.C("2022Oct25_ValRegTrain_bJetLoose_VR", "fullSubmission_2022July/")'
root -l -q './scripts/modifyAllPlotForValidationTest.C("2023Feb28_3_hourglass_unc_VR", "fullSubmission_2022Nov/")'

root -l -q './scripts/modifyAllPlotForValidationTest.C("2023Feb28_3_trim_VR", "fullSubmission_2022Nov/")'
root -l -q './scripts/modifyAllPlotForValidationTest.C("2023Feb28_3_VR", "fullSubmission_2022Nov/")'
root -l -q './scripts/modifyAllPlotForValidationTest.C("2023Jul5_VR", "fullSubmission_2022Nov/")'



(4) After unrolling need to correct for the shape
!! If changing to VR instead of SR need to apply that step first
To run the background shape calculation:
root -l
.L ./scripts/calculateAllBKGshape.C++
calculateAllBKGshape("2023Feb28_3", "fullSubmission_2022Nov/")
calculateAllBKGshape("2023Feb28_3_trim", "fullSubmission_2022Nov/")

!!! Run the modify for VR first if needed
root -l -q './scripts/calculateAllBKGshape.C("2023Feb28_3_trim_VR", "fullSubmission_2022Nov/")'
root -l -q './scripts/calculateAllBKGshape.C("2023Feb28_3_VR", "fullSubmission_2022Nov/")'
root -l -q './scripts/calculateAllBKGshape.C("2023Feb28_3_trim", "fullSubmission_2022Nov/")'
root -l -q './scripts/calculateAllBKGshape.C("2023Jul5_SR", "fullSubmission_2022Nov/")'
root -l -q './scripts/calculateAllBKGshape.C("2023Jul5_VR", "fullSubmission_2022Nov/")'



(5) - Also need to add the hourglass uncertainty - see vim-sessions/hourglassUnc.vim
and still apply the hourglass uncertainty after (after bkg shape, or before? maybe that doesnt matter)





# 2023 July 18

unrolling is now and all shapes (SR and VR) are now completed here:

source ./scripts/UnrollAllSubdir.sh

just need to add the normalization step:


# 2023 Aug 17.

using this script for saving the unrolled locations of mX and mY
Validation and Signal region seem to give the same results - but only going to save the Validation regions now
scripts/Unroll2DplotsSubRange_dev_saveLocation.cc

# 2023 Aug 25

use script to double the bkg stats uncertainty
scripts/Unroll2DplotsSubRange_dev_doubleMCStats.cc

# 2023 Aug 30

using the script now for adding HG uncertainty to the stats unc. for MC bin by bin unc.
scripts/Unroll2DplotsSubRange_dev_doubleMCStats.cc

# Sep 18
2023Jul5_binMYx2_MXx2
had to run save location version separately
TARGET=Unroll2DplotsSubRange_dev_saveLocation # the faster version _dev

# Sep 19
merged save location cc and double MC Stats cc in to:
scripts/Unroll2DplotsSubRange_dev_hourglassMCStats_lowStatsCuts.cc

# Sep 26:

applyed the low stats cut in the .cc code above
HH_kinFit_m:H2_m@H2_m     = 36, 51, 62, 70, 78, 86, 94, 102, 110, 122, 140, 156, 172, 188, 204, 228, 260, 292, 324, 356, 388, 444, 508, 572, 636, 700, 764, 892, 1020, 1148, 1276, 1404, 1564, 1820, 2076, 2204
HH_kinFit_m:H2_m@HH_kinFit_m     = 212, 228, 244, 260, 276, 292, 308, 324, 340, 360, 392, 424, 456, 488, 520, 552, 584, 616, 648, 704, 768, 832, 896, 960, 1024, 1088, 1152, 1216, 1296, 1424, 1552, 1680, 1808, 1936, 2064, 2192, 2320

TAG=2023Jul5_binMYx2_ncMCStats_lowStatsCut
source ./scripts/UnrollAllSubdir.sh

- applied a second set of cuts and named it:
TAG=2023Jul5_binMYx2_ncMCStats_lowStatsCut_5ev

- applied a second set of cuts and named it:
TAG=2023Jul5_binMYx2_ncMCStats_lowStatsCut_10ev


# 2023 Dec 4:

adding 2017 signal mass point
using the 10 ev bin low stats cuts
filling hists to the original tag and then moving the hist root file to a new folder with commands like:

myyear=2018; ls -ltrh VarPlots/rootHists/fullSubmission_2022Nov/${myyear}DataPlots_2023Nov1_binMYx2_add2017Sig/
myyear=2018; mkdir VarPlots/rootHists/fullSubmission_2022Nov/${myyear}DataPlots_2023Nov1_binMYx2_add2017Sig_10ev

myyear=2018; mv VarPlots/rootHists/fullSubmission_2022Nov/${myyear}DataPlots_2023Nov1_binMYx2_add2017Sig/outPlotter.root VarPlots/rootHists/fullSubmission_2022Nov/${myyear}DataPlots_2023Nov1_binMYx2_add2017Sig_10ev/


update tag and run
source ./scripts/UnrollAllSubdir.sh

uses
scripts/Unroll2DplotsSubRange_dev_hourglassMCStats_lowStatsCuts.cc
saves the location files already


