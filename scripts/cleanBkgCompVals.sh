#!/bin/bash

# ifile="bkgCompValues/2024Jun11_vars.txt"
# ifile="bkgCompValues/2024Jun11_vars_3b.txt"
# ifile="bkgCompValues/2024Jun11_vars_mY90pm10.txt"
# ifile="bkgCompValues/2024Jun11_vars_mY90pm1.txt"
# ifile="bkgCompValues/2024Jun11_vars_mY90pm10_3b.txt"
# ifile="bkgCompValues/2024Jun11_vars_mY90pm1_3b.txt"

valDir="bkgCompValues/Zjets204Jun30"
# ifiles=( "2024Jun21_vars_mY90_mX488.txt" )
ifiles=( "${valDir}/2024Jun11_vars.txt" )
ifiles+=( "${valDir}/2024Jun11_vars_3b.txt" )
ifiles+=( "${valDir}/2024Jun11_vars_mY90pm10.txt" )
ifiles+=( "${valDir}/2024Jun11_vars_mY90pm10_3b.txt" )
ifiles+=( "${valDir}/2024Jun21_vars_mY90_mX340.txt" )
ifiles+=( "${valDir}/2024Jun21_vars_mY90_mX488.txt" )
ifiles+=( "${valDir}/2024Jun21_vars_mY90_mX648.txt" )
ifiles+=( "${valDir}/2024Jun21_vars_mY90_mX960.txt" )
ifiles+=( "${valDir}/2024Jun21_vars_mY90_mX340to1216.txt" )
ifiles+=( "${valDir}/2024Jun21_vars_mY90_mX340_3b.txt" )
ifiles+=( "${valDir}/2024Jun21_vars_mY90_mX488_3b.txt" )
ifiles+=( "${valDir}/2024Jun21_vars_mY90_mX648_3b.txt" )
ifiles+=( "${valDir}/2024Jun21_vars_mY90_mX960_3b.txt" )
ifiles+=( "${valDir}/2024Jun21_vars_mY90_mX340to1216_3b.txt" )

function filterLines {
    local aPattern=$1
    local afile=$2
    sed -i -e "${aPattern}" ${afile}
}

for ifile in "${ifiles[@]}"; do

    filterLines '/^Processing/d' ${ifile}
    filterLines 's/selectionbJets\_//' ${ifile}
    filterLines 's/Blinded//' ${ifile}
    filterLines '/^datasetName/d' ${ifile}
    filterLines '/^ggF_Hbb/,+1d' ${ifile}
    filterLines '/^ttH/d' ${ifile}
    filterLines '/^ttbar/d' ${ifile}
    filterLines '/^WH/d' ${ifile}
    filterLines '/BKG/d' ${ifile}
    filterLines "s/data_BTagCSV_dataDriven_kinFit/model/" ${ifile}
    filterLines "s/data_BTagCSV/data/" ${ifile}
    filterLines '/^201/i\\' ${ifile}

    # https://unix.stackexchange.com/a/700691/617885
    filterLines '/Sample/{x;/./!{x;h;b;};d}' ${ifile}

    sed -i -e '/Sample/ { h; $p; d; }' -e '$G' ${ifile} ${ifile}
done

