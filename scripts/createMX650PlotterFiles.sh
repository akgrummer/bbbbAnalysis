#!/bin/bash

createPlotterFile(){
    mYval=${1}
    year=${2}
    variant=${3}

    # ofile="MoreSignals/MX650/NMSSM_XToYHTo4B_MX-650_MY-${mYval}_${year}.txt"
    #plotterListFiles
    odir="plotterListFiles/MX650/${year}/Signal${variant}/"
    ofile="${odir}FileList_NMSSM_XToYHTo4B_MX-650_MY-${mYval}_${year}.txt"
    # echo ${ofile}
    mkdir -p ${odir}
    # touch ${ofile}
    > ${ofile}
    echo "root://cmseos.fnal.gov//store/user/agrummer/bbbb_ntuples/moreSignals_mX650_mY${mYval}_${year}${variant}/SKIM_NMSSM_XToYHTo4B_MX-650_MY-${mYval}_${year}/output/bbbbNtuple_0.root">>${ofile}
    echo "root://cmseos.fnal.gov//store/user/agrummer/bbbb_ntuples/moreSignals_mX650_mY${mYval}_${year}${variant}/SKIM_NMSSM_XToYHTo4B_MX-650_MY-${mYval}_${year}/output/bbbbNtuple_1.root">>${ofile}

}

years=( 2016 2017 2018 )
mYvals=( 60 70 80 90 100 125 150 190 250 300 350 400 450 500 )
variants=( "" "_Total_down" "_Total_up" "_bjer_down" "_bjer_up" "_jer_down" "_jer_up" )



createPlotterFile 60 2018 "_Total_down"
for ayear in "${years[@]}"; do
    for anMY in "${mYvals[@]}"; do
        for avariant in "${variants[@]}"; do
            createPlotterFile ${anMY} ${ayear} ${avariant}
        done;
    done;
done
