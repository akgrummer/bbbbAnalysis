#!/bin/bash

# for 2017 mX=1000, mY=150
# ./bin/get_sample_PU_weights.exe --realPU weights/Collision17PileupHistogram.root --realPU_up weights/Collision17PileupHistogramUp.root --realPU_down weights/Collision17PileupHistogramDown.root --input MoreSignals/NMSSM_XYH_bbbb_MX_1000_MY_150_NANOAOD_v7_2017.txt --outputFolder=weights/2017_NMSSM_XYH_bbbb_weights_MoreSignals

# for all years mX=650
savePUfiles(){
    # should probabaly be local variables:
    htRange=${1}
    year=${2}
    if [ ${year} == "2016preVFP" ]; then
        pileupInput="--realPU weights/Collision16PileupHistogram.root --realPU_up weights/Collision16PileupHistogramUp.root --realPU_down weights/Collision16PileupHistogramDown.root"
    fi
    if [ ${year} == "2016" ]; then
        pileupInput="--realPU weights/Collision16PileupHistogram.root --realPU_up weights/Collision16PileupHistogramUp.root --realPU_down weights/Collision16PileupHistogramDown.root"
    fi
    if [ ${year} == "2017" ]; then
        pileupInput="--realPU weights/Collision17PileupHistogram.root --realPU_up weights/Collision17PileupHistogramUp.root --realPU_down weights/Collision17PileupHistogramDown.root"
    fi
    if [ ${year} == "2018" ]; then
        pileupInput="--realPU weights/Collision18PileupHistogram.root --realPU_up weights/Collision18PileupHistogramUp.root --realPU_down weights/Collision18PileupHistogramDown.root"
    fi
    ./bin/get_sample_PU_weights.exe ${pileupInput} --input "inputFiles/Zjets/${year}/ZJetsToQQ_HT-${htRange}_TuneCP5_13TeV-madgraphMLM-pythia8.txt" --outputFolder="weights/Zjets/${year}"
}

# Original run
# ayear=2018
# anHTrange="200to400"

# for ayear in "2016preVFP" "2016" "2017" "2018"; do
#     for anHTrange in "200to400" "400to600" "600to800" "800toInf" ; do
#         savePUfiles ${anHTrange} ${ayear}
#         ofile="weights/Zjets/${ayear}/ZJetsToQQ_HT-${htRange}_TuneCP5_13TeV-madgraphMLM-pythia8_PUweights.root"
#         ls -lthr ${ofile}
#     done;
# done

# 5 errors of file not found (4 unique sets
# reran them until no errors (see commands below)
#
# Error UL18 800toInf
# Error UL18 600to800
# Error UL17 200to400
# Error UL17 200to400
# Error UL16 800toInf

# ayear="2016"
# anHTrange="800toInf"
# savePUfiles ${anHTrange} ${ayear}
# ofile="weights/Zjets/${ayear}/ZJetsToQQ_HT-${htRange}_TuneCP5_13TeV-madgraphMLM-pythia8_PUweights.root"
# ls -lthr ${ofile}

ayear="2017"
anHTrange="200to400"
savePUfiles ${anHTrange} ${ayear}
ofile="weights/Zjets/${ayear}/ZJetsToQQ_HT-${htRange}_TuneCP5_13TeV-madgraphMLM-pythia8_PUweights.root"
ls -lthr ${ofile}

# ayear="2018"
# for anHTrange in "600to800" "800toInf" ; do
#     savePUfiles ${anHTrange} ${ayear}
#     ofile="weights/Zjets/${ayear}/ZJetsToQQ_HT-${htRange}_TuneCP5_13TeV-madgraphMLM-pythia8_PUweights.root"
#     ls -lthr ${ofile}
# done
