# -  Nominal BDT:
# --new trainings - with pt and ht cuts matching the HLT thresholds - and without Xpt
# python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2016_v27_BDTweights_2023Feb28
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2017_v27_BDTweights_2023Feb28
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2018_v27_BDTweights_2023Feb28
    
# - Shape UP:
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2016_v27_BDTweights_2023Feb28_shapeUp
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2017_v27_BDTweights_2023Feb28_shapeUp
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2018_v27_BDTweights_2023Feb28_shapeUp

# - Shape Down:
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2016_v27_BDTweights_2023Feb28_shapeDown
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2017_v27_BDTweights_2023Feb28_shapeDown
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2018_v27_BDTweights_2023Feb28_shapeDown

# # - BDT sans_mXmY - removed mX, mY, and distance from the diagonal
# python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2016_v27_BDTweights_2023Feb28_sans_mXmY
# python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2017_v27_BDTweights_2023Feb28_sans_mXmY
# python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2018_v27_BDTweights_2023Feb28_sans_mXmY
# 
# # - BDT only_mXmY
# python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2016_v27_BDTweights_2023Feb28_only_mXmY
# python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2017_v27_BDTweights_2023Feb28_only_mXmY
# python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2018_v27_BDTweights_2023Feb28_only_mXmY
# 
# # - SANS distance from the diagonal
# python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2016_v27_BDTweights_2023Feb28_sans_dfd
# python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2017_v27_BDTweights_2023Feb28_sans_dfd
# python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2018_v27_BDTweights_2023Feb28_sans_dfd
#     
# # - Shape UP: SANS distance from the diagonal
# python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2016_v27_BDTweights_2023Feb28_shapeUp_sans_dfd
# python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2017_v27_BDTweights_2023Feb28_shapeUp_sans_dfd
# python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2018_v27_BDTweights_2023Feb28_shapeUp_sans_dfd
# 
# # - Shape Down: SANS distance from the diagonal
# python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2016_v27_BDTweights_2023Feb28_shapeDown_sans_dfd
# python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2017_v27_BDTweights_2023Feb28_shapeDown_sans_dfd
# python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BDToutput/fullSubmission_2018_v27_BDTweights_2023Feb28_shapeDown_sans_dfd
# 
