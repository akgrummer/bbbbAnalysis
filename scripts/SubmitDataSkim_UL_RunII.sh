### Run with: `source ./SubmitDataSkim_UL_RunII.sh <tag>
### Run with: `source ./scripts/SubmitDataSkim_UL_RunII.sh Nominal2016_data_2022Feb17 Nominal2017_data_2022Feb17 Nominal2018_data_2022Feb17 UL2016_preVFP_data_2022Feb17 UL2016_postVFP_data_2022Feb17 UL2017_data_2022Feb17 UL2018_data_2022Feb17`
### replace the tag
# # data sample Run2016
# python scripts/submitSkimOnTier3.py --input=inputFiles/2016_NMSSM_XYH_bbbb_Datasets/BTagCSV_Data.txt --tag=$1  --cfg=config/Resonant_NMSSM_bbbb/skim_2016Resonant_NMSSM_XYH_bbbb.cfg --is-data --njobs=200 --maxDeltaR=0.25
# # # data sample Run2017
# python scripts/submitSkimOnTier3.py --input=inputFiles/2017_NMSSM_XYH_bbbb_Datasets/BTagCSV_Data.txt --tag=$2  --cfg=config/Resonant_NMSSM_bbbb/skim_2017Resonant_NMSSM_XYH_bbbb.cfg --is-data --njobs=200 --maxDeltaR=0.25
# # # data sample Run2018
# python scripts/submitSkimOnTier3.py --input=inputFiles/2018_NMSSM_XYH_bbbb_Datasets/JetHT_Data.txt --tag=$3  --cfg=config/Resonant_NMSSM_bbbb/skim_2018Resonant_NMSSM_XYH_bbbb.cfg --is-data --njobs=200 --maxDeltaR=0.25
# # data sample Run2016 UL pre VFP
# python scripts/submitSkimOnTier3.py --input=inputFiles/UL/UL2016_files_preVFP.txt --tag=$4  --cfg=config/Resonant_NMSSM_bbbb/skim_2016Resonant_NMSSM_XYH_bbbb_UL_preVFP.cfg --is-data --njobs=200 --maxDeltaR=0.25
# data sample Run2016 UL post VFP
python scripts/submitSkimOnTier3.py --input=inputFiles/UL/UL2016_files_postVFP.txt --tag=$1  --cfg=config/Resonant_NMSSM_bbbb/skim_2016Resonant_NMSSM_XYH_bbbb_UL_postVFP.cfg --is-data --njobs=200 --maxDeltaR=0.25
# # data sample Run2017 UL
# python scripts/submitSkimOnTier3.py --input=inputFiles/UL/UL2017_files.txt --tag=$6  --cfg=config/Resonant_NMSSM_bbbb/skim_2017Resonant_NMSSM_XYH_bbbb_UL.cfg --is-data --njobs=200 --maxDeltaR=0.25
# # data sample Run2018 UL
# python scripts/submitSkimOnTier3.py --input=inputFiles/UL/UL2018_files.txt --tag=$7  --cfg=config/Resonant_NMSSM_bbbb/skim_2018Resonant_NMSSM_XYH_bbbb_UL.cfg --is-data --njobs=200 --maxDeltaR=0.25
