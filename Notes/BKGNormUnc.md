# the Background Normalization Uncertainty

this is determined with
scripts/MeasureBackgroundSystematic.C

doMeasureNorm(std::string tagName, int year)

if you make changes you need to recompile:

root -l
.L scripts/MeasureBackgroundSystematic.C++
doMeasureNorm("2022Nov14_bJetScoreLoose_shapes2", 2016)
doMeasureNorm("2023Jul5", 2016)
doMeasureNorm("2023Jul5", 2017)
doMeasureNorm("2023Jul5", 2018)

This code has to be run without "AidanStyle"
- the stat box isn't printed on the plot
- The uncertainty band is not displayed
Done be temporarily renaming the rootlogon.C script in bbbbAnalysis folder




