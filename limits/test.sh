# TARGETS="MX_400_MY_125,MX_600_MY_400 MX_700_MY_60,MX_800_MY_600 MX_900_MY_600,MX_1000_MY_800 MX_1200_MY_300,MX_1400_MY_900 MX_1600_MY_125,MX_1600_MY_700"
# TARGETS="MX_400_MY_125 MX_600_MY_400" "MX_700_MY_60 MX_800_MY_600" "MX_1000_MY_800" "MX_1200_MY_300 MX_1400_MY_900" "MX_1600_MY_125 MX_1600_MY_700"
# OLDIFS=$IFS; for TARGET in ${TARGETS[@]}; do
MAINDIR=/uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/limits
for TARGET in "MX_400_MY_125 MX_600_MY_400" "MX_700_MY_60 MX_800_MY_600" "MX_1000_MY_800" "MX_1200_MY_300 MX_1400_MY_900" "MX_1600_MY_125 MX_1600_MY_700"; do
   set -- $TARGET;
   if [ -z "$2" ]
   then
        cd ${MAINDIR}/localCombineRuns/CombineGoF_2023May9/${1}; \
        echo $1; pwd;
   else
        cd ${MAINDIR}/localCombineRuns/CombineGoF_2023May9/${1}; \
        echo $1 and $2;pwd;
   fi
done
cd ${MAINDIR}
