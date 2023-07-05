# TAG=2022Nov14_bJetScoreLoose_shapes2
TAG=2023Feb28_3_trim
submissionDir=fullSubmission_2022Nov
cd scripts && g++  -std=c++17 -I `root-config --incdir` -o Unroll2DplotsSubRange Unroll2DplotsSubRange.cc `root-config --libs` -O3 ; cd -

# ./scripts/Unroll2DplotsSubRange $folder/outPlotter.root data_BTagCSV_dataDriven_kinFit selectionbJets_SignalRegion HH_kinFit_m_H2_m 0 selectionbJets_ValidationRegionBlinded
./scripts/Unroll2DplotsSubRange VarPlots/rootHists/${submissionDir}/2016DataPlots_${TAG}/outPlotter.root data_BTagCSV_dataDriven_kinFit selectionbJets_SignalRegion HH_kinFit_m_H2_m 0 selectionbJets_ValidationRegionBlinded
./scripts/Unroll2DplotsSubRange VarPlots/rootHists/${submissionDir}/2017DataPlots_${TAG}/outPlotter.root data_BTagCSV_dataDriven_kinFit selectionbJets_SignalRegion HH_kinFit_m_H2_m 0 selectionbJets_ValidationRegionBlinded
./scripts/Unroll2DplotsSubRange VarPlots/rootHists/${submissionDir}/2018DataPlots_${TAG}/outPlotter.root data_BTagCSV_dataDriven_kinFit selectionbJets_SignalRegion HH_kinFit_m_H2_m 0 selectionbJets_ValidationRegionBlinded
# ./scripts/Unroll2DplotsSubRange VarPlots/rootHists/$1DataPlots_$2/outPlotter.root data_BTagCSV_dataDriven_kinFit selectionbJets_SignalRegion HH_kinFit_m_H2_m 0
# ./scripts/Unroll2DplotsSubRange VarPlots/rootHists/$1DataPlots_$2/outPlotter.root data_BTagCSV_dataDriven_kinFit selectionbJets_SignalRegion HH_kinFit_m_H2_m 0
# ./scripts/Unroll2DplotsSubRange VarPlots/rootHists/$1DataPlots_$2/outPlotter.root data_BTagCSV_dataDriven_kinFit selectionbJets_SignalRegion HH_kinFit_m_H2_m 0
# ./scripts/Unroll2DplotsSubRange VarPlots/rootHists/$1DataPlots_$2/outPlotter.root data_BTagCSV_dataDriven_kinFit selectionbJets_SignalRegion HH_kinFit_m_H2_m 0
