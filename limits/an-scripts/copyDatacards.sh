TARGETS=( MX_400_MY_125 MX_600_MY_400 MX_700_MY_60 MX_800_MY_600 MX_1000_MY_800 MX_1200_MY_300 MX_1400_MY_900 MX_1600_MY_125 MX_1600_MY_700 )
# TARGETS=( MX_900_MY_600 )
YEARS=( 2016 2017 2018 )
# YEARS=( 2017 2018 )
# YEAR=2016
for TARGET in ${TARGETS[@]}; do
    for YEAR in ${YEARS[@]}; do
        mkdir -p ${TARGET}/${YEAR}
        cd ${TARGET}/${YEAR}
        eos cp root://cmseos.fnal.gov//store/user/agrummer/bbbb_limits/2023Feb28_hourglass/HistogramFiles_${YEAR}/datacard_${YEAR}_sig_NMSSM_bbbb_${TARGET}.txt .
        eos cp root://cmseos.fnal.gov//store/user/agrummer/bbbb_limits/2023Feb28_hourglass/HistogramFiles_${YEAR}/outPlotter_${YEAR}_sig_NMSSM_bbbb_${TARGET}.root .
        text2workspace.py datacard_${YEAR}_sig_NMSSM_bbbb_${TARGET}.txt >> text2workspace_output.txt 
        cd -
    done
done

