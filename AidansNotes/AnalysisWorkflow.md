Analysis workflow:

- build (train) the reweighting BDT model
- apply the BDT reweighting model to the nTuples (makes a new branch)
- (*where does it get used ?*) config file (one for each year) with weight branch name:
    - /uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/config/Resonant_NMSSM_bbbb/selectionCfg_2016Resonant_NMSSM_XYH_bbbb_all.cfg
        - config files contain syst. weights and variable binning
- fill the histograms and create outPlotter.root
    - Code: fill_histograms.exe 
    - Config file( one for each year ): config/Resonant_NMSSM_bbbb/plotter_2017Resonant_NMSSM_XYH_bbbb_Full_quicktest_2021Dec8.cfg
    **how do I check if the luminosity is right?**
    *added several points:*
    signals = sig_NMSSM_bbbb_MX_700_MY_300, sig_NMSSM_bbbb_MX_500_MY_200, sig_NMSSM_bbbb_MX_900_MY_400, sig_NMSSM_bbbb_MX_1400_MY_600, sig_NMSSM_bbbb_MX_1800_MY_800, sig_NMSSM_bbbb_MX_300_MY_125, sig_NMSSM_bbbb_MX_300_MY_150, sig_NMSSM_bbbb_MX_600_MY_400, sig_NMSSM_bbbb_MX_700_MY_500, sig_NMSSM_bbbb_MX_800_MY_600, sig_NMSSM_bbbb_MX_600_MY_400, sig_NMSSM_bbbb_MX_900_MY_250, sig_NMSSM_bbbb_MX_1000_MY_300, sig_NMSSM_bbbb_MX_1200_MY_200 
    new outputdir:
    ./2016DataPlots_NMSSM_XYH_bbbb_dataDrivenStudies_aidan_2021Dec15

- unroll the 2d plots
    - code: scripts/UnrollAllSubdirControlTest.sh
    - and scripts/Unroll2DplotsSubRangeControlTest.cc 
        - *do the mass values at line 56 make sense??*
    - run code with: source ./scripts/UnrollAllSubdirControlTest.sh 2016
- modify the plots to look at the bkg model (instead of signal)
    - code: scripts/modifyPlotForControlTest.C+
    - run with: 
        root -l
        .L scripts/modifyPlotForControlTest.C+
        void modifyAllPlotForControlTest(std::string tag = "NMSSM_XYH_bbbb_dataDrivenStudies_aidan")
    - removed the 'up' 'down' behavior for the CR test
    - need to edit the folder name
    - *replacing* 
    data_BTagCSV/selectionbJets_SignalRegion/data_BTagCSV_selectionbJets_SignalRegion_HH_kinFit_m_H2_m_Rebinned_Unrolled
    *with*
   data_BTagCSV/selectionbJets_ControlRegionBlinded/data_BTagCSV_selectionbJets_ControlRegionBlinded_HH_kinFit_m_H2_m_Rebinned_Unrolled 
    *and* 
    data_BTagCSV_dataDriven_kinFit/selectionbJets_SignalRegion/data_BTagCSV_dataDriven_kinFit_selectionbJets_SignalRegion_HH_kinFit_m_H2_m_Rebinned_Unrolled
    *with*
    data_BTagCSV_dataDriven_kinFit/selectionbJets_ControlRegionBlinded/data_BTagCSV_dataDriven_kinFit_selectionbJets_ControlRegionBlinded_HH_kinFit_m_H2_m_Rebinned_Unrolled 
- run the limits with Combine:
    - code: /uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/limits/prepareModels/SubmitFullRunIILimits.py
    - run from limits folder
    - run with: 
    python prepareModels/SubmitFullRunIILimits.py --tag <tag_name> --year RunII --group auto --unblind 
        - replace the <tag_name>
        python prepareModels/SubmitFullRunIILimits.py --tag aidan_2021Dec15 --year RunII --group auto --unblind 
    - config files (one for each year): limits/prepareModels/config/LimitsConfig_2016.cfg
        - *option folder has fravera name...?*
    - list of samples to run: 
        - /uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/limits/prepareModels/listOfSamples.txt
- produce limits plots:
    -code: /uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/limits/produceAllResults.sh


goals - 
*understand the problem:*
- run combine to get the stats
compare the limits between validation and control regions
    - run some points that are bad in the validation limits for CR
compare the limits to new sigma plots 
    - produce sigma plot for validation region, CR
    - 1d for a mX bins(?)
talk to Fabio... how do we know (demonstrate) there is an issue 

train the BDT with a grid search of hyper parameters 
 - use condor submission for this?
 - optimze the classifier bdt as well?


error bars 
lines
limits