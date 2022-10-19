filepath="/uscms/homes/a/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/limits/CondorJobs/"
# study="jobsLimits_2022Aug1_fullBDT_bJetLoose_CutLowMx280/"
# study="jobsLimits_2022Aug30_fullBDT_bJetLoose_CutLowMx280_VR/"
# study="jobsLimits_2022Aug30_fullBDT_bJetLoose_CutLowMx280_rmax20/"
# study="jobsLimits_2022Aug30_fullBDT_bJetLoose_CutLowMx280_rmax20_VR/"
# study="jobsLimits_2022Aug1_fullBDT_bJetLoose_CutLowMx/"
# study="jobsLimits_2022Aug1_fullBDT_bJetLoose_CutLowMx_VR/"
# study="jobsLimits_2022July13_fullBDT_bJetScoreLoose/"
# study="jobsLimits_2022July13_fullBDT_bJetScoreLoose_VR/"
# study="jobsLimits_2022Sep14_Mx300_bJetLoose_3_rmax30/"
# study="jobsLimits_2022Sep14_Mx300_bJetLoose_3_rmax20/"
# study="jobsLimits_2022Sep14_Mx300_bJetLoose_3_rmax5/"
# study="jobsLimits_2022Sep14_Mx300_bJetLoose_3_VR_rmax30/"
# study="jobsLimits_2022Sep14_Mx300_bJetLoose_3_VR_rmax20/"
# study="jobsLimits_2022Sep14_Mx300_bJetLoose_3_VR_rmax5/"

# study="jobsLimits_2022Sep14_Mx300_bJetLoose_3_rmax30_unrollcut/"
# study="jobsLimits_2022Sep14_Mx300_bJetLoose_3_VR_rmax30_unrollcut/"
# study="jobsLimits_2022Sep14_Mx300_bJetLoose_mx280cut_rmax30_unrollcut/"
# study="jobsLimits_2022Sep14_Mx300_bJetLoose_mx280cut_VR_rmax30_unrollcut/"
# study="jobsLimits_2022Sep14_Mx300_bJetLoose_depth2_leafs50_rmax30_unrollcut/"
# study="jobsLimits_2022Sep14_Mx300_bJetLoose_depth2_leafs50_VR_rmax30_unrollcut/"
# study="jobsLimits_2022Sep14_Mx300_bJetLoose_depth4_leafs50_3_rmax30_unrollcut/"
study="jobsLimits_2022Sep14_Mx300_bJetLoose_depth4_leafs50_3_VR_rmax30_unrollcut/"


# filename="limits_MX_300_MY_150_cp.txt"
# myfiles=($(ls ${filepath}${study}*MX_300*.stdout))
myfiles=($(ls ${filepath}${study}*.stdout))
for file in "${myfiles[@]}"; do
    newfilename="${file/sh_*.stdout/txt}"
    newfilename="${newfilename/job_sig_NMSSM_bbbb_/limits_}"
    cp $file $newfilename
    vim -e -s -c "execute 'g/------/1,d' | execute 'g/Done in/d' | execute 'g/done/d' | execute 'g/execution/d' | execute 'g/random/d' | execute 'g/method/d' | execute 'g/Asymptotic/d' | execute 'g/SimNLL/d' | execute 'g/Limits/norm! I,' | execute 'g/datacard/+1d' | execute 'g/finished/d' | execute 'g/exit/d'" -c "execute '%s/: r </,/'" -c "execute '%s/\.\.\. running/,/'" -c "0r! echo %:p" -c "execute '%s/.*CondorJobs\///'"  -c 'wq' ${newfilename}
    vim -c 'call setreg("q","\<C-V>7j$d9k\<C-V>7jI , \<ESC>\<C-V>7jp", "b")' -e -s -c "g/statOnly/norm @q" -c "g/statOnly/norm @q" -c "execute 'g/^$/d' | execute 'g/, $/d'" -c "wq"  ${newfilename}
    echo $newfilename;
done
# vim -e -s -c "execute 'g/------/1,d' | execute 'g/Done in/d' | execute 'g/done/d' | execute 'g/execution/d' | execute 'g/random/d' | execute 'g/method/d' | execute 'g/Asymptotic/d' | execute 'g/SimNLL/d' | execute 'g/Limits/norm! I,' | execute 'g/datacard/+1d' |execute 'g/finished/d' |execute 'g/exit/d'" -c "execute '%s/: r </,/'" -c "execute '%s/\.\.\. running/,/'" -c "0r! echo %:p" -c "execute '%s/.*CondorJobs\///'"  -c 'wq' ${filepath}${study}${filename}
