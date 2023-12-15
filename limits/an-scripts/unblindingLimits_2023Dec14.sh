#!/bin/bash

# TAG="2023Dec7_binMYx2_addMX650_10ev_rmSigs_VR"
# TAG="2023Dec7_binMYx2_addMX650_10ev_rmSigs_SR"
# TAG="2023Dec7_binMYx2_addMX650_10ev_unblind_VR"
# TAG="2023Dec7_binMYx2_addMX650_10ev_unblind_SR"

tags=( "2023Dec7_binMYx2_addMX650_10ev_unblind_VR" "2023Dec7_binMYx2_addMX650_10ev_unblind_SR" )
blindings=( "" "--unblind")
years=( "2016" "2017" "2018" "RunII" )
# unblind="--unblind"
# unblind=""
for ablinding in "${blindings[@]}"; do
    for atag in "${tags[@]}"; do
        for ayear in "${years[@]}"; do
            python an-scripts/PlotLimitVsMy_orig.py --tag ${atag} --systematics --year ${ayear} --vsMY ${ablinding}
        done
        ayear="RunII"; python an-scripts/PlotLimitVsMy_orig.py --tag ${atag} --systematics --year ${ayear} ${ablinding}
    done;
done
