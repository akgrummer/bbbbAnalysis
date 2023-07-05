# Notes for Unrolling:

Unrolling for the full analysis study is done with:
`source ./scripts/UnrollAllSubdir.sh`
This unrolls the signal region and the validation region

- Unrolling should be done in screen (takes ~4-5 hrs)

- After unrolling need to correct for the shape
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

- Also need to add the hourglass uncertainty - see vim-sessions/hourglassUnc.vim

- Next need to calculate normalization uncertainty:
```
.L scripts/MeasureBackgroundSystematic.C++
doMeasureNorm("2023Feb28_3", 2016)
doMeasureNorm("2023Feb28_3", 2017)
doMeasureNorm("2023Feb28_3", 2018)
```


For Validation test: use
root -l './scripts/modifyAllPlotForValidationTest.C("v34_aidan_2021Dec21")'
root -l -q './scripts/modifyAllPlotForValidationTest.C("2022Oct25_ValRegTrain_bJetLoose_VR", "fullSubmission_2022July/")'
root -l -q './scripts/modifyAllPlotForValidationTest.C("2023Feb28_3_hourglass_unc_VR", "fullSubmission_2022Nov/")'

root -l -q './scripts/modifyAllPlotForValidationTest.C("2023Feb28_3_trim_VR", "fullSubmission_2022Nov/")'
root -l -q './scripts/modifyAllPlotForValidationTest.C("2023Feb28_3_VR", "fullSubmission_2022Nov/")'

and still apply the hourglass uncertainty after (after bkg shape, or before? maybe that doesn't matter)

