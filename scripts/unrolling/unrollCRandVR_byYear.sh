# inTag=2022May5_RightSide
# inTag=2022May5_LeftSide
# inTag=2022May19_OutBDTtoOutCR
# inTag=2022May19_OutBDTtoInCR
# inTag=2022May19_InBDTtoInCR
# inTag=2022May19_InBDTtoOutCR
bbbbDir=/uscms/homes/a/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/
# testDir=BDTsyst_2022Apr
testDir=fullSubmission_2022Nov
plotsDir=${bbbbDir}VarPlots/rootHists/${testDir}/
year=$2
cd ${bbbbDir}
# echo "make empty VR directories"
# mkdir -p ${plotsDir}${year}DataPlots_$1_VR
# echo "unroll VR"
# source ${bbbbDir}/scripts/UnrollAllSubdirValidationTest.sh ${testDir}/${year} $1
# echo "move unrolled VR plots"
# mv ${plotsDir}${year}DataPlots_$1/outPlotter_massGroup* ${plotsDir}${year}DataPlots_$1_VR
# echo "unroll CR"
# source ${bbbbDir}/scripts/UnrollAllSubdirControlTest.sh ${testDir}/${year} $1
# source ${bbbbDir}/scripts/UnrollAllSubdir.sh ${testDir}/${year} $1

# not using this file anymore!! 
# just running: 2016DataPlots_2022Nov14_bJetScoreLoose_shapes2
# this file was intended for validation and control region test
