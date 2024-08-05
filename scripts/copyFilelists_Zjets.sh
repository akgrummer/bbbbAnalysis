#!/bin/bash

copyFilelist(){
    local htRange=${1}
    local year=${2}

    ofileName="plotterListFiles/${year:0:4}Resonant_NMSSM_XYH_bbbb/FileList_ZJetsToQQ_HT-${htRange}_${year}.txt"
    eosdir="/eos/uscms/store/user/agrummer/bbbb_ntuples/"
    tagDir="Zjets_${year}_HT${htRange}2/"
    tagDir2="SKIM_ZJetsToQQ_HT-${htRange}_TuneCP5_13TeV-madgraphMLM-pythia8"

    thefindArgs="${eosdir}${tagDir}${tagDir2}/output/ -name bbbbNtuple_*.root |sort"
    theSedArgs="s#/eos/uscms/#root://cmseos.fnal.gov//#g"

    # find /eos/uscms/store/user/agrummer/bbbb_ntuples/Zjets_2016_HT200to4002/SKIM_ZJetsToQQ_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/output/ -name bbbbNtuple_*.root |sort
    echo "find ${thefindArgs} >> ${ofileName}"
    echo "sed -i -e '${theSedArgs}' ${ofileName}"
    # find "${thefindArgs} >> ${ofileName}"
    # sed -i -e ${theSedArgs} ${ofileName}
}


# ayear=2016
# anMY=60
# submitSkimsForMassPoint ${anMY} ${ayear}
# copyFilelist "200to400"  "2016"

for ayear in "2016preVFP" "2016" "2017" "2018"; do
        copyFilelist "200to400"  ${ayear}
        copyFilelist "400to600"  ${ayear}
        copyFilelist "600to800"  ${ayear}
        copyFilelist "800toInf"  ${ayear}
done

