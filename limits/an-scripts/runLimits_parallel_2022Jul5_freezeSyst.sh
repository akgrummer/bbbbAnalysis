histsDir=/uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/VarPlots/rootHists
limitsDir=/uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/limits
combineDir=localCombineRuns

limitsTagDir=$1
limitsTag=$2
# limitsTag=2022Mar17_fullBDT_TTBAR_MassWindow_data
# limitsTag=2022Mar17_fullBDT_TTBAR_MassWindow_data_VR
# limitsTag=2022Mar28_binsReordered
# limitsTag=2022Mar28_binsReordered_VR
# . runLimits_parallel_2022Mar28.sh 2022Mar29_DATAbinsReordered_20bins_lt1p2ratio_VR
paramToFreeze=$3_
outputDir=${combineDir}/freezeParams/$3/$limitsTag

for year in 2016 2017 2018
do
    limitsDirectory=${histsDir}/${limitsTagDir}/${year}DataPlots_${limitsTag}/
    limitsFolder=${limitsDir}/${outputDir}/Limits_kinFit_${year}/sig_NMSSM_bbbb_MX_600_MY_400
    #  limitsFolder=/uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/limits/$outputDir/Limits_kinFit_$year/\$\{signalTemplate\}

    # echo $limitsDirectory
    # echo $limitsFolder


    echo "##################################################"
    echo $year
    echo "##################################################"
    echo "preparing histos" $year
    python prepareModels/prepareHistos.py --config prepareModels/config/LimitsConfig_$year.cfg --signal sig_NMSSM_bbbb_MX_600_MY_400 --group 0 --folder $limitsFolder --directory $limitsDirectory
    echo "##################################################"
    echo "making datacards (with card only option)" $year
    # python prepareModels/makeDatacardsAndWorkspaces.py --config prepareModels/config/LimitsConfig_$year.cfg  --no-comb --signal sig_NMSSM_bbbb_MX_600_MY_400 --bkgNorm 1.010 --folder $limitsFolder --card-only
    python prepareModels/makeDatacardsAndWorkspaces.py --config prepareModels/config/LimitsConfig_$year.cfg  --no-comb --signal sig_NMSSM_bbbb_MX_600_MY_400 --bkgNorm 1.010 --folder $limitsFolder --card-only --no-bbb
    echo "##################################################"
    echo "making workspace" $year
    text2workspace.py ${limitsFolder}/datacard${year}_selectionbJets_SignalRegion.txt >> ${limitsFolder}/text2workspace_output.txt
done
wait

echo ""
echo "##################################################"
echo "combine Cards for all years"
mkdir -p ${outputDir}/Limits_kinFit_RunII/sig_NMSSM_bbbb_MX_600_MY_400/
limitsFolderCombine=/uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/limits/${outputDir}/Limits_kinFit_RunII/sig_NMSSM_bbbb_MX_600_MY_400
combineCards.py c2016=${outputDir}/Limits_kinFit_2016/sig_NMSSM_bbbb_MX_600_MY_400/datacard2016_selectionbJets_SignalRegion.txt c2017=${outputDir}/Limits_kinFit_2017/sig_NMSSM_bbbb_MX_600_MY_400/datacard2017_selectionbJets_SignalRegion.txt c2018=${outputDir}/Limits_kinFit_2018/sig_NMSSM_bbbb_MX_600_MY_400/datacard2018_selectionbJets_SignalRegion.txt > ${outputDir}/Limits_kinFit_RunII/sig_NMSSM_bbbb_MX_600_MY_400/datacardRunII_selectionbJets_SignalRegion.txt

echo ""
echo "##################################################"
echo "make workspace for combination"
text2workspace.py ${outputDir}/Limits_kinFit_RunII/sig_NMSSM_bbbb_MX_600_MY_400/datacardRunII_selectionbJets_SignalRegion.txt >> $limitsFolderCombine/text2workspace_output.txt

echo ""
echo "##################################################"
echo "running limits in parallel: "
for year in 2016 2017 2018; do
    # combine ${limitsDir}/${outputDir}/Limits_kinFit_${year}/sig_NMSSM_bbbb_MX_600_MY_400/datacard${year}_selectionbJets_SignalRegion.root -n $year -M AsymptoticLimits --rMax 30 --X-rtd  MINIMIZER_analytic --X-rtd  FAST_VERTICAL_MORPH --freezeParameters allConstrainedNuisances >> ${limitsDir}/${outputDir}/Limits_kinFit_${year}/limits_${year}.txt &&
    cd ${outputDir}/Limits_kinFit_${year} &&
    # combine ${limitsDir}/${outputDir}/Limits_kinFit_${year}/sig_NMSSM_bbbb_MX_600_MY_400/datacard${year}_selectionbJets_SignalRegion.root -n $year -M AsymptoticLimits --rMax 30 --X-rtd  MINIMIZER_analytic --X-rtd  FAST_VERTICAL_MORPH --freezeParameters ${paramToFreeze}${year} >> ${limitsDir}/${outputDir}/Limits_kinFit_${year}/limits_${year}.txt &&
    combine ${limitsDir}/${outputDir}/Limits_kinFit_${year}/sig_NMSSM_bbbb_MX_600_MY_400/datacard${year}_selectionbJets_SignalRegion.root -n $year -M AsymptoticLimits --rMax 30 --X-rtd  MINIMIZER_analytic --X-rtd  FAST_VERTICAL_MORPH >> ${limitsDir}/${outputDir}/Limits_kinFit_${year}/limits_${year}.txt &&
    echo "completed" ${year} &
done
year=RunII
cd ${outputDir}/Limits_kinFit_${year} &&
# combine ${limitsDir}/${outputDir}/Limits_kinFit_${year}/sig_NMSSM_bbbb_MX_600_MY_400/datacard${year}_selectionbJets_SignalRegion.root -n $year -M AsymptoticLimits --rMax 30 --X-rtd  MINIMIZER_analytic --X-rtd  FAST_VERTICAL_MORPH --freezeParameters ${paramToFreeze}2016,${paramToFreeze}2017,${paramToFreeze}2018 >> ${limitsDir}/${outputDir}/Limits_kinFit_${year}/limits_${year}.txt &&
combine ${limitsDir}/${outputDir}/Limits_kinFit_${year}/sig_NMSSM_bbbb_MX_600_MY_400/datacard${year}_selectionbJets_SignalRegion.root -n $year -M AsymptoticLimits --rMax 30 --X-rtd  MINIMIZER_analytic --X-rtd  FAST_VERTICAL_MORPH >> ${limitsDir}/${outputDir}/Limits_kinFit_${year}/limits_${year}.txt &&
echo "completed" ${year}
wait

echo ""
echo "##################################################"
echo "combine completed, moving output"
for year in 2016 2017 2018 RunII; do
    # mv higgsCombine${year}.AsymptoticLimits.mH120.root $outputDir/Limits_kinFit_RunII/sig_NMSSM_bbbb_MX_600_MY_400/
    echo "Limits for" ${year} >> ${limitsDir}/${outputDir}/limits.txt 
    cat ${limitsDir}/${outputDir}/Limits_kinFit_${year}/limits_${year}.txt >> ${limitsDir}/${outputDir}/limits.txt
done

cd ${limitsDir}
