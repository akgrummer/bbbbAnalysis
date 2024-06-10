TAG="2023Dec7_binMYx2_addMX650_10ev_fullPlane"
submissionDir=fullSubmission_2022Nov
TARGET=Unroll2DplotsSubRange_dev_hourglassMCStats_lowStatsCuts_fullPlane # saves bin locations, applies hourglass for MC stats, cut on stats
cd scripts && g++  -std=c++17 -I `root-config --incdir` -o ${TARGET} ${TARGET}.cc `root-config --libs` -O3 ; cd -
# cd scripts && g++  -std=c++17 -I `root-config --incdir` -o ${TARGET} ${TARGET}.cc `root-config  --cflags --glibs` -O3; cd -

#UNROLLING:
group=0
for YEAR in 2016 2017 2018; do
        ./scripts/${TARGET} VarPlots/rootHists/${submissionDir}/${YEAR}DataPlots_${TAG}/outPlotter.root data_BTagCSV_dataDriven_kinFit selectionbJets_SignalRegion HH_kinFit_m_H2_m ${group} selectionbJets_ValidationRegionBlinded &
        echo "started ${YEAR}\n"
done
wait
echo "finished unrolling"

## Split in to regions:
for YEAR in 2016 2017 2018; do
    mkdir -p VarPlots/rootHists/${submissionDir}/${YEAR}DataPlots_${TAG}_VR
    mkdir -p VarPlots/rootHists/${submissionDir}/${YEAR}DataPlots_${TAG}_SR
    cp VarPlots/rootHists/${submissionDir}/${YEAR}DataPlots_${TAG}/outPlotter_fullPlane* VarPlots/rootHists/${submissionDir}/${YEAR}DataPlots_${TAG}_VR/
    cp VarPlots/rootHists/${submissionDir}/${YEAR}DataPlots_${TAG}/outPlotter_fullPlane* VarPlots/rootHists/${submissionDir}/${YEAR}DataPlots_${TAG}_SR/
done;


# This comes before creating the backgrond shapes
doublequote=\"
singlequote=\'
# if running the command line - use single quotes to wrap the function and arguement, otherwise this method seems to work here
# FOR VALIDATION TEST
root -l -b -q "./scripts/modifyAllPlotForValidationTest_fullPlane.C(${doublequote}${TAG}_VR${doublequote}, ${doublequote}fullSubmission_2022Nov/${doublequote})"
# Now create the shape hists (up and down min and max...)
# #SHAPES
root -l -q "./scripts/calculateAllBKGshape_fullPlane.C(${doublequote}${TAG}_SR${doublequote}, ${doublequote}fullSubmission_2022Nov/${doublequote})"
root -l -q "./scripts/calculateAllBKGshape_fullPlane.C(${doublequote}${TAG}_VR${doublequote}, ${doublequote}fullSubmission_2022Nov/${doublequote})"

