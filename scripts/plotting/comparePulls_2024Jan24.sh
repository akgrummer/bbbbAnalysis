tag="2023Dec7_binMYx2_addMX650_10ev_SR"
script="/uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py"
# script="studies/comparePulls_2024Jan24/diffNuisances.py"
# script="/uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/limits/CombineHarvester/CombineTools/scripts/plotImpacts.py"

years=( 2016 2017 2018 )
# sorts=( "impact" "correlation" )
sorts=( "impact" )
sigs=( "sig_NMSSM_bbbb_MX_700_MY_400" "sig_NMSSM_bbbb_MX_650_MY_350" )

for ayear in "${years[@]}"; do
    for asig in "${sigs[@]}"; do
        fName="FitDiagnostics/${tag}/${ayear}/FitDiagnostics_${ayear}_${asig}_id0_sig0.root"
        for asort in "${sorts[@]}"; do
            ofile="studies/comparePulls_2024Jan24/comparePulls_${asig}_${ayear}_sortedBy${asort}.txt"
            ofileHists="studies/comparePulls_2024Jan24/comparePulls_${asig}_${ayear}_sortedBy${asort}.root"
            # python ${script} --all --sortBy=${asort} --histogram ${ofileHists} ${fName} >> ${ofile}
            python ${script} --vtol 2.0 --stol 2.0 --vtol2 1.2 --stol2 1.2 --sortBy=${asort} --histogram ${ofileHists} ${fName} >> ${ofile}
        done;
    done;
done

# stol=2; vtol=2; stol2=10; vtol2=10; asort="impact"; tag="2023Dec7_binMYx2_addMX650_10ev_SR"; ayear=2016; asig="sig_NMSSM_bbbb_MX_700_MY_400"; fName="FitDiagnostics/${tag}/${ayear}/FitDiagnostics_${ayear}_${asig}_id0_sig0.root"; script="/uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py" python ${script} --vtol ${vtol} --stol ${stol} --vtol2 ${vtol2} --stol2 ${stol2} --sortBy=${asort} --histogram example.root ${fName}
