#!/bin/bash

# tag=2023Jul5_binMYx2_ncMCStats_lowStatsCut_5ev
# tag=2023Jul5_binMYx2_ncMCStats_lowStatsCut_10ev
tag="2023Dec7_binMYx2_addMX650_10ev_VR"
# tag=2023Jul5_binMYx2_ncMCStats
for year in 2016 2017 2018; do
    for group in 0 1 2 3 4; do
        python scripts/plotting/RerollEvents.py --tag ${tag} --year ${year} --group ${group}
done;
done
