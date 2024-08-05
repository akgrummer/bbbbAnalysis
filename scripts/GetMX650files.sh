#!/bin/bash


# /NMSSM_XToYHTo4B_MX-650_MY-100_TuneCP5_13TeV-madgraph-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM
# /NMSSM_XToYHTo4B_MX-650_MY-100_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v2/NANOAODSIM
# /NMSSM_XToYHTo4B_MX-650_MY-100_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v2/NANOAODSIM

saveDatasetNames(){
    mYval=${1}
    year=${2}
    if [ ${year} -eq 2016 ]; then
        datasetQuery="file dataset=/NMSSM_XToYHTo4B_MX-650_MY-${mYval}_TuneCP5_13TeV-madgraph-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM"
    fi
    if [ ${year} -eq 2017 ]; then
        datasetQuery="file dataset=/NMSSM_XToYHTo4B_MX-650_MY-${mYval}_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v2/NANOAODSIM"
    fi
    if [ ${year} -eq 2018 ]; then
        datasetQuery="file dataset=/NMSSM_XToYHTo4B_MX-650_MY-${mYval}_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v2/NANOAODSIM"
    fi
    # dasgoclient -query "${datasetQuery}" >> "MoreSignals/MX650/NMSSM_XToYHTo4B_MX-650_MY-${mYval}_${year}.txt"
    dasgoclient -query "${datasetQuery}" >> "/uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/MoreSignals/MX650/NMSSM_XToYHTo4B_MX-650_MY-${mYval}_${year}.txt"

}


# year=2016
# anMY=60
for year in 2016 2017 2018; do
    for anMY in 60 70 80 90 100 125 150 190 250 300 350 400 450 500; do
        saveDatasetNames ${anMY} ${year}
        ofile="MoreSignals/MX650/NMSSM_XToYHTo4B_MX-650_MY-${mYval}_${year}.txt"
        sed -i s#^#root://cmsxrootd.fnal.gov/# ${ofile}
        # same as: wc -l ${ofile} but can print without new line
        awk 'END{printf "files=%.0f ", NR}' ${ofile}
        echo -n "for mY:${mYval}, ${year}" ${ofile}" "
        awk 'a[$0]++{print "!!! there are DUPLICATE LINES"; exit(1)}' ${ofile} && echo "(lines are unique)"
    done;
done

