#!/bin/bash

# TAG="2023Feb28_hourglass_VR_ws"
# TAG="2023Feb28_trim_VR"
# TAG="2023Feb28_VR"
# TAG="2023Feb28_hourglass_unc"
# TAG="2023Feb28_trim"
# TAG="2023Jul5_VR"
# TAG="2023Jul5_SR"
# TAG="2023Jul5_doubleMCStats_VR"
# TAG="2023Jul5_1p5MCStats_VR"
# TAG="2023Jul5_newMinimizer_VR"
# TAG="2023Jul5_newMinimizer_SR"
# TAG="2023Jul5_binMYx2_VR" #
# TAG="2023Jul5_binMYx2_SR" #
# TAG="2023Jul5_nonClosureMCStats2_VR" #
# TAG="2023Jul5_nonClosureMCStats2_SR" #
# TAG="2023Jul5_binMYx2_ncMCStats_VR" #
# TAG="2023Jul5_binMYx2_ncMCStats_SR" #
# TAG="2023Jul5_binX4_VR"
# TAG="2023Jul5_binX4_SR"
# TAG="2023Jul5_binMYx2_MXx2_VR"
# TAG="2023Jul5_binMYx2_MXx2_SR"
# TAG="2023Jul5_binMYx2_ncMCStats_lowStatsCut_5ev_SR"
# TAG="2023Jul5_binMYx2_ncMCStats_lowStatsCut_10ev_SR"
TAG="2023Dec7_binMYx2_addMX650_10ev_VR"
# TAG="2023Dec7_binMYx2_addMX650_10ev_SR"
# YEAR=2016
# NTOYS=100
# SAMPLES="prepareModels/listOfSamples.txt"
SAMPLES="prepareModels/listOfSamples_10points.txt"
ALGO="saturated"

# NTOYS=2
# SEED=12340
# TAGID=6
# python prepareModels/SubmitGoF.py --tag ${TAG} --tagid ${TAGID} --algo ${ALGO} --ntoys ${NTOYS} --seed $((${TAGID}+${SEED})) --year ${YEAR} --samplelist ${SAMPLES} --group auto
NTOYS=0
TAGID=0
SEED=0
# for YEAR in 2016; do
for YEAR in 2016 2017 2018; do
    python prepareModels/SubmitGoF.py --tag ${TAG} --tagid ${TAGID} --algo ${ALGO} --ntoys ${NTOYS} --seed ${SEED} --year ${YEAR} --samplelist ${SAMPLES} --group auto --fixsig 0
done

NTOYS=200
# NTOYS=2
SEED=12340
TAGIDS=(1 2 3 4 5)
# TAGIDS=(1)
for YEAR in 2016 2017 2018; do
# for YEAR in 2016; do
    for TAGID in ${TAGIDS[@]}; do
       # echo $((${TAGID}+${SEED}))
        python prepareModels/SubmitGoF.py --tag ${TAG} --tagid ${TAGID} --algo ${ALGO} --ntoys ${NTOYS} --seed $((${TAGID}+${SEED})) --year ${YEAR} --samplelist ${SAMPLES} --group auto --fixsig 0
    done;
done

