TAG=2022Nov14_bJetScoreLoose_shapes2_UNROLLED
submissionDir=fullSubmission_2022Nov
cd scripts && g++  -std=c++17 -I `root-config --incdir` -o Unroll2Dplots Unroll2Dplots.cc `root-config --libs` -O3 ; cd -

# ./scripts/Unroll2DplotsSubRange $folder/outPlotter.root data_BTagCSV_dataDriven_kinFit selectionbJets_SignalRegion HH_kinFit_m_H2_m 0 selectionbJets_ValidationRegionBlinded
# ./scripts/Unroll2Dplots VarPlots/rootHists/$1DataPlots_$2/outPlotter.root data_BTagCSV_dataDriven_kinFit selectionbJets_SignalRegion HH_kinFit_m_H2_m 0
./scripts/Unroll2Dplots VarPlots/rootHists/${submissionDir}/2016DataPlots_${TAG}/outPlotter.root data_BTagCSV_dataDriven_kinFit selectionbJets_SignalRegion HH_kinFit_m_H2_m 0 2400 0
./scripts/Unroll2Dplots VarPlots/rootHists/${submissionDir}/2017DataPlots_${TAG}/outPlotter.root data_BTagCSV_dataDriven_kinFit selectionbJets_SignalRegion HH_kinFit_m_H2_m 0 2400 0
./scripts/Unroll2Dplots VarPlots/rootHists/${submissionDir}/2018DataPlots_${TAG}/outPlotter.root data_BTagCSV_dataDriven_kinFit selectionbJets_SignalRegion HH_kinFit_m_H2_m 0 2400 0
