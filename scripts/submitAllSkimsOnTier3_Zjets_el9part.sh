#!/bin/bash

el9part="false"

submitSkimsForMassPoint(){
    local htRange=${1}
    local year=${2}
    local crossSection=${3}



    # submitTag="moreSignalsSubmission_2017"
    submitTag="Zjets_${year}_HT${htRange}"
    fileName="ZJetsToQQ_HT-${htRange}_TuneCP5_13TeV-madgraphMLM-pythia8.txt"
    inputFiles="inputFiles/Zjets/${year}/${fileName}.txt"
    configFile="config/Resonant_NMSSM_bbbb/skim_${year}Resonant_NMSSM_XYH_bbbb_UL.cfg"
    weightFile="weights/Zjets/${year}/${fileName}_PUweights.root"
    numberOfJobs=2

    # --append=_MY_60
    # --yMassSelection=60

    if [ "${el9part}" == "true" ]; then
        submitScript="scripts/submitSkimOnTier3_el9part.py"
        python3 ${submitScript} \
            --input=${inputFiles}   \
            --tag=${submitTag} \
            --njobs=${numberOfJobs}
    else
        submitScript="scripts/submitSkimOnTier3.py"
        python ${submitScript} \
            --input=${inputFiles}   \
            --tag=${submitTag} \
            --cfg=${configFile}  \
            --puWeight=${weightFile}  \
            --xs=${crossSection}   \
            --njobs=${numberOfJobs}
    fi

}


# ayear=2016
# anMY=60
# submitSkimsForMassPoint ${anMY} ${ayear}

submitSkimsForMassPoint "200to400"  "2016" "1012.0"
# for ayear in "2016preVFP" "2016" "2017" "2018"; do
#         submitSkimsForMassPoint "200to400"  ${ayear} "1012.0"
#         submitSkimsForMassPoint "400to600"  ${ayear} "114.5"
#         submitSkimsForMassPoint "600to800"  ${ayear} "25.41"
#         submitSkimsForMassPoint "800toInf"  ${ayear} "12.91"
#     done;
# done

