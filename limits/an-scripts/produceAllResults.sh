# TAG="fullSubmission_v53"
# TAG="2022Nov22_bJetScoreLoose_shapes2"
# TAG="2023Feb28"
# TAG="2023Feb28_hourglass"
# TAG="2023Jul5_binMYx2_ncMCStats_lowStatsCut_10ev_SR"
# TAG="2023Jul5_binMYx2_ncMCStats_lowStatsCut_5ev_SR"
# TAG="2023Nov1_binMYx2_add2017Sig_10ev_SR"
# TAG="2023Dec7_binMYx2_addMX650_10ev_SR"
# TAG="2023Dec7_binMYx2_addMX650_10ev_rmSigs_VR"
# TAG="2023Dec7_binMYx2_addMX650_10ev_rmSigs_SR"
# TAG="2023Dec7_binMYx2_addMX650_10ev_unblind_VR"
TAG="2023Dec7_binMYx2_addMX650_10ev_unblind_SR"
# TAG="2023Jul5_nonClosureMCStats2_SR"
# some scripts in this file have been relocated - check an-scripts, or results
# possible that things were using Fabio's `scripts` directory with a sym link. Check fromFabio directory.

# compile the cpp codes (if needed)
# g++  -std=c++17 -I `root-config --incdir`  -o an-scripts/PlotLimitsFromCondor an-scripts/PlotLimitsFromCondor.cc `root-config --libs` -O3
# g++  -std=c++17 -I `root-config --incdir`  -o an-scripts/Plot2DLimitMap       an-scripts/Plot2DLimitMap.C        `root-config --libs` -O3
# # ##################################################
#LOOKS LIKE THIS WAS only used for the old vr closure tests
# g++  -std=c++17 -I `root-config --incdir`  -o PlotLimitsFromCondor_allyears PlotLimitsFromCondor_allyears.cc `root-config --libs` -O3
# mkdir LimitPlots_${TAG}${option}
# ./PlotLimitsFromCondor_allyears $TAG
# mv Limits_$TAG.root LimitPlots_${TAG}${option}
# # ##################################################

# makes the base plots in a root file (used just the impact version):
# ./PlotLimitsFromCondor $TAG
./an-scripts/PlotLimitsFromCondor $TAG impacts

##################################################
## no DiHiggs_v1 in Fabio's folder:
# needs: spin0/CombineResults_syst.txt
# python an-scripts/CompareHHAnalysisAll_fromRootFile.py --input hists/Limits_$TAG.root --systematics

# needs: spin0/CombineResults_statOnly.txt
# python an-scripts/CompareHHAnalysisAll_fromRootFile.py --input hists/Limits_$TAG.root

##################################################
# makes: CentralLimitMap_RunII_TheoryComparison.png
# can also run syst, statOnly and all years and runII
# ./an-scripts/Plot2DLimitMap ${TAG}

# makes: SistematicImpact_<YEAR>_*.png
# python an-scripts/MeasureSystematicEffect.py --input hists/Limits_$TAG.root --impacts
# makes just the systematic versinos, (no impacts)
# python MeasureSystematicEffect.py --input Limits_$TAG.root

# makes: LimitsRunII_Limits_syst_Overlap.png
# python an-scripts/OverlapPlots.py  --input hists/Limits_$TAG.root --systematics

# /uscms/home/fravera/nobackup/DiHiggs_v1/CMSSW_10_2_5/src/bbbbAnalysis/HXSG_NMSSM_recommendations_00.root
# needs: /uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/HXSG_NMSSM_recommendations_00.root
# makes: LimitsRunII_Limits_syst_Theory.png
# python an-scripts/OverlapTheory.py --input hists/Limits_$TAG.root --systematics

# makes: LimitsRunII_Limits_syst_HH.png
# python an-scripts/PlotHHLimit.py --input hists/Limits_$TAG.root --systematics

