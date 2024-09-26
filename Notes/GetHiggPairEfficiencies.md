effiency, match, matching, Pair, candidate, jet, b-jet,

used for Twiki response:
2b:
https://twiki.cern.ch/twiki/bin/viewauth/CMS/Run2XYHinto4BReview#5_Maria_s_questions_previous_to
studies the correctly identified b-jets of the preselected b-jets
"privateTools/GetGenMatch.C"

This one saves some plots for pairing efficiency:
"privateTools/GetGenMatch_higgsPair_2024Aug.C" line 398

This one saves a tree with values over a range of delta R values used in matching formula:
"privateTools/GetGenMatch_higgsPair_2024Aug_tree.C" line 390
then plotting is done on local computer with code:
/Users/agrummer/Documents/Fermilab/DiHiggs/plotting/higgsPairEff/plotPairEfficiency.C


Looked at branch names in skimmed files:
studies/BranchNames/bbbbNtuple_0_bbbbTree.txt
and branch names in nanoaods:
studies/BranchNames/73604338-57D0-0144-8089-C23BB6168001_Events.txt

used studies/BranchNames/BranchNamesMacro_withType.cpp
compiled with:
g++ BranchNamesMacro_withType.cpp -o BranchNamesMacro_withType `root-config --glibs --cflags`

run with:
./studies/BranchNames/BranchNamesMacro_withType 73604338-57D0-0144-8089-C23BB6168001.root

copied nano aod with xrdcp
xrdcp root://cmsxrootd.fnal.gov//store//mc/RunIISummer16NanoAODv6/NMSSM_XToYHTo4b_MX-700_TuneCUETP8M1_13TeV-madgraph-pythia8/NANOAODSIM/PUSummer16v3Fast_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/120000/73604338-57D0-0144-8089-C23BB6168001.root .

but removed the 1.2G file


