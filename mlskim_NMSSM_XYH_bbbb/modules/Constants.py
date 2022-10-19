
modelFileName        = 'reweighterModel.pkl'
outputConfigFileName = 'reweighterConfig.cfg'
eosPath              = 'root://cmseos.fnal.gov'
nTuplesPath          = '/store/user/agrummer/bbbb_ntuples/'
#  outputDirPrefix      = "BackgroundModels/Reweight_"
#  outputDirPrefix      = "VariablePlots_2022Feb/"
#  outputDirPrefix      = "BDToutput/MassWindowTraining_2022Feb/"
outputDirPrefix      = "BDToutput/"
logFileName          = 'BDTreweight.log'
treeName             = "bbbbTree"
weightBranchPrefix   = "Weight_forBackground_"
minVariableList      = ['H1_b1_pt', 'H1_b2_pt', 'H2_b1_pt', 'H2_b2_pt', 'H1_b1_ptRegressed', 'H1_b2_ptRegressed', 'H2_b1_ptRegressed', 'H2_b2_ptRegressed', 'H1_b1_eta', 'H1_b2_eta', 'H2_b1_eta', 'H2_b2_eta']
# for mass window selection study:
