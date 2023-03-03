# TAG="fullSubmission_v53"
# TAG="2022Nov22_bJetScoreLoose_shapes2"
TAG="2023Feb28"
# some scripts in this file have been relocated - check an-scripts, or results
# possible that things were using Fabio's `scripts` directory with a sym link. Check fromFabio directory.

# compile the cpp codes (if needed)
# g++  -std=c++17 -I `root-config --incdir`  -o PlotLimitsFromCondor PlotLimitsFromCondor.cc `root-config --libs` -O3
# g++  -std=c++17 -I `root-config --incdir`  -o Plot2DLimitMap       Plot2DLimitMap.C        `root-config --libs` -O3
# # ##################################################
#LOOKS LIKE THIS WAS only used for the old vr closure tests
# g++  -std=c++17 -I `root-config --incdir`  -o PlotLimitsFromCondor_allyears PlotLimitsFromCondor_allyears.cc `root-config --libs` -O3
# mkdir LimitPlots_${TAG}${option}
# ./PlotLimitsFromCondor_allyears $TAG
# mv Limits_$TAG.root LimitPlots_${TAG}${option}
# # ##################################################

# makes the base plots in a root file (used just the impact version):
# ./PlotLimitsFromCondor $TAG
# ./an-scripts/PlotLimitsFromCondor $TAG impacts

##################################################
## no DiHiggs_v1 in Fabio's folder:
# needs: spin0/CombineResults_syst.txt
# python CompareHHAnalysisAll_fromRootFile.py --input Limits_$TAG.root --systematics

# needs: spin0/CombineResults_statOnly.txt
# python CompareHHAnalysisAll_fromRootFile.py --input Limits_$TAG.root

##################################################
# makes: CentralLimitMap_RunII_TheoryComparison.png
# can also run syst, statOnly and all years and runII
# ./Plot2DLimitMap Limits_$TAG.root

# makes: SistematicImpact_<YEAR>_*.png
# python MeasureSystematicEffect.py --input Limits_$TAG.root --impacts
# makes just the systematic versinos, (no impacts)
# python MeasureSystematicEffect.py --input Limits_$TAG.root

# makes: LimitsRunII_Limits_syst_Overlap.png
# python OverlapPlots.py  --input Limits_$TAG.root --systematics

# /uscms/home/fravera/nobackup/DiHiggs_v1/CMSSW_10_2_5/src/bbbbAnalysis/HXSG_NMSSM_recommendations_00.root
# needs: /uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/HXSG_NMSSM_recommendations_00.root
# makes: LimitsRunII_Limits_syst_Theory.png
# python OverlapTheory.py --input Limits_$TAG.root --systematics

# makes: LimitsRunII_Limits_syst_HH.png
# python PlotHHLimit.py --input Limits_$TAG.root --systematics

# makes: LimitsRunII_Limits_syst_mX_*.png, and prints central combine r values to a text file (text file is always appended to so need to remove old version as needed)
### a set of commands:######
# rm limitValues.txt
python an-scripts/PlotLimitVsMy_orig.py --input data/Limits_$TAG.root --systematics
# python PlotLimitVsMy_orig.py --input Limits_$TAG.root --systematics --year 2016
# python PlotLimitVsMy_orig.py --input Limits_$TAG.root --systematics --year 2017
# python PlotLimitVsMy_orig.py --input Limits_$TAG.root --systematics --year 2018
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
