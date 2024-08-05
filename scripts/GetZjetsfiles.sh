#!/bin/bash


saveDatasetNames(){
    # should probabaly be local variables:
    htRange=${1}
    year=${2}
    if [ "${year}" == "2016preVFP" ]; then
        datasetQuery="file dataset=/ZJetsToQQ_HT-${htRange}_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM"
    fi
    if [ ${year} == "2016" ]; then
        datasetQuery="file dataset=/ZJetsToQQ_HT-${htRange}_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v2/NANOAODSIM"
    fi
    if [ ${year} == "2017" ]; then
        datasetQuery="file dataset=/ZJetsToQQ_HT-${htRange}_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM"
    fi
    if [ ${year} == "2018" ]; then
        datasetQuery="file dataset=/ZJetsToQQ_HT-${htRange}_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM"
    fi
    # dasgoclient -query "${datasetQuery}" >> "MoreSignals/MX650/NMSSM_XToYHTo4B_MX-650_MY-${mYval}_${year}.txt"
    dasgoclient -query "${datasetQuery}" > "/uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/inputFiles/Zjets/${year}/ZJetsToQQ_HT-${htRange}_TuneCP5_13TeV-madgraphMLM-pythia8.txt"

}


# year="2016"
# anHTrange="200to400"
for year in "2016preVFP" "2016" "2017" "2018"; do
    for anHTrange in "200to400" "400to600" "600to800" "800toInf" ; do
        saveDatasetNames ${anHTrange} ${year}
        ofile="inputFiles/Zjets/${year}/ZJetsToQQ_HT-${htRange}_TuneCP5_13TeV-madgraphMLM-pythia8.txt"
        sort ${ofile} -o ${ofile}
        sed -i s#^#root://cmsxrootd.fnal.gov/# ${ofile}
        # same as: wc -l ${ofile} but can print without new line
        awk 'END{printf "files=%.0f ", NR}' ${ofile}
        echo -n "for htRange:${anHTrange}, ${year}" ${ofile}" "
        awk 'a[$0]++{print "!!! there are DUPLICATE LINES"; exit(1)}' ${ofile} && echo "(lines are unique)"
        echo "" >> ${ofile}
    done;
done

