#!/bin/bash

# tag="2023Dec7_binMYx2_addMX650_10ev_VR"
tag="2023Dec7_binMYx2_addMX650_10ev_SR"

# years=( 2017 )
years=( 2016 2017 2018 )
# groups=( 0 )
groups=( 1 )
for ayear in "${years[@]}"; do
    for agroup in "${groups[@]}"; do
        python scripts/plotting/FitDiag2Dpull_LocalSignfPoints.py --tag ${tag} --year ${ayear} --group ${agroup}
    done;
done

