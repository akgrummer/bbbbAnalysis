# tag=2022Jul7_fullBDT_bJetScoreLoose
# tag=2022Jul14_fullBDT_bJetScore1p5
# tag=2022Aug1_fullBDT_bJetLoose_CutLowMx
# tag=2022Aug4_MassGroup0_bJetLoose
# tag=2022Aug30_fullBDT_bJetLoose_CutLowMx280
# tag=2022Sep14_Mx300_bJetLoose_3
# tag=2022Sep14_Mx300_bJetLoose_mx280cut
# tag=2022Sep14_Mx300_bJetLoose_depth4_leafs50_3
# tag=2022Sep14_Mx300_bJetLoose_depth2_leafs50
# tag=2022Oct25_ValRegTrain_bJetLoose
# tag=BDTweights_2022Nov14_bJetScoreLoose_shapes2
# tag2=2022Nov14_bJetScoreLoose_shapes2
# tag=BDTweights_2022Nov14_bJetScoreLoose_shapes_allVars_selectSigs
# tag2=2022Nov14_bJetScoreLoose_shapes_allVars_selectSigs

#tag=BDTweights_2023Feb13_preapprovalVars2
#tag2=2023Feb13_preapprovalVars2

# tag=BDTweights_2023Feb21_genMatched
# tag2=2023Feb21_genMatched
# tag=BDTweights_2023Feb21_visualBinning3
# tag2=2023Feb21_visualBinning3
# tag=BDTweights_2023Feb22_analysisBinning
# tag2=2023Feb22_analysisBinning
# tag=BDTweights_2023Feb22_Mxgt500
# tag2=2023Feb22_Mxgt500
# tag=BDTweights_2023Feb22_Mxlt500_3
# tag2=2023Feb22_Mxlt500_3
tag=BDTweights_${1}
tag2=${1}
folderTag=fullSubmission_2022Nov
for year in "2016preVFP" "2016" "2017" "2018"
# for year in 2016 2017 2018
do
    mv DataPlots_fullSubmission_${year}_${tag} ${year}DataPlots_${tag2}
    # mv fullSubmission_${year}_${tag} ${year}DataPlots_${tag}
    mkdir -p VarPlots/rootHists/${folderTag}
    mv ${year}DataPlots_${tag2} VarPlots/rootHists/${folderTag}/
done
