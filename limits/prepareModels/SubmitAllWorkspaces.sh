#!/bin/bash

# TAG="2023Feb28_trim_VR"
# TAG="2023Feb28_VR"
TAG="2023Feb28_hourglass_unc"
# TAG="2023Feb28_trim"
YEAR="RunII"

python prepareModels/SubmitWorkspaces.py --tag ${TAG} --year ${YEAR} --group auto