# makes: LimitsRunII_Limits_syst_mX_*.png, and prints central combine r values to a text file (text file is always appended to so need to remove old version as needed)
### a set of commands:######
# rm limitValues.txt
# unblind=""
#################
# unblind="--unblind"
# years=( "2016" "2017" "2018" "RunII" )
# for ayear in "${years[@]}"; do
#     python an-scripts/PlotLimitVsMy_orig.py --tag ${TAG} --systematics --year ${ayear} --vsMY ${unblind}
# done
# ayear="RunII"; python an-scripts/PlotLimitVsMy_orig.py --tag ${TAG} --systematics --year ${ayear} ${unblind}
#################
# to compare two limit runs:
# python an-scripts/PlotLimitVsMy_orig_twoLimits.py --input1 hists/Limits_2023Feb28.root --input2 hists/Limits_2023Feb28_hourglass.root --systematics
# python an-scripts/PlotLimitVsMy_orig_twoLimits.py --input1 hists/Limits_2023Feb28_hourglass.root --input2 hists/Limits_2023Jul5_binMYx2_ncMCStats_lowStatsCut_10ev_SR.root --systematics
# python an-scripts/PlotLimitVsMy_orig_twoLimits.py --input1 hists/Limits_2023Jul5_binMYx2_ncMCStats_lowStatsCut_10ev_SR.root --input2 hists/Limits_2023Nov1_binMYx2_add2017Sig_10ev_SR.root --systematics
# python an-scripts/PlotLimitVsMy_orig_twoLimits.py --vsMY --input1 hists/Limits_2023Jul5_binMYx2_ncMCStats_lowStatsCut_10ev_SR.root --input2 hists/Limits_2023Nov1_binMYx2_add2017Sig_10ev_SR.root --systematics
# python an-scripts/PlotLimitVsMy_orig_twoLimits.py --vsMY --year 2017 --input1 hists/Limits_2023Jul5_binMYx2_ncMCStats_lowStatsCut_10ev_SR.root --input2 hists/Limits_2023Nov1_binMYx2_add2017Sig_10ev_SR.root --systematics
# python an-scripts/PlotLimitVsMy_orig_threeLimits.py --input1 hists/Limits_2023Jul5_nonClosureMCStats2_SR.root --input2 hists/Limits_2023Jul5_binMYx2_ncMCStats_lowStatsCut_5ev_SR.root --input3 hists/Limits_2023Jul5_binMYx2_ncMCStats_lowStatsCut_10ev_SR.root --systematics
# the individual years didn't run
# python an-scripts/PlotLimitVsMy_orig.py --input hists/Limits_$TAG.root --systematics --year 2016
# python an-scripts/PlotLimitVsMy_orig.py --input hists/Limits_$TAG.root --systematics --year 2017
# python an-scripts/PlotLimitVsMy_orig.py --input hists/Limits_$TAG.root --systematics --year 2018
############################


##############################
##############################
##############################

# used PlotLimitsFromCondor_allyears compilation step here


# TAG="fullSubmission_v56"
# TAG="aidan_all_2021Dec23"
# TAG="CR_2022Jan26"
# TAG="CR_binwidthX2_2022Jan26"
# TAG="VR_2022Jan26"
# TAG="VR_binwidthX2_2022Jan26"
# TAG="2022July11_fullBDT_bJetScoreLoose"
# TAG="2022July11_fullBDT_bJetScoreLoose_VR"
# TAG="2022July13_fullBDT_bJetScoreLoose"
# TAG="2022July13_fullBDT_bJetScoreLoose_VR"
# TAG="2022July15_fullBDT_bJetScore1p5"
# TAG="2022July15_fullBDT_bJetScore1p5_VR"
# # TAG="2022Aug1_fullBDT_bJetLoose_CutLowMx"
# TAG="2022Aug1_fullBDT_bJetLoose_CutLowMx_VR"
option=""
# # option="_statOnly"
# # option="_freezeBKGnorm"


