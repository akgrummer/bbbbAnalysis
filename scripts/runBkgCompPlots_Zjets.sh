#!/bin/bash

# TString tag= "2024Jun11_vars"; TString mYlabel = ""; TString sample="4b Sample";
#

saveVals=false

function runComp {
    local tag=$1
    local tag2=$2
    local mYlabel=$3
    local sample=$4
    local vsMY=$5
    local ayear=$6
    local outValsDir="bkgCompValues/Zjets204Jun30/"
    if [ "${saveVals}" = true ]; then
        echo "Output values in: ${outValsDir}${tag}.txt"
        root -l -b -q "./scripts/privateScript/StackPlots_mY90GeV_Zjets.C(\"${tag}\", \"${tag2}\", \"${mYlabel}\", \"${sample}\", \"${vsMY}\", \"${ayear}\")" >> "${outValsDir}${tag}.txt"
    else
        echo "running: ${tag2}"
        root -l -b -q "./scripts/privateScript/StackPlots_mY90GeV_Zjets.C(\"${tag}\", \"${tag2}\", \"${mYlabel}\", \"${sample}\", \"${vsMY}\", \"${ayear}\" )" > /dev/null
        # root -l -b -q "./scripts/privateScript/StackPlots_mY90GeV_Zjets.C"
    fi
}

# Orig (used for getting yields in different regions
# plots vs mX
# fj
#

tags=("2024Jun11_vars")
tags+=("2024Jun11_vars_3b")
tags+=("2024Jun11_vars_mY90pm10")
tags+=("2024Jun11_vars_mY90pm10_3b")
tags+=("2024Jun21_vars_mY90_mX340")
tags+=("2024Jun21_vars_mY90_mX488")
tags+=("2024Jun21_vars_mY90_mX648")
tags+=("2024Jun21_vars_mY90_mX960")
tags+=("2024Jun21_vars_mY90_mX340to1216")
tags+=("2024Jun21_vars_mY90_mX340_3b")
tags+=("2024Jun21_vars_mY90_mX488_3b")
tags+=("2024Jun21_vars_mY90_mX648_3b")
tags+=("2024Jun21_vars_mY90_mX960_3b")
tags+=("2024Jun21_vars_mY90_mX340to1216_3b")

for atag in "${tags[@]}"; do
    mkdir -p "VarPlots/BkgCompositionZjets2024Jun30_pngs/${atag}"
done

#
years=("2016")
years+=("2017")
years+=("2018")
#


for ayear in "${years[@]}"; do
    runComp "2024Jun11_vars"             "2024Jun30_vars_Zjets"                ""          "4b Sample" "false" "${ayear}"
    runComp "2024Jun11_vars_3b"          "2024Jun30_vars_Zjets_3b"             ""          "3b Sample" "false" "${ayear}"
    runComp "2024Jun11_vars_mY90pm10"    "2024Jun30_vars_Zjets_mY90pm10"       "80<mY<100" "4b Sample" "false" "${ayear}"
    runComp "2024Jun11_vars_mY90pm10_3b" "2024Jun30_vars_Zjets_mY90pm10_3b"    "80<mY<100" "3b Sample" "false" "${ayear}"
    # # runComp "2024Jun11_vars_mY90pm1"     "89<mY<91"  "4b Sample" "false"
    # # runComp "2024Jun11_vars_mY90pm1_3b"  "89<mY<91"  "3b Sample" "false"

    # # plots vs mY

    runComp "2024Jun21_vars_mY90_mX340"          "2024Jun30_vars_mY90_Zjets_mX340"         "340<mX<488" "4b Sample" "true" "${ayear}"
    runComp "2024Jun21_vars_mY90_mX488"          "2024Jun30_vars_mY90_Zjets_mX488"         "488<mX<648" "4b Sample" "true" "${ayear}"
    runComp "2024Jun21_vars_mY90_mX648"          "2024Jun30_vars_mY90_Zjets_mX648"         "648<mX<960" "4b Sample" "true" "${ayear}"
    runComp "2024Jun21_vars_mY90_mX960"          "2024Jun30_vars_mY90_Zjets_mX960"         "960<mX<1216" "4b Sample" "true" "${ayear}"
    runComp "2024Jun21_vars_mY90_mX340to1216"    "2024Jun30_vars_mY90_Zjets_mX340to1216"   "340<mX<1216" "4b Sample" "true" "${ayear}"

    runComp "2024Jun21_vars_mY90_mX340_3b"       "2024Jun30_vars_mY90_Zjets_mX340_3b"         "340<mX<488" "3b Sample" "true" "${ayear}"
    runComp "2024Jun21_vars_mY90_mX488_3b"       "2024Jun30_vars_mY90_Zjets_mX488_3b"         "488<mX<648" "3b Sample" "true" "${ayear}"
    runComp "2024Jun21_vars_mY90_mX648_3b"       "2024Jun30_vars_mY90_Zjets_mX648_3b"         "648<mX<960" "3b Sample" "true" "${ayear}"
    runComp "2024Jun21_vars_mY90_mX960_3b"       "2024Jun30_vars_mY90_Zjets_mX960_3b"         "960<mX<1216" "3b Sample" "true" "${ayear}"
    runComp "2024Jun21_vars_mY90_mX340to1216_3b" "2024Jun30_vars_mY90_Zjets_mX340to1216_3b"   "340<mX<1216" "3b Sample" "true" "${ayear}"
done

