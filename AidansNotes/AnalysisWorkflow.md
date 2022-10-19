Analysis workflow:

# build (train) the reweighting BDT model
# apply the BDT reweighting model to the nTuples (makes a new branch)
# fill the histograms and create outPlotter.root
## Code: fill_histograms.exe
    - run with `fill_histograms.exe configfile`
    - Config files:
        - ( *called from bottom of plotter_ config file* ) config file (one for each year) with weight branch name:
            - config/Resonant_NMSSM_bbbb/selectionCfg_2016Resonant_NMSSM_XYH_bbbb_all.cfg
                - config files contain syst. weights and variable binning
                *do sig_..._3bScaled weights need to be changed?*
                *same question for kinfit_up and kinfit_down*
        - Config file( one for each year ): `config/Resonant_NMSSM_bbbb/plotter_2017Resonant_NMSSM_XYH_bbbb_Full_quicktest_2021Dec8.cfg`
            - changed selection_ config to "rebinned" versions
        **how do I check if the luminosity is right? - fabio pfullSubmissict lumis in the Full files; but probably a 1% effect**
        *added several points:*
        signals = `sig_NMSSM_bbbb_MX_700_MY_300, sig_NMSSM_bbbb_MX_500_MY_200, sig_NMSSM_bbbb_MX_900_MY_400, sig_NMSSM_bbbb_MX_1400_MY_600, sig_NMSSM_bbbb_MX_1800_MY_800, sig_NMSSM_bbbb_MX_300_MY_125, sig_NMSSM_bbbb_MX_300_MY_150, sig_NMSSM_bbbb_MX_600_MY_400, sig_NMSSM_bbbb_MX_700_MY_500, sig_NMSSM_bbbb_MX_800_MY_600, sig_NMSSM_bbbb_MX_600_MY_400, sig_NMSSM_bbbb_MX_900_MY_250, sig_NMSSM_bbbb_MX_1000_MY_300, sig_NMSSM_bbbb_MX_1200_MY_200` 
        new outputdir:
        `./2016DataPlots_NMSSM_XYH_bbbb_dataDrivenStudies_aidan_2021Dec15`
    - for full test use `scripts/submitAllFillOnTier3_RunII.sh` (change the tag inside), which uses scripts/submitFillOnTier3.py for each year
        - the outputFolder in `plotterconfig` is not used when submitting to condor
        - then you have to merge the outputs:
            mergeHistograms.py and use the same tag as in `submitAllFillOnTier3_RunII`
                - `python ./scripts/mergeHistograms.py --tag fullSubmission_2016_v34_aidan_2021Dec21`
                - `python ./scripts/mergeHistograms.py --tag fullSubmission_2017_v34_aidan_2021Dec21`
                - `python ./scripts/mergeHistograms.py --tag fullSubmission_2018_v34_aidan_2021Dec21`
            For rebinned submission:
                - `python ./scripts/mergeHistograms.py --tag fullSubmission_2016_v34_aidan_rebinnned_2021Dec23`
                - `python ./scripts/mergeHistograms.py --tag fullSubmission_2017_v34_aidan_rebinnned_2021Dec23`
                - `python ./scripts/mergeHistograms.py --tag fullSubmission_2018_v34_aidan_rebinnned_2021Dec23`
        - run the job from dir above scripts

# unroll the 2d plots
    - code: scripts/UnrollAllSubdirControlTest.sh
    - and scripts/Unroll2DplotsSubRangeControlTest.cc 
    - run code with: source ./scripts/UnrollAllSubdirControlTest.sh 2016
# for the up and down variations: use scripts/calculateBGKshape.C (need to use the right tag)
    - takes the up and down histograms and recomputes them so that "up" is always above the average when "down" is below and vice versa.
    - run with:
        root -l './scripts/calculateAllBKGshape.C("v34_aidan_2021Dec21")'
# modify the plots to look at the bkg model (instead of signal)
    - code: scripts/modifyPlotForControlTest.C+
    - now using code: scripts/modifyAllPlotForControlTest.C+
    - run with:
        root -l './scripts/modifyAllPlotForControlTest.C("v34_aidan_2021Dec21")'
    - removed the 'up' 'down' behavior for the CR test
    - need to edit the folder name
    - *replacing* 
    data_BTagCSV/selectionbJets_SignalRegion/data_BTagCSV_selectionbJets_SignalRegion_HH_kinFit_m_H2_m_Rebinned_Unrolled
    *with*
   data_BTagCSV/selectionbJets_ControlRegionBlinded/data_BTagCSV_selectionbJets_ControlRegionBlinded_HH_kinFit_m_H2_m_Rebinned_Unrolled 
    *and also replacing* 
    data_BTagCSV_dataDriven_kinFit/selectionbJets_SignalRegion/data_BTagCSV_dataDriven_kinFit_selectionbJets_SignalRegion_HH_kinFit_m_H2_m_Rebinned_Unrolled
    *with*
    data_BTagCSV_dataDriven_kinFit/selectionbJets_ControlRegionBlinded/data_BTagCSV_dataDriven_kinFit_selectionbJets_ControlRegionBlinded_HH_kinFit_m_H2_m_Rebinned_Unrolled 
# run the limits with Combine:
    - code: nobackup/DiHiggs_v2/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/limits/prepareModels/SubmitFullRunIILimits.py
    - run from limits folder
    - run with: 
    python prepareModels/SubmitFullRunIILimits.py --tag <tag_name> --year RunII --group auto --unblind 
        - replace the <tag_name>
        python prepareModels/SubmitFullRunIILimits.py --tag aidan_2021Dec15 --year RunII --group auto --unblind 
        python prepareModels/SubmitFullRunIILimits.py --tag aidan_all_2021Dec23 --year RunII --group auto --unblind 
    - config files (one for each year): limits/prepareModels/config/LimitsConfig_2016.cfg
        - *option folder has fravera name...? this is the output folder for when you run the script locally (ie without condor)*
    - list of samples to run: 
        - /uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/limits/prepareModels/listOfSamples.txt
# produce limits plots:
    -code: /uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/limits/produceAllResults.sh
    - need to grab use tag from the previous step 


goals - 
*understand the problem:*
- run combine to get the Goodness of Fit stats
- compare the limits between validation and control regions
    + run some points that are bad in the validation limits for CR
    - run all points - for both control and validation region
- compare the limits to new sigma plots 
    + produce sigma plot for validation region, CR
    + 1d for a mX bins(?)
    - produce plots for all points
- run the limits and the sigma plots with different bins

train the BDT with a grid search of hyper parameters 
 - use condor submission for this?
 - optimze the classifier bdt as well?


error bars 
lines
limits

for the plots - want to match the bin for the sigma plot 


plan - run the Validation limits for the orig binning and rebinned outplotters (make sure you don't overwrite the orig binnning...)
 - also run the CR limits with the new binning
