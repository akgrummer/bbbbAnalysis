# Produce Results

among other things
produceAllResults can be used
- to merge the limit results
- plot the limit results
- compare 2 limit results
- compare 3 limit results


source ./an-scripts/produceAllResults.sh

# 2023 Dec 14

unblinding limits:

./an-scripts/unblindingLimits_2023Dec14.sh

# 2023 Dec 15

computed pulls of the observed limits:
an-scripts/produceMeanLimitPlots.sh

# 2023 Dec18
2d limit map:

for significance:
./an-scripts/produce2DlimitMap.sh
runs:
./an-scripts/PlotSignificanceFromCondor.cc
and
./an-scripts/Plot2DSignificanceMap.C

and
an-scripts/PlotSignficanceDist.py



# 2023 Jan29:

overlay the pseudoData crosscheck
an-scripts/unblindingLimits_2023Dec14_pseudoDatasetOverlay.sh

# 2023 Apr 5

reruning with the limits produced from the full plane background (instigated for the LEE global significance study)
2023Dec7_binMYx2_addMX650_10ev_fullPlane_SR
the full plane limits were not produced with impacts though - would need to add that option. see LEE vim session
./an-scripts/produceAllResults.sh


