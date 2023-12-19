#!/bin/bash

tag="2023Dec7_binMYx2_addMX650_10ev_unblind_signif_all_SR"
years=( "2016" "2017" "2018" "RunII" )

odir="Significance/${tag}/"
mkdir -p ${odir}

for ayear in "${years[@]}"; do
    ofile="sig_${ayear}.root"
    mapfile -t vars < <( xrdfs root://cmseos.fnal.gov ls -u /store/user/agrummer/bbbb_limits/${tag}/HistogramFiles_${ayear} | egrep '*syst\.root' )
    hadd ${odir}${ofile} "${vars[@]}"
    var=()
done

# for avar in "${vars[@]}";do
#     echo ${avar}
# done
#
