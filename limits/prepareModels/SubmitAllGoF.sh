#!/bin/bash

# TAG="2023Feb28_hourglass_VR_ws"
# TAG="2023Feb28_trim_VR"
# TAG="2023Feb28_VR"
# TAG="2023Feb28_hourglass_unc"
TAG="2023Feb28_trim"
# YEAR=2016
# NTOYS=100
SAMPLES="prepareModels/listOfSamples.txt"
ALGO="saturated"

# NTOYS=2
# SEED=12340
# TAGID=6
# python prepareModels/SubmitGoF.py --tag ${TAG} --tagid ${TAGID} --algo ${ALGO} --ntoys ${NTOYS} --seed $((${TAGID}+${SEED})) --year ${YEAR} --samplelist ${SAMPLES} --group auto
NTOYS=0
TAGID=0
SEED=0
for YEAR in 2016 2017 2018; do
    python prepareModels/SubmitGoF.py --tag ${TAG} --tagid ${TAGID} --algo ${ALGO} --ntoys ${NTOYS} --seed ${SEED} --year ${YEAR} --samplelist ${SAMPLES} --group auto
done

NTOYS=200
SEED=12340
TAGIDS=(1 2 3 4 5)
# TAGIDS=(1)
for YEAR in 2016 2017 2018; do
    for TAGID in ${TAGIDS[@]}; do
        # echo $((${TAGID}+${SEED}))
        python prepareModels/SubmitGoF.py --tag ${TAG} --tagid ${TAGID} --algo ${ALGO} --ntoys ${NTOYS} --seed $((${TAGID}+${SEED})) --year ${YEAR} --samplelist ${SAMPLES} --group auto
    done;
done
