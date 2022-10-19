TAG=2022Aug1_fullBDT_bJetLoose_CutLowMx280
MassPoints="MX_300_MY_150 MX_300_MY_60 MX_600_MY_400"
mkdir -p $TAG
for MassPoint in $MassPoints; do
    eoscp -ns root://cmseos.fnal.gov//store/user/agrummer/bbbb_limits/${TAG}/HistogramFiles_RunII/datacard_RunII_sig_NMSSM_bbbb_${MassPoint}.txt ${TAG}/datacard_RunII_sig_NMSSM_bbbb_MX_${MassPoint}.txt
done
# eoscp root://cmseos.fnal.gov//store/user/agrummer/bbbb_limits/2022Aug1_fullBDT_bJetLoose_CutLowMx280/HistogramFiles_RunII/datacard_RunII_sig_NMSSM_bbbb_MX_300_MY_150.txt .
