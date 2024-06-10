#!/bin/bash

TAG="2023Dec7_binMYx2_addMX650_10ev_fullPlane_SR"
# SAMPLES="prepareModels/listOfSamples_genToys.txt" # needs to be one signal for genToys jobs
SAMPLES="prepareModels/listOfSamples.txt" # needs to be one signal
YEAR="RunII"

python prepareModels/SubmitFullRunIILimits_fullPlane.py --tag ${TAG} \
    --year ${YEAR} --samplelist ${SAMPLES} --unblind

