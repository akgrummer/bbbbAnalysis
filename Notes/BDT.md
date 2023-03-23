# These notes are for running and applying the background model BDT

The vim session file is:
vim-sessions/BDT.vim

current files list (as of 2023Feb28)

mlskim_NMSSM_XYH_bbbb/BuildBackgroundModel.py
mlskim_NMSSM_XYH_bbbb/config/outputskim_2016_Full_kinFit.cfg
mlskim_NMSSM_XYH_bbbb/config/outputskim_2017_Full_kinFit.cfg
mlskim_NMSSM_XYH_bbbb/config/outputskim_2018_Full_kinFit.cfg
mlskim_NMSSM_XYH_bbbb/modules/ConfigurationReader.py
Notes/BDT.md
vim-sessions/BDT.vim

## 2023 Feb 28

Rerunning the BDT now with pT Selections to match the HLT selections

- Edit the config files and run:

python mlskim_NMSSM_XYH_bbbb/BuildBackgroundModel.py --config mlskim_NMSSM_XYH_bbbb/config/outputskim_2016_Full_kinFit.cfg --bJetScore
python mlskim_NMSSM_XYH_bbbb/BuildBackgroundModel.py --config mlskim_NMSSM_XYH_bbbb/config/outputskim_2017_Full_kinFit.cfg --bJetScore
python mlskim_NMSSM_XYH_bbbb/BuildBackgroundModel.py --config mlskim_NMSSM_XYH_bbbb/config/outputskim_2018_Full_kinFit.cfg --bJetScore

## BDT variants 

Total of 5 trainings
- nominal - all vars used in training (minus XpT, and nominal CR bands
- Shapes UP and DOWN - all vars, alternate CR bands
- altVars - only MX and MY, and without MX, MY and distance from diagonal

## Apply BDT weights:

-  Nominal BDT:
--new trainings - with pt and ht cuts matching the HLT thresholds - and without Xpt
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2016_v27_BDTweights_2023Feb28
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2017_v27_BDTweights_2023Feb28
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2018_v27_BDTweights_2023Feb28
    
- Shape UP:
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2016_v27_BDTweights_2023Feb28_shapeUp
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2017_v27_BDTweights_2023Feb28_shapeUp
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2018_v27_BDTweights_2023Feb28_shapeUp

- Shape Down:
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2016_v27_BDTweights_2023Feb28_shapeDown
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2017_v27_BDTweights_2023Feb28_shapeDown
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2018_v27_BDTweights_2023Feb28_shapeDown

- BDT sans_mXmY - removed mX, mY, and distance from the diagonal
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2016_v27_BDTweights_2023Feb28_sans_mXmY
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2017_v27_BDTweights_2023Feb28_sans_mXmY
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2018_v27_BDTweights_2023Feb28_sans_mXmY

- BDT only_mXmY
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2016_v27_BDTweights_2023Feb28_only_mXmY
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2017_v27_BDTweights_2023Feb28_only_mXmY
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2018_v27_BDTweights_2023Feb28_only_mXmY

- SANS distance from the diagonal
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2016_v27_BDTweights_2023Feb28_sans_dfd
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2017_v27_BDTweights_2023Feb28_sans_dfd
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2018_v27_BDTweights_2023Feb28_sans_dfd
    
- Shape UP: SANS distance from the diagonal
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2016_v27_BDTweights_2023Feb28_shapeUp_sans_dfd
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2017_v27_BDTweights_2023Feb28_shapeUp_sans_dfd
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2018_v27_BDTweights_2023Feb28_shapeUp_sans_dfd

- Shape Down: SANS distance from the diagonal
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2016_v27_BDTweights_2023Feb28_shapeDown_sans_dfd
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2017_v27_BDTweights_2023Feb28_shapeDown_sans_dfd
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2018_v27_BDTweights_2023Feb28_shapeDown_sans_dfd


- Nominal vars, offshell
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2016_v27_BDTweights_2023Feb28_offshell
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2017_v27_BDTweights_2023Feb28_offshell
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2018_v27_BDTweights_2023Feb28_offshell

!!!Dont run these in parallel!

- Nominal vars, offshell, added blinding for offshell h1 and h2
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2016_v27_BDTweights_2023Mar23_offshell_blind
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2017_v27_BDTweights_2023Mar23_offshell_blind
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2018_v27_BDTweights_2023Mar23_offshell_blind

