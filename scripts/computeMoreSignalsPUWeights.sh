#!/bin/bash

# for 2017 mX=1000, mY=150
# ./bin/get_sample_PU_weights.exe --realPU weights/Collision17PileupHistogram.root --realPU_up weights/Collision17PileupHistogramUp.root --realPU_down weights/Collision17PileupHistogramDown.root --input MoreSignals/NMSSM_XYH_bbbb_MX_1000_MY_150_NANOAOD_v7_2017.txt --outputFolder=weights/2017_NMSSM_XYH_bbbb_weights_MoreSignals

# for all years mX=650
savePUfiles(){
    mYval=${1}
    year=${2}
    if [ ${year} -eq 2016 ]; then
        pileupInput="--realPU weights/Collision16PileupHistogram.root --realPU_up weights/Collision16PileupHistogramUp.root --realPU_down weights/Collision16PileupHistogramDown.root"
    fi
    if [ ${year} -eq 2017 ]; then
        pileupInput="--realPU weights/Collision17PileupHistogram.root --realPU_up weights/Collision17PileupHistogramUp.root --realPU_down weights/Collision17PileupHistogramDown.root"
    fi
    if [ ${year} -eq 2018 ]; then
        pileupInput="--realPU weights/Collision18PileupHistogram.root --realPU_up weights/Collision18PileupHistogramUp.root --realPU_down weights/Collision18PileupHistogramDown.root"
    fi
    ./bin/get_sample_PU_weights.exe ${pileupInput} --input "MoreSignals/MX650/NMSSM_XToYHTo4B_MX-650_MY-${mYval}_${year}.txt" --outputFolder="weights/MX650_MoreSignals/${year}"
}

# ayear=2018
# anMY=450
# for ayear in 2016 2017 2018; do
    # for anMY in 60 70 80 90 100 125 150 190 250 300 350 400 450 500; do
        # savePUfiles ${anMY} ${ayear}
        # ofile="weights/MX650_MoreSignals/${year}/NMSSM_XToYHTo4B_MX-650_MY-${mYval}_${year}_PUweights.root"
        # ls -lthr ${ofile}
    # done;
# done

# 9 ERRORs of: [3000] Unable to open - cannot determine the prefix path
# in 6 datasets
#  all output listed in computePUerrors.md
#  repeated the PU computation for these files until no errors reported

# ayear=2016
# anMY=350
# savePUfiles ${anMY} ${ayear}
# ofile="weights/MX650_MoreSignals/${year}/NMSSM_XToYHTo4B_MX-650_MY-${mYval}_${year}_PUweights.root"
# ls -lthr ${ofile}

# ayear=2017
# anMY=100
# savePUfiles ${anMY} ${ayear}
# ofile="weights/MX650_MoreSignals/${year}/NMSSM_XToYHTo4B_MX-650_MY-${mYval}_${year}_PUweights.root"
# ls -lthr ${ofile}

ayear=2018
# anMY=450
for anMY in 60 125 150; do
    savePUfiles ${anMY} ${ayear}
    ofile="weights/MX650_MoreSignals/${year}/NMSSM_XToYHTo4B_MX-650_MY-${mYval}_${year}_PUweights.root"
    ls -lthr ${ofile}
done

