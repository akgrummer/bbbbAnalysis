# Notes for Unrolling full plane:

This is to target the global significance study LEE.

## previous script

An old script UnrollAll2Dplots.cc unrolled the full plane. Was run with `scripts/UnrollAll.sh`.

- it did not include the remove of low stats bins
- no hourglass uncertainty.
- no saving of the original bins (used later to re-roll)
- includes a bin correspondance plot (which I don't know what it is for and probably don't care)

* deciding to make a new unroll script based on
`scripts/Unroll2DplotsSubRange_dev_hourglassMCStats_lowStatsCuts.cc`

which does not include the mass group features. Of course it would be better if everything were moduler but there is no time.

## scripts

full plane unroll script(s):

scripts/Unroll2DplotsSubRange_dev_hourglassMCStats_lowStatsCuts_fullPlane.cc
scripts/calculateAllBKGshape_fullPlane.C
scripts/modifyAllPlotForValidationTest_fullPlane.C

shell script to run the full sequence:

./scripts/UnrollAllSubdir_FullPlane.sh


## running on new files

used this tag for unblind step:
2016DataPlots_2023Dec7_binMYx2_addMX650_10ev
TAG="2023Dec7_binMYx2_addMX650_10ev"

used
./scripts/Unroll_addTag.sh
to create tag
TAG="2023Dec7_binMYx2_addMX650_10ev_fullPlane"

adding background for VR had to be run twice. Really only care about SR for now, but VR is probably ok.

## 2024 Apr 1

ran:
./scripts/UnrollAllSubdir_FullPlane.sh
the unrolled plot in for model looks qualitativly correct or as I would expect. May be time consuming to prove it is truly correct by comparing to the subrange (mass group) unrolled plots.
Also, probably did not need mass groups at all after the rebinning campaign.


