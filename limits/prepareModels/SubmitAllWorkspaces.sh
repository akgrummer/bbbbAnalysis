#!/bin/bash

# TAG="2023Feb28_trim_VR"
# TAG="2023Feb28_VR"
# TAG="2023Feb28_hourglass_unc"
# TAG="2023Feb28_trim"
# TAG="2023Jul5_VR"
# TAG="2023Jul5_SR"
# TAG="2023Jul5_binX4_VR"
# TAG="2023Jul5_binX4_SR"
# TAG="2023Jul5_doubleMCStats_VR"
# TAG="2023Jul5_1p5MCStats_VR"
# TAG="2023Jul5_newMinimizer_VR" # this is a copy of 2023Jul5_VR until the next (GoF step)
# TAG="2023Jul5_newMinimizer_SR" # this is a copy of 2023Jul5_VR until the next (GoF step)
# TAG="2023Jul5_binMYx2_VR" #
# TAG="2023Jul5_binMYx2_SR" #
# TAG="2023Jul5_nonClosureMCStats_VR" #
# TAG="2023Jul5_nonClosureMCStats_SR" #
# TAG="2023Jul5_nonClosureMCStats2_VR" #
# TAG="2023Jul5_nonClosureMCStats2_SR" #
# TAG="2023Jul5_binMYx2_ncMCStats_VR" #
# TAG="2023Jul5_binMYx2_ncMCStats_SR" #
# TAG="2023Jul5_binMYx2_MXx2_VR"
# TAG="2023Jul5_binMYx2_MXx2_SR"
# TAG="2023Jul5_binMYx2_ncMCStats_lowStatsCut_5ev_SR"
TAG="2023Jul5_binMYx2_ncMCStats_lowStatsCut_10ev_SR"
YEAR="RunII"
# SAMPLES="prepareModels/listOfSamples_10points.txt"
SAMPLES="prepareModels/listOfSamples_3in1600.txt"


python prepareModels/SubmitWorkspaces.py --tag ${TAG} --year ${YEAR} --group auto --samplelist ${SAMPLES}

