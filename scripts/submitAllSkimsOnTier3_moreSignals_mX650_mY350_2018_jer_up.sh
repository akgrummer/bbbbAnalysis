#!/bin/bash

submitSkimsForMassPoint(){
    mYval=${1}
    year=${2}

    submitScript="scripts/submitSkimOnTier3.py"
    # submitTag="moreSignalsSubmission_2017"
    submitTag="moreSignals_mX650_mY${mYval}_${year}_njobs6"
    fileName="NMSSM_XToYHTo4B_MX-650_MY-${mYval}_${year}"
    inputFiles="MoreSignals/MX650/${fileName}.txt"
    configFile="config/Resonant_NMSSM_bbbb/skim_${year}Resonant_NMSSM_XYH_bbbb.cfg"
    weightFile="weights/MX650_MoreSignals/${year}/${fileName}_PUweights.root"
    numberOfJobs=6
    crossSection=0.01
    deltaR=0.25

    # --append=_MY_60
    # --yMassSelection=60

    # python ${submitScript} \
    #     --input=${inputFiles}   \
    #     --tag=${submitTag} \
    #     --cfg=${configFile}  \
    #     --puWeight=${weightFile}  \
    #     --is-signal \
    #     --xs=${crossSection}   \
    #     --njobs=${numberOfJobs} \
    #     --maxDeltaR=${deltaR}


    # jecSystList=( Total )

    # # --append=_MY_60
    # # --yMassSelection=60

    # for jecsyst in "${jecSystList[@]}"; do
    #     # for systdir in up down ; do
    #     for systdir in down ; do
    #         python ${submitScript}  \
    #             --jes-shift-syst ${jecsyst}:${systdir} \
    #             --input=${inputFiles}  \
    #             --tag=${submitTag}_${jecsyst}_${systdir} \
    #             --cfg=${configFile}  \
    #             --puWeight=${weightFile}  \
    #             --is-signal \
    #             --xs=${crossSection}   \
    #             --njobs=${numberOfJobs} \
    #             --maxDeltaR=${deltaR}
    #     done
    # done

    jerSystList=( jer )

    for jersyst in "${jerSystList[@]}"; do
        for systdir in up ; do
            python ${submitScript}  \
                --jer-shift-syst ${jersyst}:${systdir} \
                --input=${inputFiles}  \
                --tag=${submitTag}_${jersyst}_${systdir} \
                --cfg=${configFile}  \
                --puWeight=${weightFile}  \
                --is-signal \
                --xs=${crossSection}   \
                --njobs=${numberOfJobs} \
                --maxDeltaR=${deltaR}
        done
    done

}


# ayear=2016
# anMY=60
# submitSkimsForMassPoint ${anMY} ${ayear}

# for ayear in 2016 2017 2018; do
#     for anMY in 60 70 80 90 100 125 150 190 250 300 350 400 450 500; do
#         submitSkimsForMassPoint ${anMY} ${ayear}
#     done;
# done

ayear=2018
anMY=350
submitSkimsForMassPoint ${anMY} ${ayear}

