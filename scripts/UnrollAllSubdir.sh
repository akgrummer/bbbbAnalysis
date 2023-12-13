# TAG=2022Nov14_bJetScoreLoose_shapes2
# TAG=2023Feb28_3_trim
# TAG=2023Jul5 # everything is trimmed now - starting from the BDT, and the fill
# TAG=2023Jul5_loc # for saving the unrolled location of mX, mY and their 1d bin number
# TAG=2023Jul5_doubleMCStats # for saving the unrolled location of mX, mY and their 1d bin number
# TAG=2023Jul5_1p5MCStats # for saving the unrolled location of mX, mY and their 1d bin number
# TAG=2023Jul5_binMYx2_ncMCStats #
# TAG=2023Jul5_nonClosureMCStats #
# TAG=2023Jul5_nonClosureMCStats2 #
# TAG=2023Jul5_binMYx2_MXx2
# TAG=2023Jul5_binMYx2_ncMCStats_lowStatsCut
# TAG=2023Jul5_binMYx2_ncMCStats_lowStatsCut_5ev
# TAG=2023Jul5_binMYx2_ncMCStats_lowStatsCut_10ev
# TAG=2023Nov1_binMYx2_add2017Sig_10ev
TAG="2023Dec7_binMYx2_addMX650_10ev"
# TAG=2023Jul5_binMYx2_MXx2_loc
# TAG=2023Jul5_test
# TAG=2023Jul5_binX4 # bins are 4 x larger in mX and mY
submissionDir=fullSubmission_2022Nov
# TARGET=Unroll2DplotsSubRange_dev # the faster version _dev
# TARGET=Unroll2DplotsSubRange_dev_saveLocation # the faster version _dev
# TARGET=Unroll2DplotsSubRange_dev_doubleMCStats # misnamed now, actually applies hourglass unc in the stat unc. bkg uncertainty
TARGET=Unroll2DplotsSubRange_dev_hourglassMCStats_lowStatsCuts # saves bin locations, applies hourglass for MC stats, cut on stats
cd scripts && g++  -std=c++17 -I `root-config --incdir` -o ${TARGET} ${TARGET}.cc `root-config --libs` -O3 ; cd -
# cd scripts && g++  -std=c++17 -I `root-config --incdir` -o ${TARGET} ${TARGET}.cc `root-config  --cflags --glibs` -O3; cd -

###########################################
#old
###########################################
# ./scripts/Unroll2DplotsSubRange $folder/outPlotter.root data_BTagCSV_dataDriven_kinFit selectionbJets_SignalRegion HH_kinFit_m_H2_m 0 selectionbJets_ValidationRegionBlinded
# ./scripts/Unroll2DplotsSubRange VarPlots/rootHists/$1DataPlots_$2/outPlotter.root data_BTagCSV_dataDriven_kinFit selectionbJets_SignalRegion HH_kinFit_m_H2_m 0
# ./scripts/Unroll2DplotsSubRange VarPlots/rootHists/$1DataPlots_$2/outPlotter.root data_BTagCSV_dataDriven_kinFit selectionbJets_SignalRegion HH_kinFit_m_H2_m 0
# ./scripts/Unroll2DplotsSubRange VarPlots/rootHists/$1DataPlots_$2/outPlotter.root data_BTagCSV_dataDriven_kinFit selectionbJets_SignalRegion HH_kinFit_m_H2_m 0
# ./scripts/Unroll2DplotsSubRange VarPlots/rootHists/$1DataPlots_$2/outPlotter.root data_BTagCSV_dataDriven_kinFit selectionbJets_SignalRegion HH_kinFit_m_H2_m 0

# ./scripts/${TARGET} VarPlots/rootHists/${submissionDir}/2016DataPlots_${TAG}/outPlotter.root data_BTagCSV_dataDriven_kinFit selectionbJets_SignalRegion HH_kinFit_m_H2_m 0 selectionbJets_ValidationRegionBlinded
# ./scripts/${TARGET} VarPlots/rootHists/${submissionDir}/2017DataPlots_${TAG}/outPlotter.root data_BTagCSV_dataDriven_kinFit selectionbJets_SignalRegion HH_kinFit_m_H2_m 0 selectionbJets_ValidationRegionBlinded
# ./scripts/${TARGET} VarPlots/rootHists/${submissionDir}/2018DataPlots_${TAG}/outPlotter.root data_BTagCSV_dataDriven_kinFit selectionbJets_SignalRegion HH_kinFit_m_H2_m 0 selectionbJets_ValidationRegionBlinded

# ./scripts/${TARGET} VarPlots/rootHists/${submissionDir}/2016DataPlots_${TAG}/outPlotter.root data_BTagCSV_dataDriven_kinFit selectionbJets_SignalRegion HH_kinFit_m_H2_m 1 selectionbJets_ValidationRegionBlinded
###########################################

#UNROLLING:
for YEAR in 2016 2017 2018; do
    for group in 0 1 2 3 4; do
        ./scripts/${TARGET} VarPlots/rootHists/${submissionDir}/${YEAR}DataPlots_${TAG}/outPlotter.root data_BTagCSV_dataDriven_kinFit selectionbJets_SignalRegion HH_kinFit_m_H2_m ${group} selectionbJets_ValidationRegionBlinded &
    done;
    wait
    echo "finished ${YEAR}"
done

## Split in to regions:
for YEAR in 2016 2017 2018; do
    mkdir -p VarPlots/rootHists/${submissionDir}/${YEAR}DataPlots_${TAG}_VR
    mkdir -p VarPlots/rootHists/${submissionDir}/${YEAR}DataPlots_${TAG}_SR
    cp VarPlots/rootHists/${submissionDir}/${YEAR}DataPlots_${TAG}/outPlotter_massGroup* VarPlots/rootHists/${submissionDir}/${YEAR}DataPlots_${TAG}_VR/
    cp VarPlots/rootHists/${submissionDir}/${YEAR}DataPlots_${TAG}/outPlotter_massGroup* VarPlots/rootHists/${submissionDir}/${YEAR}DataPlots_${TAG}_SR/
done;


# This comes before creating the backgrond shapes
doublequote=\" singlequote=\'
# if running the command line - use single quotes to wrap the function and arguement, otherwise this method seems to work here
# FOR VALIDATION TEST
root -l -b -q "./scripts/modifyAllPlotForValidationTest.C(${doublequote}${TAG}_VR${doublequote}, ${doublequote}fullSubmission_2022Nov/${doublequote})"
# Now create the shape hists (up and down min and max...)
# #SHAPES
root -l -q "./scripts/calculateAllBKGshape.C(${doublequote}${TAG}_SR${doublequote}, ${doublequote}fullSubmission_2022Nov/${doublequote})"
root -l -q "./scripts/calculateAllBKGshape.C(${doublequote}${TAG}_VR${doublequote}, ${doublequote}fullSubmission_2022Nov/${doublequote})"


# # probably dont need this at all anymore:
# # HOURGLASS SHAPES (probably don't need to recompile everytime...
# cd hourglassUnc
# make add_hourglass_unc
# ./bin/add_hourglass_unc ${TAG}
# make add_hourglass_unc_VR_forLimits
# ./bin/add_hourglass_unc_VR_forLimits ${TAG}
# cd -
#
#
