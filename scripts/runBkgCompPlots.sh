#!/bin/bash

# TString tag= "2024Jun11_vars"; TString mYlabel = ""; TString sample="4b Sample";
#

saveVals=false

function runComp {
    local tag=$1
    local mYlabel=$2
    local sample=$3
    local vsMY=$4
    if [ "${saveVals}" = true ]; then
        echo "Output values in: bkgCompValues/${tag}.txt"
        root -l -b -q "./scripts/privateScript/StackPlots_mY90GeV.C(\"${tag}\", \"${mYlabel}\", \"${sample}\", \"${vsMY}\")" > "bkgCompValues/${tag}.txt"
    else
        root -l -b -q "./scripts/privateScript/StackPlots_mY90GeV.C(\"${tag}\", \"${mYlabel}\", \"${sample}\", \"${vsMY}\" )" > /dev/null
    fi
}

# Orig (used for getting yields in different regions
# plots vs mX
runComp "2024Jun11_vars"             ""          "4b Sample" "false"
runComp "2024Jun11_vars_3b"          ""          "3b Sample" "false"
runComp "2024Jun11_vars_mY90pm10"    "80<mY<100" "4b Sample" "false"
runComp "2024Jun11_vars_mY90pm1"     "89<mY<91"  "4b Sample" "false"
runComp "2024Jun11_vars_mY90pm10_3b" "80<mY<100" "3b Sample" "false"
runComp "2024Jun11_vars_mY90pm1_3b"  "89<mY<91"  "3b Sample" "false"

# plots vs mY
runComp "2024Jun21_vars_mY90_mX340" "340<mX<488" "4b Sample" "true"
runComp "2024Jun21_vars_mY90_mX488" "488<mX<648" "4b Sample" "true"
runComp "2024Jun21_vars_mY90_mX648" "648<mX<960" "4b Sample" "true"
runComp "2024Jun21_vars_mY90_mX960" "960<mX<1216" "4b Sample" "true"
runComp "2024Jun21_vars_mY90_mX340to1216" "340<mX<1216" "4b Sample" "true"

runComp "2024Jun21_vars_mY90_mX340_3b" "340<mX<488" "3b Sample" "true"
runComp "2024Jun21_vars_mY90_mX488_3b" "488<mX<648" "3b Sample" "true"
runComp "2024Jun21_vars_mY90_mX648_3b" "648<mX<960" "3b Sample" "true"
runComp "2024Jun21_vars_mY90_mX960_3b" "960<mX<1216" "3b Sample" "true"
runComp "2024Jun21_vars_mY90_mX340to1216_3b" "340<mX<1216" "3b Sample" "true"