# python PlotLimitVsMy.py --input LimitPlots_$TAG${option}/Limits_$TAG.root --year 2016 --systematics
# python PlotLimitVsMy.py --input LimitPlots_$TAG${option}/Limits_$TAG.root --year 2017 --systematics
# python PlotLimitVsMy.py --input LimitPlots_$TAG${option}/Limits_$TAG.root --year 2018 --systematics
# python PlotLimitVsMy.py --input LimitPlots_$TAG${option}/Limits_$TAG.root --year RunII --systematics

# python PlotLimitVsMy.py --input LimitPlots_$TAG${option}/Limits_$TAG.root --year 2016
# python PlotLimitVsMy.py --input LimitPlots_$TAG${option}/Limits_$TAG.root --year 2017
# python PlotLimitVsMy.py --input LimitPlots_$TAG${option}/Limits_$TAG.root --year 2018
# python PlotLimitVsMy.py --input LimitPlots_$TAG${option}/Limits_$TAG.root --year RunII

# python PlotLimitVsMy.py --input LimitPlots_${TAG}_freezeBKGnorm/Limits_$TAG.root --year 2016 --freezeBKGnorm
# python PlotLimitVsMy.py --input LimitPlots_${TAG}_freezeBKGnorm/Limits_$TAG.root --year 2017 --freezeBKGnorm
# python PlotLimitVsMy.py --input LimitPlots_${TAG}_freezeBKGnorm/Limits_$TAG.root --year 2018 --freezeBKGnorm
# python PlotLimitVsMy.py --input LimitPlots_${TAG}_freezeBKGnorm/Limits_$TAG.root --year RunII --freezeBKGnorm

# TAG="CR_2022Jan26"
# python PlotLimitVsMy.py --input LimitPlots_$TAG/Limits_$TAG.root --year 2016 --systematics
# python PlotLimitVsMy.py --input LimitPlots_$TAG/Limits_$TAG.root --year 2017 --systematics
# python PlotLimitVsMy.py --input LimitPlots_$TAG/Limits_$TAG.root --year 2018 --systematics
# python PlotLimitVsMy.py --input LimitPlots_$TAG/Limits_$TAG.root --year RunII --systematics
# # TAG="CR_binwidthX2_2022Jan26"
# # python PlotLimitVsMy.py --input LimitPlots_$TAG/Limits_$TAG.root --year 2016 --systematics
# # python PlotLimitVsMy.py --input LimitPlots_$TAG/Limits_$TAG.root --year 2017 --systematics
# # python PlotLimitVsMy.py --input LimitPlots_$TAG/Limits_$TAG.root --year 2018 --systematics
# # python PlotLimitVsMy.py --input LimitPlots_$TAG/Limits_$TAG.root --year RunII --systematics
# TAG="VR_2022Jan26"
# python PlotLimitVsMy.py --input LimitPlots_$TAG/Limits_$TAG.root --year 2016 --systematics
# python PlotLimitVsMy.py --input LimitPlots_$TAG/Limits_$TAG.root --year 2017 --systematics
# python PlotLimitVsMy.py --input LimitPlots_$TAG/Limits_$TAG.root --year 2018 --systematics
# python PlotLimitVsMy.py --input LimitPlots_$TAG/Limits_$TAG.root --year RunII --systematics
# # TAG="VR_binwidthX2_2022Jan26"
# # python PlotLimitVsMy.py --input LimitPlots_$TAG/Limits_$TAG.root --year 2016 --systematics
# # python PlotLimitVsMy.py --input LimitPlots_$TAG/Limits_$TAG.root --year 2017 --systematics
# # python PlotLimitVsMy.py --input LimitPlots_$TAG/Limits_$TAG.root --year 2018 --systematics
# # python PlotLimitVsMy.py --input LimitPlots_$TAG/Limits_$TAG.root --year RunII --systematics
