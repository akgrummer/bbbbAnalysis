#!/bin/bash

# TAG="2023Dec7_binMYx2_addMX650_10ev_rmSigs_VR"
# TAG="2023Dec7_binMYx2_addMX650_10ev_rmSigs_SR"
# TAG="2023Dec7_binMYx2_addMX650_10ev_unblind_VR"
# TAG="2023Dec7_binMYx2_addMX650_10ev_unblind_SR"

tags=( "2023Dec7_binMYx2_addMX650_10ev_unblind_SR" )

# sig_tag="mx700_my400"
sig_tag="mx650_my350"
pseudoDatatags=( "2024Jan26_psuedoData_checkExcessLimits_${sig_tag}_unblind" )
blindings=( "--unblind")
# years=( "2016" "2017" "2018" "RunII" )
# unblind="--unblind"
# unblind=""
for ablinding in "${blindings[@]}"; do
    for atag in "${tags[@]}"; do
        for ayear in "${years[@]}"; do
            python an-scripts/PlotLimitVsMy_orig_pseudoDataOverlayed.py --tag ${atag} --systematics --year ${ayear} --vsMY ${ablinding} --pseudo ${pseudoDatatags}
        done
        ayear="RunII"; python an-scripts/PlotLimitVsMy_orig_pseudoDataOverlayed.py --tag ${atag} --systematics --year ${ayear} ${ablinding} --pseudo ${pseudoDatatags}
    done;
done
