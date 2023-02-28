# inTag=2022May5_RightSide
# inTag=2022May5_LeftSide
# inTag=2022May19_OutBDTtoOutCR
# inTag=2022May19_OutBDTtoInCR
# inTag=2022May19_InBDTtoInCR
# inTag=2022May19_InBDTtoOutCR
bbbbDir=/uscms/homes/a/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/
# testDir=BDTsyst_2022Apr
testDir=fullSubmission_2022July
plotsDir=${bbbbDir}VarPlots/rootHists/${testDir}/
cd ${bbbbDir}
echo "make empty VR directories"
mkdir ${plotsDir}2016DataPlots_$1_VR
mkdir ${plotsDir}2017DataPlots_$1_VR
mkdir ${plotsDir}2018DataPlots_$1_VR
echo "unroll VR"
source ${bbbbDir}/scripts/UnrollAllSubdirValidationTest.sh ${testDir}/2016 $1
source ${bbbbDir}/scripts/UnrollAllSubdirValidationTest.sh ${testDir}/2017 $1
source ${bbbbDir}/scripts/UnrollAllSubdirValidationTest.sh ${testDir}/2018 $1
echo "move unrolled VR plots"
mv ${plotsDir}2016DataPlots_$1/outPlotter_massGroup* ${plotsDir}2016DataPlots_$1_VR
mv ${plotsDir}2017DataPlots_$1/outPlotter_massGroup* ${plotsDir}2017DataPlots_$1_VR
mv ${plotsDir}2018DataPlots_$1/outPlotter_massGroup* ${plotsDir}2018DataPlots_$1_VR
echo "unroll CR"
source ${bbbbDir}/scripts/UnrollAllSubdirControlTest.sh ${testDir}/2016 $1
source ${bbbbDir}/scripts/UnrollAllSubdirControlTest.sh ${testDir}/2017 $1
source ${bbbbDir}/scripts/UnrollAllSubdirControlTest.sh ${testDir}/2018 $1
