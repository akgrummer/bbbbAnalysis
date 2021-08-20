folder=$1

cd scripts && g++  -std=c++17 -I `root-config --incdir` -o Unroll2DplotsSubRange Unroll2DplotsSubRange.cc `root-config --libs` -O3 ; cd -

./scripts/Unroll2DplotsSubRange $folder/outPlotter.root data_BTagCSV_dataDriven_kinFit selectionbJets_SignalRegion HH_kinFit_m_H2_m 0 selectionbJets_ValidationRegionBlinded
