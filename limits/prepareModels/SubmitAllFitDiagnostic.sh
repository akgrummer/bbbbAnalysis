#!/bin/bash

# TAG="2023Feb28_hourglass_VR_ws"
# TAG="2023Feb28_trim_VR"
# TAG="2023Feb28_VR"
# TAG="2023Feb28_hourglass_unc"
# TAG="2023Feb28_trim"
# TAG="2023Jul5_VR"
# TAG="2023Jul5_SR"
# TAG="2023Jul5_binX4_VR"
# TAG="2023Jul5_binX4_SR"
# TAG="2023Jul5_binMYx2_VR" #
# TAG="2023Jul5_binMYx2_SR" #
# TAG="2023Jul5_nonClosureMCStats2_VR" #
# TAG="2023Jul5_nonClosureMCStats2_SR" #
# TAG="2023Jul5_binMYx2_ncMCStats_VR" #
# TAG="2023Jul5_binMYx2_MXx2_VR"
# TAG="2023Jul5_binMYx2_MXx2_SR"
# TAG="2023Dec7_binMYx2_addMX650_10ev_VR"
TAG="2023Dec7_binMYx2_addMX650_10ev_SR"
# YEAR=2016
# NTOYS=100
# SAMPLES="prepareModels/listOfSamples.txt"
SAMPLES="prepareModels/listOfSamples_10points.txt"
ALGO="saturated"

# NTOYS=2
# SEED=12340
# TAGID=6
TAGID=0
# for YEAR in 2016; do
for YEAR in 2016 2017 2018; do
    python prepareModels/SubmitFitDiagnostics.py --tag ${TAG} --tagid ${TAGID} --year ${YEAR} --samplelist ${SAMPLES} --group auto --fixsig 0
done

