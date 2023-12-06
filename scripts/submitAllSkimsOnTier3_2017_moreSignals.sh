#!/bin/bash

submitTag="moreSignalsSubmission_2017_test"
submitScript="scripts/submitSkimOnTier3.py"
inputFiles="MoreSignals/NMSSM_XYH_bbbb_MX_1000_MY_150_NANOAOD_v7_2017.txt"
configFile="config/Resonant_NMSSM_bbbb/skim_2017Resonant_NMSSM_XYH_bbbb.cfg"
weightFile="weights/2017_NMSSM_XYH_bbbb_weights_MoreSignals/NMSSM_XYH_bbbb_MX_1000_MY_150_NANOAOD_v7_2017_PUweights.root"
crossSection=0.01
numberOfJobs=2
deltaR=0.25

# --append=_MY_60
# --yMassSelection=60

python ${submitScript} \
    --input=${inputFiles}   \
    --tag=${submitTag} \
    --cfg=${configFile}  \
    --puWeight=${weightFile}  \
    --is-signal \
    --xs=${crossSection}   \
    --njobs=${numberOfJobs} \
    --maxDeltaR=${deltaR}


jecSystList=( Total )

# --append=_MY_60
# --yMassSelection=60

for jecsyst in "${jecSystList[@]}"; do
    for systdir in up down ; do
        python ${submitScript}  \
            --jes-shift-syst ${jecsyst}:${systdir} \
            --input=${inputFiles}  \
            --tag=${submitTag}_${jecsyst}_${systdir} \
            --cfg=${configFile}  \
            --puWeight=${weightFile}  \
            --is-signal \
            --xs=${crossSection}   \
            --njobs=${numberOfJobs} \
            --maxDeltaR=${deltaR}
    done
done

jerSystList=( jer bjer )

for jersyst in "${jerSystList[@]}"; do
    for systdir in up down ; do
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

