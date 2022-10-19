# TAG="fullSubmission_v53"

# g++  -std=c++17 -I `root-config --incdir`  -o PlotLimitsFromCondor PlotLimitsFromCondor.cc `root-config --libs` -O3
# g++  -std=c++17 -I `root-config --incdir`  -o Plot2DLimitMap       Plot2DLimitMap.C        `root-config --libs` -O3

# # ./PlotLimitsFromCondor $TAG
# ./PlotLimitsFromCondor $TAG impacts

# python CompareHHAnalysisAll.py --input Limits_$TAG.root --systematics
# python CompareHHAnalysisAll.py --input Limits_$TAG.root
# ./Plot2DLimitMap Limits_$TAG.root

# python MeasureSystematicEffect.py --input Limits_$TAG.root --impacts

# python OverlapPlots.py  --input Limits_$TAG.root --systematics
# python OverlapTheory.py --input Limits_$TAG.root --systematics
# python PlotHHLimit.py --input Limits_$TAG.root --systematics
# python PlotLimitVsMy.py --input Limits_$TAG.root --systematics








# TAG="fullSubmission_v56"
# TAG="aidan_all_2021Dec23"
# TAG="CR_2022Jan26"
# TAG="CR_binwidthX2_2022Jan26"
# TAG="VR_2022Jan26"
# TAG="VR_binwidthX2_2022Jan26"

# g++  -std=c++17 -I `root-config --incdir`  -o PlotLimitsFromCondor_allyears PlotLimitsFromCondor_allyears.cc `root-config --libs` -O3
# mkdir LimitPlots_$TAG

# ./PlotLimitsFromCondor_allyears $TAG
# mv Limits_$TAG.root LimitPlots_$TAG

# TAG="CR_2022Jan26"
# python PlotLimitMean.py --input LimitPlots_$TAG/Limits_$TAG.root --year 2016 --systematics
# python PlotLimitMean.py --input LimitPlots_$TAG/Limits_$TAG.root --year 2017 --systematics
# python PlotLimitMean.py --input LimitPlots_$TAG/Limits_$TAG.root --year 2018 --systematics
# python PlotLimitMean.py --input LimitPlots_$TAG/Limits_$TAG.root --year RunII --systematics
TAG="VR_2022Jan26"
# python PlotLimitMean.py --input LimitPlots_$TAG/Limits_$TAG.root --year 2016 --systematics
# python PlotLimitMean.py --input LimitPlots_$TAG/Limits_$TAG.root --year 2017 --systematics
# python PlotLimitMean.py --input LimitPlots_$TAG/Limits_$TAG.root --year 2018 --systematics
# python PlotLimitMean.py --input LimitPlots_$TAG/Limits_$TAG.root --year RunII --systematics
# TAG="2022July11_fullBDT_bJetScoreLoose"
# TAG="2022July11_fullBDT_bJetScoreLoose_VR"
# TAG="2022July13_fullBDT_bJetScoreLoose_VR"
# TAG="2022July15_fullBDT_bJetScore1p5_VR"
# TAG="2022July15_fullBDT_bJetScore1p5_VR"
# TAG="2022Aug1_fullBDT_bJetLoose_CutLowMx_VR"
option=""
# option="_freezeBKGnorm"
# option="_statOnly"
python PlotLimitMean.py --input LimitPlots_$TAG${option}/Limits_$TAG.root --year 2016 --systematics
python PlotLimitMean.py --input LimitPlots_$TAG${option}/Limits_$TAG.root --year 2017 --systematics
python PlotLimitMean.py --input LimitPlots_$TAG${option}/Limits_$TAG.root --year 2018 --systematics
python PlotLimitMean.py --input LimitPlots_$TAG${option}/Limits_$TAG.root --year RunII --systematics

# python PlotLimitMean.py --input LimitPlots_$TAG${option}/Limits_$TAG.root --year 2016 --freezeBKGnorm
# python PlotLimitMean.py --input LimitPlots_$TAG${option}/Limits_$TAG.root --year 2017 --freezeBKGnorm
# python PlotLimitMean.py --input LimitPlots_$TAG${option}/Limits_$TAG.root --year 2018 --freezeBKGnorm
# python PlotLimitMean.py --input LimitPlots_$TAG${option}/Limits_$TAG.root --year RunII --freezeBKGnorm

# python PlotLimitMean.py --input LimitPlots_$TAG${option}/Limits_$TAG.root --year 2016
# python PlotLimitMean.py --input LimitPlots_$TAG${option}/Limits_$TAG.root --year 2017
# python PlotLimitMean.py --input LimitPlots_$TAG${option}/Limits_$TAG.root --year 2018
# python PlotLimitMean.py --input LimitPlots_$TAG${option}/Limits_$TAG.root --year RunII

