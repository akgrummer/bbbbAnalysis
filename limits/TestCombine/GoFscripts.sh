YEAR=2017
ALGO=KS
TAG=BkgOnly
# combine -M GoodnessOfFit -n ${YEAR}${ALGO}SigStr0 localCombineRuns/CombineGoF_2022Oct20/${YEAR}/sig_NMSSM_bbbb_MX_300_MY_150/datacard${YEAR}_selectionbJets_SignalRegion.txt --algo=${ALGO} >> ${ALGO}_${YEAR}_sig_NMSSM_bbbb_MX_300_MY_150_VR.txt -t 100 -s 12345 --fixedSignalStrength=0
combine -M GoodnessOfFit -n ${YEAR}${ALGO}${TAG} ../localCombineRuns/CombineGoF_2022Oct20/${YEAR}/sig_NMSSM_bbbb_MX_300_MY_150/datacard${YEAR}_selectionbJets_SignalRegion.txt --algo=${ALGO} >> ${ALGO}_${YEAR}_${TAG}_sig_NMSSM_bbbb_MX_300_MY_150_VR.txt
# combine -M FitDiagnostics -n ${YEAR}${ALGO}SigStr0 localCombineRuns/CombineGoF_2022Oct20/${YEAR}/sig_NMSSM_bbbb_MX_300_MY_150/datacard${YEAR}_selectionbJets_SignalRegion.txt --algo=${ALGO} >> ${ALGO}_${YEAR}_sig_NMSSM_bbbb_MX_300_MY_150_VR.txt -t 100 -s 12345

