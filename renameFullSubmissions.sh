# tag=2022Jul7_fullBDT_bJetScoreLoose
# tag=2022Jul14_fullBDT_bJetScore1p5
# tag=2022Aug1_fullBDT_bJetLoose_CutLowMx
# tag=2022Aug4_MassGroup0_bJetLoose
# tag=2022Aug30_fullBDT_bJetLoose_CutLowMx280
# tag=2022Sep14_Mx300_bJetLoose_3
# tag=2022Sep14_Mx300_bJetLoose_mx280cut
tag=2022Sep14_Mx300_bJetLoose_depth4_leafs50_3
# tag=2022Sep14_Mx300_bJetLoose_depth2_leafs50
folderTag=fullSubmission_2022July
for year in 2016 2017 2018
do
    mv DataPlots_fullSubmission_${year}_${tag} ${year}DataPlots_${tag}
    # mv fullSubmission_${year}_${tag} ${year}DataPlots_${tag}
    mkdir -p VarPlots/rootHists/${folderTag}
    mv ${year}DataPlots_${tag} VarPlots/rootHists/${folderTag}/
done
