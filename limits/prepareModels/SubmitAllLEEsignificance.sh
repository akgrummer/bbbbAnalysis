#!/bin/bash

TAG="2023Dec7_binMYx2_addMX650_10ev_fullPlane_SR"
SAMPLES="prepareModels/listOfSamples.txt" # needs to be one signal


# NTOYS=200
# NTOYS=1000
NTOYS=250
SEED=12340
# TAGIDS=(1 2 3 4 5)
# TAGIDS=9 # seq includes the last number
TAGIDS=39 # seq includes the last number
# for YEAR in 2016 2017 2018; do
# for YEAR in 2016 2017 2018; do
for YEAR in "RunII"; do
    # for TAGID in ${TAGIDS[@]}; do
    for TAGID in $(seq 0 ${TAGIDS}); do
        # echo ${TAGID}
       # echo $((${TAGID}+${SEED}))
        python prepareModels/SubmitLEEsignificance.py --tag ${TAG} \
            --tagid ${TAGID} --ntoys ${NTOYS} \
            --year ${YEAR} --samplelist ${SAMPLES}
    done;
done

