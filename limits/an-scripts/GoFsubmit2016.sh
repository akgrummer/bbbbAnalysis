MAINDIR=/uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/limits
# COMBINEDIR=/localCombineRuns/CombineGoF_2023May9/
COMBINEDIR=/localCombineRuns/CombineGoF_2023May9_MX_1600_MY_700/

# TARGETS="MX_400_MY_125,MX_600_MY_400 MX_700_MY_60,MX_800_MY_600 MX_900_MY_600,MX_1000_MY_800 MX_1200_MY_300,MX_1400_MY_900 MX_1600_MY_125,MX_1600_MY_700"
# TARGETS="MX_400_MY_125,MX_600_MY_400 MX_700_MY_60,MX_800_MY_600 MX_1000_MY_800 MX_1200_MY_300,MX_1400_MY_900 MX_1600_MY_125,MX_1600_MY_700"

YEAR=2016
# for TARGET in "MX_400_MY_125 MX_600_MY_400" "MX_700_MY_60 MX_800_MY_600" "MX_1000_MY_800" "MX_1200_MY_300 MX_1400_MY_900" "MX_1600_MY_125 MX_1600_MY_700"; do
for TARGET in "MX_1600_MY_700"; do
   set -- $TARGET;
   if [ -z "$2" ]
   then
       ( cd ${MAINDIR}${COMBINEDIR}${1}; \
            combine -M GoodnessOfFit -n _${YEAR}_${1} ${YEAR}/datacard_${YEAR}_sig_NMSSM_bbbb_${1}.root --algo=saturated >> sat_${YEAR}_sig_NMSSM_bbbb_${1}.txt && \
            cd ${MAINDIR}${COMBINEDIR}${1}; \
            combine -M GoodnessOfFit -n _${YEAR}_${1}_TF ${YEAR}/datacard_${YEAR}_sig_NMSSM_bbbb_${1}.root --algo=saturated -t 1000 -s 12345 --toysFreq >> TFsat_${YEAR}_sig_NMSSM_bbbb_${1}_data.txt ) &

   else
       ( cd ${MAINDIR}${COMBINEDIR}${1}; \
            combine -M GoodnessOfFit -n _${YEAR}_${1} ${YEAR}/datacard_${YEAR}_sig_NMSSM_bbbb_${1}.root --algo=saturated >> sat_${YEAR}_sig_NMSSM_bbbb_${1}.txt && \
            cd ${MAINDIR}${COMBINEDIR}${1}; \
            combine -M GoodnessOfFit -n _${YEAR}_${1}_TF ${YEAR}/datacard_${YEAR}_sig_NMSSM_bbbb_${1}.root --algo=saturated -t 1000 -s 12345 --toysFreq >> TFsat_${YEAR}_sig_NMSSM_bbbb_${1}_data.txt && \
            cd ${MAINDIR}${COMBINEDIR}${2}; \
            combine -M GoodnessOfFit -n _${YEAR}_${2} ${YEAR}/datacard_${YEAR}_sig_NMSSM_bbbb_${2}.root --algo=saturated >> sat_${YEAR}_sig_NMSSM_bbbb_${2}.txt && \
            cd ${MAINDIR}${COMBINEDIR}${2}; \
            combine -M GoodnessOfFit -n _${YEAR}_${2}_TF ${YEAR}/datacard_${YEAR}_sig_NMSSM_bbbb_${2}.root --algo=saturated -t 1000 -s 12345 --toysFreq >> TFsat_${YEAR}_sig_NMSSM_bbbb_${2}_data.txt ) &
   fi
done
cd ${MAINDIR}
