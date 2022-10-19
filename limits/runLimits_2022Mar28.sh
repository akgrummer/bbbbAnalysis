# year=2016

histsDir=/uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/VarPlots/rootHists
limitsDir=/uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/limits
combineDir=localCombineRuns

limitsTag=$1
# limitsTag=2022Mar17_fullBDT_TTBAR_MassWindow_data
# limitsTag=2022Mar17_fullBDT_TTBAR_MassWindow_data_VR
# limitsTag=2022Mar28_binsReordered
# limitsTag=2022Mar28_binsReordered_VR
outputDir=${combineDir}/$limitsTag

for year in 2016 2017 2018
do
    limitsDirectory=${histsDir}/${year}DataPlots_${limitsTag}/
    limitsFolder=${limitsDir}/${outputDir}/Limits_kinFit_${year}/sig_NMSSM_bbbb_MX_600_MY_400
    #  limitsFolder=/uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/limits/$outputDir/Limits_kinFit_$year/\$\{signalTemplate\}

    # echo $limitsDirectory
    # echo $limitsFolder


    echo "##################################################"
    echo $year
    echo "##################################################"
    echo "running prepareHistos.py" $year
    python prepareModels/prepareHistos.py --config prepareModels/config/LimitsConfig_$year.cfg --signal sig_NMSSM_bbbb_MX_600_MY_400 --group 0 --folder $limitsFolder --directory $limitsDirectory
    echo ""
    echo "##################################################"
    echo "running makeDatacardsAndWorkspaces.py (with card only option)"

    python prepareModels/makeDatacardsAndWorkspaces.py --config prepareModels/config/LimitsConfig_$year.cfg  --no-comb --signal sig_NMSSM_bbbb_MX_600_MY_400 --bkgNorm 1.010 --folder $limitsFolder --card-only

    echo ""
    echo "##################################################"
    echo "running text2workspace.py" $year

    text2workspace.py ${limitsFolder}/datacard${year}_selectionbJets_SignalRegion.txt >> ${limitsFolder}/text2workspace_output.txt

    # sleep 10

    echo ""
    echo "##################################################"
    echo "running combine" $year 

    echo "Limits for" $year >> ${outputDir}/limits.txt 
    combine ${outputDir}/Limits_kinFit_${year}/sig_NMSSM_bbbb_MX_600_MY_400/datacard${year}_selectionbJets_SignalRegion.root -M AsymptoticLimits --rMax 30 --X-rtd  MINIMIZER_analytic --X-rtd  FAST_VERTICAL_MORPH >> ${outputDir}/limits.txt

    mv higgsCombineTest.AsymptoticLimits.mH120.root $outputDir/Limits_kinFit_$year/sig_NMSSM_bbbb_MX_600_MY_400/
done

echo "##################################################"
echo "running combination of all years"
mkdir -p ${outputDir}/Limits_kinFit_RunII/sig_NMSSM_bbbb_MX_600_MY_400/
limitsFolderCombine=/uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/limits/${outputDir}/Limits_kinFit_RunII/sig_NMSSM_bbbb_MX_600_MY_400


echo ""
echo "##################################################"
echo "running combineCards.py (for all years)"
combineCards.py c2016=${outputDir}/Limits_kinFit_2016/sig_NMSSM_bbbb_MX_600_MY_400/datacard2016_selectionbJets_SignalRegion.txt c2017=${outputDir}/Limits_kinFit_2017/sig_NMSSM_bbbb_MX_600_MY_400/datacard2017_selectionbJets_SignalRegion.txt c2018=${outputDir}/Limits_kinFit_2018/sig_NMSSM_bbbb_MX_600_MY_400/datacard2018_selectionbJets_SignalRegion.txt > ${outputDir}/Limits_kinFit_RunII/sig_NMSSM_bbbb_MX_600_MY_400/datacardRunII_selectionbJets_SignalRegion.txt

echo ""
echo "##################################################"
echo "text2workspace.py (for all years)"
text2workspace.py ${outputDir}/Limits_kinFit_RunII/sig_NMSSM_bbbb_MX_600_MY_400/datacardRunII_selectionbJets_SignalRegion.txt >> $limitsFolderCombine/text2workspace_output.txt

echo ""
echo "##################################################"
echo "combine (for all years)"
echo "Limits for Run II" >> ${outputDir}/limits.txt 
combine ${outputDir}/Limits_kinFit_RunII/sig_NMSSM_bbbb_MX_600_MY_400/datacardRunII_selectionbJets_SignalRegion.root -M AsymptoticLimits --rMax 30 --X-rtd  MINIMIZER_analytic --X-rtd  FAST_VERTICAL_MORPH >> ${outputDir}/limits.txt

mv higgsCombineTest.AsymptoticLimits.mH120.root $outputDir/Limits_kinFit_RunII/sig_NMSSM_bbbb_MX_600_MY_400/

