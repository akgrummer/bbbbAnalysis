# Notes for Unrolling:

Unrolling for the full analysis study is done with:
`source ./scripts/UnrollAllSubdir.sh`
This unrolls the signal region and the validation region

- Unrolling should be done in screen (takes ~4-5 hrs)

- After unrolling need to correct for the shape
To run the background shape calculation:
root -l
.L ./scripts/calculateAllBKGshape.C++
calculateAllBKGshape("2023Feb28_3", "fullSubmission_2022Nov/")

- Next need to calculate normalization uncertainty:
```
.L scripts/MeasureBackgroundSystematic.C++
doMeasureNorm("2023Feb28_3", 2016)
doMeasureNorm("2023Feb28_3", 2017)
doMeasureNorm("2023Feb28_3", 2018)
```

