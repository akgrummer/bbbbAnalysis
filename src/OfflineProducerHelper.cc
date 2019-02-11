#include "OfflineProducerHelper.h"
#include <iostream>
#include <iomanip>
#include <cmath>
#include <stdlib.h>    

#include "CompositeCandidate.h"
#include "Jet.h"
#include "Electron.h"
#include "Muon.h"
#include "GenPart.h"
#include "HH4b_kinFit.h"
#include <experimental/any>
 
using namespace std::experimental;

using namespace std;

// ----------------- Objects for cut - BEGIN ----------------- //

void OfflineProducerHelper::initializeObjectsForCuts(OutputTree &ot){

    string objectsForCut = any_cast<string>(parameterList_->at("ObjectsForCut"));

    if(objectsForCut == "None")
        save_objects_for_cut = [](NanoAODTree& nat, OutputTree &ot) -> void {return;};
    else if(objectsForCut == "WandZleptonDecays"){
        save_objects_for_cut = &save_WandZleptondecays;
        ot.declareUserFloatBranch("LeadingIsolatedZElectron_pt", -1.);
        ot.declareUserFloatBranch("LeadingIsolatedZMuon_pt", -1.);
        ot.declareUserFloatBranch("LeadingIsolatedWElectron_pt", -1.);
        ot.declareUserFloatBranch("LeadingIsolatedWMuon_pt", -1.);
    }

    return;

}

// reject events with leptons that may come from W and Z decays
void OfflineProducerHelper::save_WandZleptondecays (NanoAODTree& nat, OutputTree &ot){

    std::vector<Electron> electronFromW;
    electronFromW.reserve(*(nat.nElectron));
    std::vector<Electron> electronFromZ;
    electronFromZ.reserve(*(nat.nElectron));
    std::vector<Muon> muonFromW;
    muonFromW.reserve(*(nat.nMuon));
    std::vector<Muon> muonFromZ;
    muonFromZ.reserve(*(nat.nMuon));

    for (uint eIt = 0; eIt < *(nat.nElectron); ++eIt){
        Electron theElectron(eIt, &nat);
        
        if( //theElectron.P4Regressed().Pt()                                 >25.0 && 
            get_property(theElectron,Electron_mvaSpring16GP_WP80) && 
            get_property(theElectron,Electron_pfRelIso03_all    ) < any_cast<float>(parameterList_->at("WElectronMaxPfIso")) )
            electronFromW.emplace_back(theElectron);

        if( //theElectron.P4().Pt()                                 >20.0 && 
            get_property(theElectron,Electron_mvaSpring16GP_WP90) && 
            get_property(theElectron,Electron_pfRelIso03_all    ) < any_cast<float>(parameterList_->at("ZElectronMaxPfIso")) )
            electronFromZ.emplace_back(theElectron);
    }

    if(electronFromZ.size()>0){
        stable_sort(electronFromZ.begin(), electronFromZ.end(), [](const Electron & a, const Electron & b) -> bool
        {
            return ( a.P4().Pt() > b.P4().Pt() );
        }); // sort electrons by pt (highest to lowest)
        
        ot.userFloat("LeadingIsolatedZElectron_pt") = electronFromZ.at(0).P4().Pt();
    }

    if(electronFromW.size()>0){
        stable_sort(electronFromW.begin(), electronFromW.end(), [](const Electron & a, const Electron & b) -> bool
        {
            return ( a.P4().Pt() > b.P4().Pt() );
        }); // sort electrons by pt (highest to lowest)
        
        ot.userFloat("LeadingIsolatedWElectron_pt") = electronFromW.at(0).P4().Pt();
    }

    for (uint eIt = 0; eIt < *(nat.nMuon); ++eIt){
        Muon theMuon(eIt, &nat);

        if( //theMuon.P4().Pt()                                     >25.0 && 
            get_property(theMuon,Muon_tightId                    )      &&
            get_property(theMuon,Muon_pfRelIso04_all             ) < any_cast<float>(parameterList_->at("WMuonMaxPfIso")) &&
            get_property(theMuon,Muon_dxy                        ) < any_cast<float>(parameterList_->at("MuonMaxDxy")) &&
            get_property(theMuon,Muon_dz                         ) < any_cast<float>(parameterList_->at("MuonMaxDz")) )
            muonFromW.emplace_back(theMuon);

        if( //theMuon.P4().Pt()                                     >20.0 && 
            get_property(theMuon,Muon_pfRelIso04_all             ) < any_cast<float>(parameterList_->at("ZMuonMaxPfIso")) &&
            get_property(theMuon,Muon_dxy                        ) < any_cast<float>(parameterList_->at("MuonMaxDxy")) &&
            get_property(theMuon,Muon_dz                         ) < any_cast<float>(parameterList_->at("MuonMaxDz")) )
            muonFromZ.emplace_back(theMuon);
    }

    if(muonFromZ.size()>0){
        stable_sort(muonFromZ.begin(), muonFromZ.end(), [](const Muon & a, const Muon & b) -> bool
        {
            return ( a.P4().Pt() > b.P4().Pt() );
        }); // sort muons by pt (highest to lowest)
        
        ot.userFloat("LeadingIsolatedZMuon_pt") = muonFromZ.at(0).P4().Pt();
    }

    if(muonFromW.size()>0){
        stable_sort(muonFromW.begin(), muonFromW.end(), [](const Muon & a, const Muon & b) -> bool
        {
            return ( a.P4().Pt() > b.P4().Pt() );
        }); // sort muons by pt (highest to lowest)
        
        ot.userFloat("LeadingIsolatedWMuon_pt") = muonFromW.at(0).P4().Pt();
    }

}

// ----------------- Objects for cut - END ----------------- //



// ----------------- Compute scaleFactors - BEGIN ----------------- //

void OfflineProducerHelper::initializeObjectsForScaleFactors(OutputTree &ot){

    string scaleFactorsMethod = any_cast<string>(parameterList_->at("ScaleFactorMethod"));

    if(scaleFactorsMethod == "None"){
        //do nothing
    }
    else if(scaleFactorsMethod == "FourBtag_ScaleFactor"){
        ot.declareUserFloatBranch("bTagScaleFactor_central"          , 1.);
        ot.declareUserFloatBranch("bTagScaleFactor_bJets_up"         , 1.);
        ot.declareUserFloatBranch("bTagScaleFactor_bJets_down"       , 1.);
        ot.declareUserFloatBranch("bTagScaleFactor_cJets_up"         , 1.);
        ot.declareUserFloatBranch("bTagScaleFactor_cJets_down"       , 1.);
        ot.declareUserFloatBranch("bTagScaleFactor_lightJets_up"     , 1.);
        ot.declareUserFloatBranch("bTagScaleFactor_lightJets_down"   , 1.);

        BTagCalibration btagCalibration("DeepCSV",any_cast<string>(parameterList_->at("BJetScaleFactorsFile")));    
        btagCalibrationReader_lightJets_ = new BTagCalibrationReader(BTagEntry::OP_MEDIUM,"central",{"up", "down"});      
        btagCalibrationReader_cJets_     = new BTagCalibrationReader(BTagEntry::OP_MEDIUM,"central",{"up", "down"});      
        btagCalibrationReader_bJets_     = new BTagCalibrationReader(BTagEntry::OP_MEDIUM,"central",{"up", "down"}); 

        btagCalibrationReader_lightJets_->load(btagCalibration, BTagEntry::FLAV_UDSG, "incl"  );
        btagCalibrationReader_cJets_    ->load(btagCalibration, BTagEntry::FLAV_C   , "mujets");
        btagCalibrationReader_bJets_    ->load(btagCalibration, BTagEntry::FLAV_B   , "mujets");
    }

    return;

}

void OfflineProducerHelper::compute_scaleFactors_fourBtag_eventScaleFactor (const std::vector<Jet> &jets, NanoAODTree& nat, OutputTree &ot){
    
    float tmpScaleFactor_bJets_central     = 1.;
    float tmpScaleFactor_bJets_up          = 1.;
    float tmpScaleFactor_bJets_down        = 1.;
    float tmpScaleFactor_cJets_central     = 1.;
    float tmpScaleFactor_cJets_up          = 1.;
    float tmpScaleFactor_cJets_down        = 1.;
    float tmpScaleFactor_lightJets_central = 1.;
    float tmpScaleFactor_lightJets_up      = 1.;
    float tmpScaleFactor_lightJets_down    = 1.;

    for(const auto &iJet : jets){
        int jetFlavour = abs(get_property(iJet,Jet_partonFlavour));
        if(jetFlavour==5){
            tmpScaleFactor_bJets_central     *= btagCalibrationReader_bJets_    ->eval_auto_bounds("central", BTagEntry::FLAV_B   , iJet.P4().Eta(), iJet.P4().Pt());
            tmpScaleFactor_bJets_up          *= btagCalibrationReader_bJets_    ->eval_auto_bounds("up"     , BTagEntry::FLAV_B   , iJet.P4().Eta(), iJet.P4().Pt());
            tmpScaleFactor_bJets_down        *= btagCalibrationReader_bJets_    ->eval_auto_bounds("down"   , BTagEntry::FLAV_B   , iJet.P4().Eta(), iJet.P4().Pt());
        }
        else if(jetFlavour==4){
            tmpScaleFactor_cJets_central     *= btagCalibrationReader_cJets_    ->eval_auto_bounds("central", BTagEntry::FLAV_C   , iJet.P4().Eta(), iJet.P4().Pt());
            tmpScaleFactor_cJets_up          *= btagCalibrationReader_cJets_    ->eval_auto_bounds("up"     , BTagEntry::FLAV_C   , iJet.P4().Eta(), iJet.P4().Pt());
            tmpScaleFactor_cJets_down        *= btagCalibrationReader_cJets_    ->eval_auto_bounds("down"   , BTagEntry::FLAV_C   , iJet.P4().Eta(), iJet.P4().Pt());
        }
        else{
            tmpScaleFactor_lightJets_central *= btagCalibrationReader_lightJets_->eval_auto_bounds("central", BTagEntry::FLAV_UDSG, iJet.P4().Eta(), iJet.P4().Pt());
            tmpScaleFactor_lightJets_up      *= btagCalibrationReader_lightJets_->eval_auto_bounds("up"     , BTagEntry::FLAV_UDSG, iJet.P4().Eta(), iJet.P4().Pt());
            tmpScaleFactor_lightJets_down    *= btagCalibrationReader_lightJets_->eval_auto_bounds("down"   , BTagEntry::FLAV_UDSG, iJet.P4().Eta(), iJet.P4().Pt());
        }   
    }

    ot.userFloat("bTagScaleFactor_central"          ) = tmpScaleFactor_bJets_central * tmpScaleFactor_cJets_central * tmpScaleFactor_lightJets_central ;
    ot.userFloat("bTagScaleFactor_bJets_up"         ) = tmpScaleFactor_bJets_up      * tmpScaleFactor_cJets_central * tmpScaleFactor_lightJets_central ;
    ot.userFloat("bTagScaleFactor_bJets_down"       ) = tmpScaleFactor_bJets_down    * tmpScaleFactor_cJets_central * tmpScaleFactor_lightJets_central ;
    ot.userFloat("bTagScaleFactor_cJets_up"         ) = tmpScaleFactor_bJets_central * tmpScaleFactor_cJets_up      * tmpScaleFactor_lightJets_central ;
    ot.userFloat("bTagScaleFactor_cJets_down"       ) = tmpScaleFactor_bJets_central * tmpScaleFactor_cJets_down    * tmpScaleFactor_lightJets_central ;
    ot.userFloat("bTagScaleFactor_lightJets_up"     ) = tmpScaleFactor_bJets_central * tmpScaleFactor_cJets_central * tmpScaleFactor_lightJets_up      ;
    ot.userFloat("bTagScaleFactor_lightJets_down"   ) = tmpScaleFactor_bJets_central * tmpScaleFactor_cJets_central * tmpScaleFactor_lightJets_down    ;

    return;
}

// ----------------- Compute scaleFactors - END ----------------- //


// ----------------- Compute weights - BEGIN ----------------- //

void OfflineProducerHelper::initializeObjectsForEventWeight(OutputTree &ot, SkimEffCounter &ec, std::string PUWeightFileName)
{

    string weightsMethod = any_cast<string>(parameterList_->at("WeightMethod"));

    if(weightsMethod == "None")
    {
        calculateEventWeight = [](NanoAODTree& nat, OutputTree &ot, SkimEffCounter &ec) -> float {return 1.;};
    }
    else if(weightsMethod == "StandardWeight")
    {
        calculateEventWeight = &calculateEventWeight_AllWeights;
        std::string branchName;

        int weightBin = ec.binMap_.size();

        // PUWeight need to store histograms from pu files
        branchName = "PUWeight";
        ot.declareUserFloatBranch(branchName, 1.);
        weightMap_[branchName] = std::pair< float, std::map<std::string, float> >();
        weightMap_[branchName].first = 1.;
        std::vector<std::string> puWeightVariation = {"_up","_down"};
        TFile *PUWeightFile = TFile::Open(PUWeightFileName.data());
        std::map<std::string, TH1D*> PUWeightHistogramMap;
        if(PUWeightFile == NULL){
            cerr << "**  Pileup weight file " << PUWeightFileName << " not found, aborting" << endl;
            abort();
        }
        PUWeightHistogramMap[branchName] = (TH1D*) PUWeightFile->Get("PUweights");
        // PUWeightHistogramMap[branchName]->SetDirectory(0);

        for(unsigned int var = 0; var<puWeightVariation.size(); ++var)
        {
            std::string variationBranch = branchName + puWeightVariation[var];
            ot.declareUserFloatBranch(variationBranch, 1.);
            weightMap_[branchName].second[variationBranch] = 1.;           
            ec.binMap_[variationBranch] = ++weightBin;
            ec.binEntries_[variationBranch] = 1.;
            PUWeightHistogramMap[variationBranch] = (TH1D*) PUWeightFile->Get(("PUweights"+puWeightVariation[var]).data());
            // PUWeightHistogramMap[variationBranch]->SetDirectory(0);
        }

        for(const auto & histogram : PUWeightHistogramMap)
        {
            for(int iBin=1; iBin<=histogram.second->GetNbinsX(); ++iBin)
            {
                PUWeightMap_[histogram.first][std::pair<float,float>(histogram.second->GetBinLowEdge(iBin),histogram.second->GetBinLowEdge(iBin+1))] = histogram.second->GetBinContent(iBin);
            }
        }

        PUWeightFile->Close();

        //genWeight (no weight variations)
        branchName = "genWeight";
        ot.declareUserFloatBranch(branchName, 1.);
        weightMap_[branchName] = std::pair< float, std::map<std::string, float> >();
        weightMap_[branchName].first = 1.;

        // LHEPdfWeight
        branchName = "LHEPdfWeight";
        ot.declareUserFloatBranch(branchName, 1.);
        weightMap_[branchName] = std::pair< float, std::map<std::string, float> >();
        weightMap_[branchName].first = 1.;
        // LHEPdfWeight weight variations
        for(unsigned int var = 0; var<=100; ++var)
        {
            std::string variationBranch = branchName + "_var" + std::to_string(var);
            ot.declareUserFloatBranch(variationBranch, 1.);
            weightMap_[branchName].second[variationBranch] = 1.;           
            ec.binMap_[variationBranch] = ++weightBin;
            ec.binEntries_[variationBranch] = 1.;
        }

        // LHEScaleWeight
        branchName = "LHEScaleWeight";
        ot.declareUserFloatBranch(branchName, 1.);
        weightMap_[branchName] = std::pair< float, std::map<std::string, float> >();
        weightMap_[branchName].first = 1.;
        // LHEScaleWeight weight variations
        for(unsigned int var = 0; var<9; ++var)
        {
            if(var == 4) continue; //Yep... the nominal seems to be in the middle...
            std::string variationBranch = branchName + "_var" + std::to_string(var);
            ot.declareUserFloatBranch(variationBranch, 1.);
            weightMap_[branchName].second[variationBranch] = 1.;           
            ec.binMap_[variationBranch] = ++weightBin;
            ec.binEntries_[variationBranch] = 1.;
        }

        //PSWeight are empty, skypping
        // branchName = "PSWeight";
        // ot.declareUserFloatBranch(branchName, 1.);
        // weightMap_[branchName] = std::pair< float, std::map<std::string, float> >();
        // weightMap_[branchName].first = 1.;
        // // PSWeight weight variations
        // for(unsigned int var = 0; var<4; ++var)
        // {
        //     std::string variationBranch = branchName + "_var" + std::to_string(var);
        //     ot.declareUserFloatBranch(variationBranch, 1.);
        //     weightMap_[branchName].second[variationBranch] = 1.;           
        //     ec.binMap_[variationBranch] = weightBin++;
        //     ec.binEntries_[variationBranch] = 1.;
        // }
    }

    return;

}

float OfflineProducerHelper::calculateEventWeight_AllWeights(NanoAODTree& nat, OutputTree &ot, SkimEffCounter &ec)
{

    for(auto & weight : weightMap_)
    {
        weight.second.first = 1.;
        for(auto & correction : weight.second.second)
        {
            correction.second = 1.;
        }
    }

    float eventWeight = 1.;
    float tmpWeight = 1.;
    std::string branchName;

    // PUWeight need get pu from histograms
    branchName = "PUWeight";
    float eventPU = *(nat.Pileup_nTrueInt);
    for(const auto & weightBin : PUWeightMap_[branchName])
    {
        if(eventPU >= weightBin.first.first && eventPU < weightBin.first.second)
        {
            tmpWeight = weightBin.second;
            break;
        }
    }
    tmpWeight = tmpWeight==0 ? 1 : tmpWeight; //set to 1 if weight is 0
    ot.userFloat(branchName) = tmpWeight;
    weightMap_[branchName].first = tmpWeight;
    eventWeight *= tmpWeight;
    std::vector<std::string> puWeightVariation = {"_up","_down"};
    for(unsigned int var = 0; var<puWeightVariation.size(); ++var)
    {
        std::string variationBranch = branchName + puWeightVariation[var];
        for(const auto & weightBin : PUWeightMap_[variationBranch])
        {
            if(eventPU >= weightBin.first.first && eventPU < weightBin.first.second)
            {
                tmpWeight = weightBin.second;
                break;
            }
        }
        tmpWeight = tmpWeight==0 ? 1 : tmpWeight; //set to 1 if weight is 0
        ot.userFloat(variationBranch) = tmpWeight;
        weightMap_[branchName].second[variationBranch] = tmpWeight;           
    }

    //genWeight (no weight variations)
    branchName = "genWeight";
    tmpWeight = *(nat.genWeight);
    tmpWeight = tmpWeight==0 ? 1 : tmpWeight; //set to 1 if weight is 0
    ot.userFloat(branchName) = tmpWeight;
    weightMap_[branchName].first = tmpWeight;
    eventWeight *= tmpWeight;

    // LHEPdfWeight
    branchName = "LHEPdfWeight";
    tmpWeight = 1.;
    tmpWeight = tmpWeight==0 ? 1 : tmpWeight; //set to 1 if weight is 0
    ot.userFloat(branchName) = tmpWeight;
    weightMap_[branchName].first = tmpWeight;
    eventWeight *= tmpWeight;
    // LHEPdfWeight weight variations
    for(unsigned int var = 0; var<=100; ++var)
    {
        tmpWeight = nat.LHEPdfWeight.At(var);
        tmpWeight = tmpWeight==0 ? 1 : tmpWeight; //set to 1 if weight is 0
        std::string variationBranch = branchName + "_var" + std::to_string(var);
        ot.userFloat(variationBranch) = tmpWeight;
        weightMap_[branchName].second[variationBranch] = tmpWeight;           
    }

    // LHEScaleWeight
    branchName = "LHEScaleWeight";
    tmpWeight = nat.LHEScaleWeight.At(4);
    tmpWeight = tmpWeight==0 ? 1 : tmpWeight; //set to 1 if weight is 0
    ot.userFloat(branchName) = tmpWeight;
    weightMap_[branchName].first = tmpWeight;
    eventWeight *= tmpWeight;
    // LHEScaleWeight weight variations
    for(unsigned int var = 0; var<9; ++var)
        {
        if(var == 4) continue; //Yep... the nominal seems to be in the middle...
        tmpWeight = nat.LHEScaleWeight.At(var);
        tmpWeight = tmpWeight==0 ? 1 : tmpWeight; //set to 1 if weight is 0
        std::string variationBranch = branchName + "_var" + std::to_string(var);
        ot.userFloat(variationBranch) = tmpWeight;
        weightMap_[branchName].second[variationBranch] = tmpWeight;           
    }
    
    // PSWeight are empty, skypping
    // branchName = "PSWeight";
    // tmpWeight = nat.PSWeight.At(0);
    // tmpWeight = tmpWeight==0 ? 1 : tmpWeight; //set to 1 if weight is 0
    // ot.userFloat(branchName) = tmpWeight;
    // weightMap_[branchName].first = tmpWeight;
    // eventWeight *= tmpWeight;
    // // PSWeight weight variations
    // for(unsigned int var = 0; var<4; ++var)
    // {
    //     tmpWeight = nat.PSWeight.At(var);
    //     tmpWeight = tmpWeight==0 ? 1 : tmpWeight; //set to 1 if weight is 0
    //     std::string variationBranch = branchName + "_var" + std::to_string(var);
    //     ot.userFloat(variationBranch) = tmpWeight;
    //     weightMap_[branchName].second[variationBranch] = tmpWeight;           
    // }

    //calculate bins for weights variations

    for(auto & weight : weightMap_)
    {
        for(auto & correction : weight.second.second)
        {
            ec.binEntries_[correction.first] += (eventWeight/weight.second.first*correction.second);
        }
    }

    return eventWeight;

}

// ----------------- Compute weights - END ----------------- //

bool OfflineProducerHelper::select_bbbb_jets(NanoAODTree& nat, EventInfo& ei, OutputTree &ot)
{
    if (*(nat.nJet) < 4)
        return false;

    std::vector<Jet> jets;
    jets.reserve(*(nat.nJet));

    for (uint ij = 0; ij < *(nat.nJet); ++ij){
        jets.emplace_back(Jet(ij, &nat));
    }
    
    //if some montecarlo weight are applied via a reshaping of the jets variables, they must be applied here

    //Apply preselection cuts
    const string preselectionCutStrategy = any_cast<string>(parameterList_->at("PreselectionCut"));
    
    if(preselectionCutStrategy=="bJetCut"){
        bJets_PreselectionCut(jets);
    }
    else if(preselectionCutStrategy=="None"){
        //do nothing
    }
    else throw std::runtime_error("cannot recognize cut strategy --" + preselectionCutStrategy + "--");

    //at least 4 jets required
    if(jets.size()<4) return false;

    // calculate scaleFactors after preselection cuts
    if(parameterList_->find("ScaleFactorMethod") != parameterList_->end()){ //is it a MC event
        const string scaleFactorsMethod = any_cast<string>(parameterList_->at("ScaleFactorMethod"));

        if(scaleFactorsMethod == "FourBtag_ScaleFactor"){
            compute_scaleFactors_fourBtag_eventScaleFactor(jets,nat,ot);
        }
    }


    // sort by deepCSV (highest to lowest)
    stable_sort(jets.begin(), jets.end(), [](const Jet & a, const Jet & b) -> bool
    {
        return ( get_property(a, Jet_btagDeepB) > get_property(b, Jet_btagDeepB) );
    });

    // now need to pair the jets
    std::vector<Jet> presel_jets = {{
        *(jets.rbegin()+0),
        *(jets.rbegin()+1),
        *(jets.rbegin()+2),
        *(jets.rbegin()+3)
    }};

    std::vector<Jet> ordered_jets;
    string strategy = any_cast<string>(parameterList_->at("bbbbChoice"));

    //Select the fouf b jets 
    if(strategy == "OneClosestToMh")
        ordered_jets = bbbb_jets_idxs_OneClosestToMh(&presel_jets);
    else if(strategy == "BothClosestToMh")
        ordered_jets = bbbb_jets_idxs_BothClosestToMh(&presel_jets);
    else if(strategy == "MostBackToBack")
        ordered_jets = bbbb_jets_idxs_MostBackToBack(&presel_jets);
    else if(strategy == "HighestCSVandClosestToMh"){
        ordered_jets = bbbb_jets_idxs_HighestCSVandClosestToMh(&jets);
    }
    else throw std::runtime_error("cannot recognize bbbb choice strategy " + strategy);

    if(ordered_jets.size()!=4) return false;

    // order H1, H2 by pT: pT(H1) > pT (H2)
    CompositeCandidate H1 = CompositeCandidate(ordered_jets.at(0), ordered_jets.at(1));
    H1.rebuildP4UsingRegressedPt(true,true);
    
    CompositeCandidate H2 = CompositeCandidate(ordered_jets.at(2), ordered_jets.at(3));
    H2.rebuildP4UsingRegressedPt(true,true);
    
    //Do a random swap to be sure that the m1 and m2 are simmetric
    bool swapped = (int(H1.P4().Pt()*100.) % 2 == 1);
 
    if (!swapped)
    {
        ei.H1 = H1;
        ei.H2 = H2;
        ei.H1_b1 = ordered_jets.at(0);
        ei.H1_b2 = ordered_jets.at(1);
        ei.H2_b1 = ordered_jets.at(2);
        ei.H2_b2 = ordered_jets.at(3);
    }
    else
    {
        ei.H1 = H2;
        ei.H2 = H1;
        ei.H1_b1 = ordered_jets.at(2);
        ei.H1_b2 = ordered_jets.at(3);
        ei.H2_b1 = ordered_jets.at(0);
        ei.H2_b2 = ordered_jets.at(1);
    }

    ei.H1_bb_DeltaR = sqrt(pow(ei.H1_b1->P4Regressed().Eta() - ei.H1_b2->P4Regressed().Eta(),2) + pow(ei.H1_b1->P4Regressed().Phi() - ei.H1_b2->P4Regressed().Phi(),2));
    ei.H2_bb_DeltaR = sqrt(pow(ei.H2_b1->P4Regressed().Eta() - ei.H2_b2->P4Regressed().Eta(),2) + pow(ei.H2_b1->P4Regressed().Phi() - ei.H2_b2->P4Regressed().Phi(),2));

    
    ei.HH = CompositeCandidate(ei.H1.get(), ei.H2.get());
 
    float targetHiggsMass;
    if(strategy == "HighestCSVandClosestToMh")
    {
        targetHiggsMass = any_cast<float>(parameterList_->at("HiggsMassLMR"));
        if(any_cast<float>(parameterList_->at("LMRToMMRTransition"))>=0. && ei.HH->P4().M() > any_cast<float>(parameterList_->at("LMRToMMRTransition"))) targetHiggsMass = any_cast<float>(parameterList_->at("HiggsMassMMR"));
                   
    }
    else
    {
        targetHiggsMass = any_cast<float>(parameterList_->at("HiggsMass"));
    }

    ei.HH_2DdeltaM = pow(ei.H1->P4().M() - targetHiggsMass,2) + pow(ei.H2->P4().M() - targetHiggsMass,2);
    

    ei.Run = *(nat.run);
    ei.LumiSec = *(nat.luminosityBlock);
    ei.Event = *(nat.event);

    bool applyKineamticFit=true;
    if(applyKineamticFit)
    {
        HH4b_kinFit::constrainHH_signalMeasurement(&ordered_jets.at(0).p4Regressed_, &ordered_jets.at(1).p4Regressed_, &ordered_jets.at(2).p4Regressed_, &ordered_jets.at(3).p4Regressed_);
        CompositeCandidate H1kf = CompositeCandidate(ordered_jets.at(0), ordered_jets.at(1));
        H1kf.rebuildP4UsingRegressedPt(true,true);
        
        CompositeCandidate H2kf = CompositeCandidate(ordered_jets.at(2), ordered_jets.at(3));
        H2kf.rebuildP4UsingRegressedPt(true,true);

        ei.HH_m_kinFit = CompositeCandidate(H1kf, H2kf).P4().M();
    }

    return true;
}


//functions fo apply preselection cuts:
void OfflineProducerHelper::bJets_PreselectionCut(std::vector<Jet> &jets)
{

    float minimumDeepCSVaccepted            = any_cast<float>(parameterList_->at("MinDeepCSV"          ));
    float maximumPtAccepted                 = any_cast<float>(parameterList_->at("MinPt"               ));
    float maximumAbsEtaCSVaccepted          = any_cast<float>(parameterList_->at("MaxAbsEta"           ));

    auto it = jets.begin();
    while (it != jets.end()){
        if(minimumDeepCSVaccepted>=0.){
            if(get_property((*it),Jet_btagDeepB)<minimumDeepCSVaccepted){
                it=jets.erase(it);
                continue;
            }
        }
        if(maximumPtAccepted>0.){
            if(it->P4().Pt()<maximumPtAccepted){
                it=jets.erase(it);
                continue;                
            }
        }
        if(maximumAbsEtaCSVaccepted>0.){
            if(abs(it->P4().Eta())>maximumAbsEtaCSVaccepted){
                it=jets.erase(it);
                continue;                
            }
        }
        ++it;
    }

    return;

}


// one pair is closest to the Higgs mass, the other follows
std::vector<Jet> OfflineProducerHelper::bbbb_jets_idxs_OneClosestToMh(const std::vector<Jet> *presel_jets)
{
    float targetHiggsMass = any_cast<float>(parameterList_->at("HiggsMass"));
    std::vector<pair <float, pair<int,int>>> mHs_and_jetIdx; // each entry is the mH and the two idxs of the pair
    
    for (uint i = 0; i < presel_jets->size(); ++i)
        for (uint j = i+1; j < presel_jets->size(); ++j)
        {
            TLorentzVector p4sum = (presel_jets->at(i).P4Regressed() + presel_jets->at(j).P4Regressed());
            float dmh = fabs(p4sum.Mag() - targetHiggsMass);
            mHs_and_jetIdx.emplace_back(make_pair(dmh, make_pair(i,j)));
        }

    // sort to get the pair closest to mH
    stable_sort (mHs_and_jetIdx.begin(), mHs_and_jetIdx.end());

    std::vector<Jet> outputJets = *presel_jets;
    int ij0 = mHs_and_jetIdx.begin()->second.first;
    int ij1 = mHs_and_jetIdx.begin()->second.second;

    // get the other two jets. The following creates a vector with idxs 0/1/2/3, and then removes ij1 and ij2
    std::vector<int> vres;
    for (uint i = 0; i < presel_jets->size(); ++i) vres.emplace_back(i);
    vres.erase(std::remove(vres.begin(), vres.end(), ij0), vres.end());
    vres.erase(std::remove(vres.begin(), vres.end(), ij1), vres.end());
    
    int ij2 = vres.at(0);
    int ij3 = vres.at(1);

    outputJets.at(0) = presel_jets->at(ij0);
    outputJets.at(1) = presel_jets->at(ij1);
    outputJets.at(2) = presel_jets->at(ij2);
    outputJets.at(3) = presel_jets->at(ij3);

    return outputJets;
}

// minimize the distance from (targetHiggsMass, targetHiggsMass) in the 2D plane
std::vector<Jet> OfflineProducerHelper::bbbb_jets_idxs_BothClosestToMh(const std::vector<Jet> *presel_jets)
{

    float targetHiggsMass = any_cast<float>(parameterList_->at("HiggsMass"));
    std::vector<float> mHs;
    
    for (uint i = 0; i < presel_jets->size(); ++i)
        for (uint j = i+1; j < presel_jets->size(); ++j)
        {
            TLorentzVector p4sum = (presel_jets->at(i).P4Regressed() + presel_jets->at(j).P4Regressed());
            mHs.emplace_back(p4sum.Mag());
        }

    std::pair<float, float> m_12_34 = make_pair (mHs.at(0), mHs.at(5));
    std::pair<float, float> m_13_24 = make_pair (mHs.at(1), mHs.at(4));
    std::pair<float, float> m_14_23 = make_pair (mHs.at(2), mHs.at(3));

    float r12_34 = sqrt (pow(m_12_34.first - targetHiggsMass, 2) + pow(m_12_34.second - targetHiggsMass, 2) );
    float r13_24 = sqrt (pow(m_13_24.first - targetHiggsMass, 2) + pow(m_13_24.second - targetHiggsMass, 2) );
    float r14_23 = sqrt (pow(m_14_23.first - targetHiggsMass, 2) + pow(m_14_23.second - targetHiggsMass, 2) );

    float the_min = std::min({r12_34, r13_24, r14_23});

    std::vector<Jet> outputJets = *presel_jets;

    if (the_min == r12_34){
        outputJets.at(0) = presel_jets->at(1 - 1);
        outputJets.at(1) = presel_jets->at(2 - 1);
        outputJets.at(2) = presel_jets->at(3 - 1);
        outputJets.at(3) = presel_jets->at(4 - 1);
    }

    else if (the_min == r13_24){
        outputJets.at(0) = presel_jets->at(1 - 1);
        outputJets.at(1) = presel_jets->at(3 - 1);
        outputJets.at(2) = presel_jets->at(2 - 1);
        outputJets.at(3) = presel_jets->at(4 - 1);
    }

    else if (the_min == r14_23){
        outputJets.at(0) = presel_jets->at(1 - 1);
        outputJets.at(1) = presel_jets->at(4 - 1);
        outputJets.at(2) = presel_jets->at(2 - 1);
        outputJets.at(3) = presel_jets->at(3 - 1);   
    }

    else
        cout << "** [WARNING] : bbbb_jets_idxs_BothClosestToMh : something went wrong with finding the smallest radius" << endl;

    return outputJets;
}

// make the pairs that maximize their dR separation
std::vector<Jet> OfflineProducerHelper::bbbb_jets_idxs_MostBackToBack(const std::vector<Jet> *presel_jets)
{
    std::pair<CompositeCandidate,CompositeCandidate> H1H2 = get_two_best_jet_pairs (
        *presel_jets,
        std::function<float (std::pair<CompositeCandidate,CompositeCandidate>)> ([](pair<CompositeCandidate,CompositeCandidate> x)-> float {return x.first.P4().DeltaR(x.second.P4());}),
        false);

    std::vector<Jet> output_jets;
    output_jets.at(0) = static_cast<Jet&> (H1H2.first.getComponent1());
    output_jets.at(1) = static_cast<Jet&> (H1H2.first.getComponent2());
    output_jets.at(2) = static_cast<Jet&> (H1H2.second.getComponent1());
    output_jets.at(3) = static_cast<Jet&> (H1H2.second.getComponent2());

    return output_jets;
}


std::vector<Jet> OfflineProducerHelper::bbbb_jets_idxs_HighestCSVandClosestToMh(const std::vector<Jet> *jets){
    
    float targetHiggsMassLMR                = any_cast<float>(parameterList_->at("HiggsMassLMR"        ));
    float targetHiggsMassMMR                = any_cast<float>(parameterList_->at("HiggsMassMMR"        ));
    float LMRToMMRTransition                = any_cast<float>(parameterList_->at("LMRToMMRTransition" ));
 
    std::vector<Jet> output_jets;
    unsigned int numberOfJets = jets->size();
    if(numberOfJets  < 4) return output_jets;

    std::map< const std::array<unsigned int,4>, float> candidateMap;
    for(unsigned int h1b1it = 0; h1b1it< numberOfJets-1; ++h1b1it){
        for(unsigned int h1b2it = h1b1it+1; h1b2it< numberOfJets; ++h1b2it){
            for(unsigned int h2b1it = h1b1it+1; h2b1it< numberOfJets-1; ++h2b1it){
                if(h2b1it == h1b2it) continue;
                for(unsigned int h2b2it = h2b1it+1; h2b2it< numberOfJets; ++h2b2it){
                    if(h2b2it == h1b2it) continue;
                    float candidateMass = (jets->at(h1b1it).P4Regressed() + jets->at(h1b2it).P4Regressed() + jets->at(h2b1it).P4Regressed() + jets->at(h2b2it).P4Regressed()).M();
                    float targetHiggsMass = targetHiggsMassLMR;
                    if(LMRToMMRTransition>=0. && candidateMass > LMRToMMRTransition) targetHiggsMass = targetHiggsMassMMR; //use different range for mass
                    float squareDeltaMassH1 = pow((jets->at(h1b1it).P4Regressed() + jets->at(h1b2it).P4Regressed()).M()-targetHiggsMass,2);
                    float squareDeltaMassH2 = pow((jets->at(h2b1it).P4Regressed() + jets->at(h2b2it).P4Regressed()).M()-targetHiggsMass,2);
                    candidateMap.emplace((std::array<unsigned int,4>){h1b1it,h1b2it,h2b1it,h2b2it},squareDeltaMassH1+squareDeltaMassH2);
                }
            }
        }
    }

    if(candidateMap.size()==0) return output_jets;

    const std::pair< const std::array<unsigned int,4>, float> *itCandidateMap=NULL;
    //find candidate with both Higgs candidates cloasest to the true Higgs mass
    for(const auto & candidate : candidateMap){
        if(itCandidateMap==NULL) itCandidateMap = &candidate;
        else if(itCandidateMap->second > candidate.second) itCandidateMap = &candidate;
    }

    for(const auto & jetPosition : itCandidateMap->first){
        output_jets.emplace_back(jets->at(jetPosition));
    }

    return output_jets;
}

////////////-----FUNCTIONS FOR PRESELECTION OF EVENTS FOR NON-RESONANT ANALYSIS - START
bool OfflineProducerHelper::select_bbbbjj_jets(NanoAODTree& nat, EventInfo& ei, OutputTree &ot)
{
    //Event variables
    ei.Run = *(nat.run);
    ei.LumiSec = *(nat.luminosityBlock);
    ei.Event = *(nat.event);
    //Get the jets in the event and fill the jet multiplicity
    std::vector<Jet> jets; int njpt25=0,njpt30=0,njpt35=0,njpt40=0;
    std::vector<std::tuple<Jet,int,int>> jetsinfo;
    jets.reserve(*(nat.nJet));
    for (uint ij = 0; ij < *(nat.nJet); ++ij){
        if(get_property(Jet(ij, &nat), Jet_pt) > 25) njpt25++;
        if(get_property(Jet(ij, &nat), Jet_pt) > 30) njpt30++;
        if(get_property(Jet(ij, &nat), Jet_pt) > 35) njpt35++;
        if(get_property(Jet(ij, &nat), Jet_pt) > 40) njpt40++;
        jets.emplace_back(Jet(ij, &nat));
        jetsinfo.emplace_back(make_tuple(Jet(ij, &nat),-1,-1));
    }
    ot.userInt("nJetPT25") = njpt25; ot.userInt("nJetPT30") = njpt30;
    ot.userInt("nJetPT35") = njpt35; ot.userInt("nJetPT40") = njpt40;
    //Add gen-level matching information to the jets, and make a tuple = (Jet, MatchingFlag, QuarkId )
    bool is_VBF_sig = any_cast<bool>(parameterList_->at("is_VBF_sig"));
    if( is_VBF_sig )
    {
        jetsinfo = AddGenMatchingInfo(nat,ei,jets);
    }
    else
    {
    //Do Nothing 
    }
    //----------------------------EVENT SELECTION ALGORITHM STUDY HERE------------------------------------------------
    //---Preselect four 'b-jets' (pt, eta, btagging) & 'two vbfjets'(pt,eta,deltaEta) 
    //---prejets is a vector of tuples (tuple = [Jet, MatchingFlag, QuarkID] )
    std::vector<std::tuple<Jet,int,int>> prejetsinfo = bjJets_PreselectionCut(jetsinfo);
    if(prejetsinfo.size()<4) return false;
    //Organize data of preselected jets
    std::vector<std::tuple<Jet,int,int>> prebjetsinfo, prejjetsinfo;
    uint m=0; while(m<4){prebjetsinfo.push_back(make_tuple(get<0>(prejetsinfo[m]),get<1>(prejetsinfo[m]),get<2>(prejetsinfo[m])) ); m++;} 
    stable_sort(prebjetsinfo.begin(), prebjetsinfo.end(), [](const tuple<Jet,int,int> & a, const tuple<Jet,int,int> & b) -> bool
    { return ( get_property(get<0>(a), Jet_pt) > get_property(get<0>(b), Jet_pt) );});
    ei.HH_b1 = get<0>(prebjetsinfo[0]); ei.HH_b1_matchedflag= get<1>(prebjetsinfo[0]); ei.HH_b1_quarkflag= get<2>(prebjetsinfo[0]);  
    ei.HH_b2 = get<0>(prebjetsinfo[1]); ei.HH_b2_matchedflag= get<1>(prebjetsinfo[1]); ei.HH_b2_quarkflag= get<2>(prebjetsinfo[1]);  
    ei.HH_b3 = get<0>(prebjetsinfo[2]); ei.HH_b3_matchedflag= get<1>(prebjetsinfo[2]); ei.HH_b3_quarkflag= get<2>(prebjetsinfo[2]);     
    ei.HH_b4 = get<0>(prebjetsinfo[3]); ei.HH_b4_matchedflag= get<1>(prebjetsinfo[3]); ei.HH_b4_quarkflag= get<2>(prebjetsinfo[3]);  
    //Pair the four 'bjets' according the defined choice in the config file
    std::vector<std::tuple<Jet,int,int>> ordered_bjets = bbbbBothClosestToMh(prebjetsinfo);
    // order H1, H2 by pT: pT(H1) > pT (H2)   
    CompositeCandidate H1 = CompositeCandidate( get<0>(ordered_bjets[0]), get<0>(ordered_bjets[1]) );
    CompositeCandidate H2 = CompositeCandidate( get<0>(ordered_bjets[2]), get<0>(ordered_bjets[3]) );
    ei.H1=H1;
    ei.H2=H2;
    bool swapped = order_by_pT(ei.H1.get(), ei.H2.get());      
    if (!swapped)
    {
        ei.H1_b1 = get<0>(ordered_bjets[0]);
        ei.H1_b2 = get<0>(ordered_bjets[1]);
        ei.H2_b1 = get<0>(ordered_bjets[2]);
        ei.H2_b2 = get<0>(ordered_bjets[3]);      
    }
    else
    {
        ei.H1_b1 = get<0>(ordered_bjets[2]);
        ei.H1_b2 = get<0>(ordered_bjets[3]);
        ei.H2_b1 = get<0>(ordered_bjets[0]);
        ei.H2_b2 = get<0>(ordered_bjets[1]);
    }       
    //HH variables
    ei.HH = CompositeCandidate(ei.H1.get(), ei.H2.get());
    //Add VBF jets information if existing
    if(prejetsinfo.size()==6)
    {
       uint n=4; while(n<6){prejjetsinfo.push_back(make_tuple(get<0>(prejetsinfo[n]),get<1>(prejetsinfo[n]),get<2>(prejetsinfo[n])) ); n++;} 
       stable_sort(prejjetsinfo.begin(), prejjetsinfo.end(), [](const tuple<Jet,int,int> & a, const tuple<Jet,int,int> & b) -> bool
       { return ( get_property(get<0>(a), Jet_pt) > get_property(get<0>(b), Jet_pt) );}); 
       ei.JJ_j1 = get<0>(prejjetsinfo[0]); ei.JJ_j1_matchedflag= get<1>(prejjetsinfo[0]); ei.JJ_j1_quarkflag= get<2>(prejjetsinfo[0]);  
       ei.JJ_j2 = get<0>(prejjetsinfo[1]); ei.JJ_j2_matchedflag= get<1>(prejjetsinfo[1]); ei.JJ_j2_quarkflag= get<2>(prejjetsinfo[1]); 
       ei.JJ = CompositeCandidate(ei.JJ_j1.get(), ei.JJ_j2.get());  
       ei.JJ_deltaEta = abs( ei.JJ_j1->P4().Eta() - ei.JJ_j2->P4().Eta());
       ei.b1j1_deltaPhi = ei.HH_b1->P4().DeltaPhi(ei.JJ_j1->P4());
       ei.b1b2_deltaPhi = ei.HH_b1->P4().DeltaPhi(ei.HH_b2->P4());
       ei.VBFEvent = 1;
    }
    else
    {
       ei.VBFEvent = 0 ;       
    }

    return true;
}

std::vector<std::tuple<Jet,int,int>> OfflineProducerHelper::bjJets_PreselectionCut(std::vector<std::tuple<Jet,int,int>> jetsinfo)

{
    float bminimumDeepCSVAccepted           = any_cast<float>(parameterList_->at("bMinDeepCSV"          ));
    float bminimumPtAccepted                = any_cast<float>(parameterList_->at("bMinPt"               ));
    float bmaximumAbsEtaAccepted            = any_cast<float>(parameterList_->at("bMaxAbsEta"           ));
    float jminimumPtAccepted                = any_cast<float>(parameterList_->at("jMinPt"               ));
    float jmaximumAbsEtaAccepted            = any_cast<float>(parameterList_->at("jMaxAbsEta"           ));

    std::vector<std::tuple<Jet,int,int>> nobjetsinfo,outputJets;
    /////////////--------Select four b-jet candidates 
    /////////////--------b-tagging requirements    
    auto it = jetsinfo.begin();
    while (it != jetsinfo.end()){
        Jet itjet = get<0>(*it);
        if(bminimumDeepCSVAccepted>=0.){
            if(get_property(itjet,Jet_btagDeepB) < bminimumDeepCSVAccepted){
                nobjetsinfo.emplace_back(*it); 
                it=jetsinfo.erase(it);    
                continue;
            }
        }    
        if(bminimumPtAccepted>0.){
            if(itjet.P4().Pt()<bminimumPtAccepted){
                nobjetsinfo.emplace_back(*it);
                it=jetsinfo.erase(it);
                continue;                
            }
        }
        if(bmaximumAbsEtaAccepted>0.){
            if(abs(itjet.P4().Eta())>bmaximumAbsEtaAccepted){
                nobjetsinfo.emplace_back(*it);
                it=jetsinfo.erase(it);
                continue;                
            }
        }
        ++it;
    }

    /////////////--------Check that there is at least 4 bjet candidates
    if(jetsinfo.size() < 4) return outputJets;
    //cout<<jetsinfo.size()<<endl;
    stable_sort(jetsinfo.begin(), jetsinfo.end(), [](const tuple<Jet,int,int> & a, const tuple<Jet,int,int> & b) -> bool
    { return ( get_property(get<0>(a), Jet_btagDeepB) > get_property(get<0>(b), Jet_btagDeepB) );});
    /////////////--------Pick up the four b-jets 
    outputJets = {{*(jetsinfo.begin()+0),*(jetsinfo.begin()+1),*(jetsinfo.begin()+2),*(jetsinfo.begin()+3)}};
    int c=0; while (c<4){jetsinfo.erase(jetsinfo.begin());c++;}
    /////////////--------Select two VBF-jet candidates based on PT and ETA1*ETA2s
    jetsinfo.insert(jetsinfo.end(), nobjetsinfo.begin(), nobjetsinfo.end());
    
    auto jt = jetsinfo.begin();
    while (jt != jetsinfo.end()){
        Jet jtjet = get<0>(*jt);        
        if(jminimumPtAccepted>0.){
            if(jtjet.P4().Pt()<jminimumPtAccepted){
                jt=jetsinfo.erase(jt);
                continue;                
            }
        }
        if(jmaximumAbsEtaAccepted>0.){
            if(abs(jtjet.P4().Eta())>jmaximumAbsEtaAccepted){
                jt=jetsinfo.erase(jt);
                continue;                
            }
        }
        ++jt;
    }
    if(jetsinfo.size() < 2) return outputJets;
    stable_sort(jetsinfo.begin(), jetsinfo.end(), [](const tuple<Jet,int,int> & a, const tuple<Jet,int,int> & b) -> bool
    { return ( get_property(get<0>(a), Jet_pt ) >  get_property(get<0>(b), Jet_pt)  );});
    std::vector<std::tuple<Jet,int,int>> VBFjets = OppositeEtaJetPair(jetsinfo);
    if(VBFjets.size() < 2) return outputJets;
    /////////////--------Load information of preselected jets: outputJets = (4 b-jets, 2 VBF jets, rest) and return      
    outputJets.insert(outputJets.end(),VBFjets.begin(),VBFjets.end());
    return outputJets;
}

std::vector<std::tuple<Jet,int,int>> OfflineProducerHelper::bbbbBothClosestToMh(std::vector<std::tuple<Jet,int,int>> presel_jets)
{
    float targetHiggsMass = any_cast<float>(parameterList_->at("HiggsMass"));
    std::vector<float> mHs;

    stable_sort(presel_jets.begin(), presel_jets.end(), [](const tuple<Jet,int,int> & a, const tuple<Jet,int,int> & b) -> bool
    { return ( get_property(get<0>(a), Jet_pt) > get_property(get<0>(b), Jet_pt) );});

    for (uint i = 0; i < presel_jets.size(); ++i)
        for (uint j = i+1; j < presel_jets.size(); ++j)
        {
            TLorentzVector p4sum = (get<0>(presel_jets[i]).P4() + get<0>(presel_jets[j]).P4());
            mHs.emplace_back(p4sum.Mag());
        }

    std::pair<float, float> m_12_34 = make_pair (mHs.at(0), mHs.at(5));
    std::pair<float, float> m_13_24 = make_pair (mHs.at(1), mHs.at(4));
    std::pair<float, float> m_14_23 = make_pair (mHs.at(2), mHs.at(3));

    float r12_34 = sqrt (pow(m_12_34.first - targetHiggsMass, 2) + pow(m_12_34.second - targetHiggsMass, 2) );
    float r13_24 = sqrt (pow(m_13_24.first - targetHiggsMass, 2) + pow(m_13_24.second - targetHiggsMass, 2) );
    float r14_23 = sqrt (pow(m_14_23.first - targetHiggsMass, 2) + pow(m_14_23.second - targetHiggsMass, 2) );

    float the_min = std::min({r12_34, r13_24, r14_23});

    std::vector<std::tuple<Jet,int,int>> outputJets = presel_jets;

    if (the_min == r12_34){
        outputJets.at(0) = presel_jets.at(1 - 1);
        outputJets.at(1) = presel_jets.at(2 - 1);
        outputJets.at(2) = presel_jets.at(3 - 1);
        outputJets.at(3) = presel_jets.at(4 - 1);
    }

    else if (the_min == r13_24){
        outputJets.at(0) = presel_jets.at(1 - 1);
        outputJets.at(1) = presel_jets.at(3 - 1);
        outputJets.at(2) = presel_jets.at(2 - 1);
        outputJets.at(3) = presel_jets.at(4 - 1);
    }

    else if (the_min == r14_23){
        outputJets.at(0) = presel_jets.at(1 - 1);
        outputJets.at(1) = presel_jets.at(4 - 1);
        outputJets.at(2) = presel_jets.at(2 - 1);
        outputJets.at(3) = presel_jets.at(3 - 1);   
    }

    else
        cout << "** [WARNING] : bbbb_jets_idxs_BothClosestToMh : something went wrong with finding the smallest radius" << endl;
    return outputJets;
}

std::vector<std::tuple<Jet,int,int>> OfflineProducerHelper::bbbbOneClosestToMh(std::vector<std::tuple<Jet,int,int>> presel_jets)
{
    float targetHiggsMass = any_cast<float>(parameterList_->at("HiggsMass"));
    std::vector<pair <float, pair<int,int>>> mHs_and_jetIdx; // each entry is the mH and the two idxs of the pair
    
    for (uint i = 0; i < presel_jets.size(); ++i)
        for (uint j = i+1; j < presel_jets.size(); ++j)
        {
            TLorentzVector p4sum = (get<0>(presel_jets[i]).P4Regressed() + get<0>(presel_jets[j]).P4Regressed());
            float dmh = fabs(p4sum.Mag() - targetHiggsMass);
            mHs_and_jetIdx.emplace_back(make_pair(dmh, make_pair(i,j)));
        }

    // sort to get the pair closest to mH
    stable_sort (mHs_and_jetIdx.begin(), mHs_and_jetIdx.end());

    std::vector<std::tuple<Jet,int,int>> outputJets = presel_jets;
    int ij0 = mHs_and_jetIdx.begin()->second.first;
    int ij1 = mHs_and_jetIdx.begin()->second.second;

    // get the other two jets. The following creates a vector with idxs 0/1/2/3, and then removes ij1 and ij2
    std::vector<int> vres;
    for (uint i = 0; i < presel_jets.size(); ++i) vres.emplace_back(i);
    vres.erase(std::remove(vres.begin(), vres.end(), ij0), vres.end());
    vres.erase(std::remove(vres.begin(), vres.end(), ij1), vres.end());
    
    int ij2 = vres.at(0);
    int ij3 = vres.at(1);

    outputJets.at(0) = presel_jets.at(ij0);
    outputJets.at(1) = presel_jets.at(ij1);
    outputJets.at(2) = presel_jets.at(ij2);
    outputJets.at(3) = presel_jets.at(ij3);

    return outputJets;
}

std::vector<std::tuple<Jet,int,int>> OfflineProducerHelper::OppositeEtaJetPair(std::vector<std::tuple<Jet,int,int>> jjets){
//Initialize DEta 
int id;
float Eta1Eta2= 0; bool foundpair=false;
std::vector<std::tuple<Jet,int,int>> outputJets;
for (uint y=1;y<jjets.size();y++ )
{
        Eta1Eta2 = get<0>(jjets[0]).P4().Eta() * get<0>(jjets[y]).P4().Eta()  ;
        if (Eta1Eta2<0)
        {
            id = y; foundpair=true;
        }
        if(foundpair) break;
}
if(!foundpair) return outputJets;
outputJets = {{*(jjets.begin()+0),*(jjets.begin()+id)}}; return outputJets;
}

std::vector<std::tuple<Jet,int,int>> OfflineProducerHelper::AddGenMatchingInfo(NanoAODTree& nat, EventInfo& ei, std::vector<Jet> jets)
{

    //OUTPUT: Vector of tuples ( tuple = [Jet, MatchingFlag, QuarkId] )
    std::vector<std::tuple<Jet,int,int>> output;
    //Order the generator level by PT  
    order_by_pT(ei.gen_H1_b1.get(), ei.gen_H1_b2.get());              
    order_by_pT(ei.gen_H2_b1.get(), ei.gen_H2_b2.get());
    order_by_pT(ei.gen_q1_out.get(), ei.gen_q2_out.get());
    std::vector<GenPart> bs = {{*(ei.gen_H1_b1),*(ei.gen_H1_b2),*(ei.gen_H2_b1),*(ei.gen_H2_b2)}};
    bool swapped = order_by_pT(ei.gen_H1.get(), ei.gen_H2.get());
    if (!swapped)
    {
        ei.gen_H1_b1 = bs.at(0);
        ei.gen_H1_b2 = bs.at(1);
        ei.gen_H2_b1 = bs.at(2);
        ei.gen_H2_b2 = bs.at(3); 
    }
    else
    {
        ei.gen_H1_b1 = bs.at(2);
        ei.gen_H1_b2 = bs.at(3);
        ei.gen_H2_b1 = bs.at(0);
        ei.gen_H2_b2 = bs.at(1);         
    } 
    //Define a vector with the six ordered quarks   
    std::vector<GenPart> quarks = {{
        *(ei.gen_H1_b1),*(ei.gen_H1_b2),
        *(ei.gen_H2_b1),*(ei.gen_H2_b2),
        *(ei.gen_q1_out),*(ei.gen_q2_out)}};
    //minfo: Vector of tuples ( tuple = [MatchingFlag, QuarkId, JetId] )     
    std::vector<std::tuple<int,int,int>> minfo = QuarkToJetMatcher(quarks,jets); 
    //Fill output vector tuple with the jet information
    bool found; int foundy;
    for (uint x=0; x < jets.size(); x++ ){
          uint jetid=x;
          found = false;
          //Check if there is a quark that is linked to this jet
          for (uint y=0; y < minfo.size(); y++ ){
          uint m = get<2>(minfo[y]);
          if(jetid == m ){found = true; foundy=y;}   
          }
          //Load jet information to the output: [Jet, MatchingFlag, QuarkId]
          if(found){output.emplace_back(make_tuple(jets.at(x),1,get<1>(minfo[foundy]) ));}
          else{output.emplace_back(make_tuple(jets.at(x),0,-1));}   
    }    
    return output; 
 } 

std::vector<std::tuple<int,int,int>> OfflineProducerHelper::QuarkToJetMatcher(const std::vector<GenPart> quarks, std::vector<Jet> jets){
// OUTPUT = (MatchingFlag, QuarkIdx, JetIdx)
//----MatchingFlag: 0 (Unmatched) or 1 (Matched)
//----QuarkId: (0) gen_H1_b1, (1) gen_H1_b2, (2) gen_H2_b1, (3) gen_H2_b2, (4) gen_j1_out, (5) gen_j2_out, (-1) Nothing  
//----JetId: Index of the jets in the input vector 'jets'
//Define and initialize variables
std::vector<std::tuple<TLorentzVector,int>> jetsinfo,quarksinfo;
std::vector<std::tuple<int,int,int>> output; uint id;
float dR=0.3, maxDeltaR, DeltaR; bool matched = false;
uint m=0; while(m<quarks.size()){quarksinfo.emplace_back( make_tuple(quarks.at(m).P4(), m)); m++;}
uint n=0; while(n<jets.size()){jetsinfo.emplace_back( make_tuple(jets.at(n).P4(), n)    ); n++;  }
//Create all possible combinations and find the jet set that minimize the maximum deltaEta
for (uint x=0;x < quarksinfo.size();x++ )
{
 maxDeltaR = dR;
 for (uint y=0;y < jetsinfo.size(); y++ ){

      DeltaR = get<0>(quarksinfo[x]).DeltaR( get<0>(jetsinfo[y]) ); 
      if(DeltaR < maxDeltaR){maxDeltaR=DeltaR; matched=true; id = y ;}
 }
 if(matched) {output.emplace_back( make_tuple(1,x,get<1>(jetsinfo[id])) ); jetsinfo.erase(jetsinfo.begin()+id);}
 else {output.emplace_back( make_tuple(0,x,-1) );}
 matched = false;
} 

return output;
}

////////////-----FUNCTIONS FOR PRESELECTION OF EVENTS FOR NON-RESONANT ANALYSIS - END


bool OfflineProducerHelper::select_gen_HH (NanoAODTree& nat, EventInfo& ei)
{
    bool all_ok = true;
    for (uint igp = 0; igp < *(nat.nGenPart); ++igp)
    {
        GenPart gp (igp, &nat);
        if (abs(get_property(gp, GenPart_pdgId)) != 25) continue;
        // bool isFirst = checkBit(get_property(gp, GenPart_statusFlags), 12); // 12: isFirstCopy
        // if (!isFirst) continue;
        if (gp.isFirstCopy())
        {
            if (!assign_to_uninit(gp, {&ei.gen_H1, &ei.gen_H2} )) {
                cout << "** [WARNING] : select_gen_HH : more than two Higgs found" << endl;
                all_ok = false;
            }
            
            // // assign
            // if      (!ei.gen_H1) ei.gen_H1 = gp;
            // else if (!ei.gen_H2) ei.gen_H2 = gp;
            // else{
            //     cout << "** [WARNING] : select_gen_HH : more than two Higgs found" << endl;
            //     return false;
            // }
        }
        if (gp.isLastCopy())
        {
            if (!assign_to_uninit(gp, {&ei.gen_H1_last, &ei.gen_H2_last} )) {
                cout << "** [WARNING] : select_gen_HH : more than two Higgs found (last copy)" << endl;
                all_ok = false;
            }

            // assign
            // if      (!ei.gen_H1_last) ei.gen_H1_last = gp;
            // else if (!ei.gen_H2_last) ei.gen_H2_last = gp;
            // else{
            //     cout << "** [WARNING] : select_gen_HH : more than two Higgs found (last copy)" << endl;
            //     return false;
            // }
        }
    }

    if (!ei.gen_H1 || !ei.gen_H2){
        cout << "** [WARNING] : select_gen_HH : didn't find two Higgs : "
             << std::boolalpha
             << "H1 :" << ei.gen_H1.is_initialized()
             << "H2 :" << ei.gen_H2.is_initialized()
             << std::noboolalpha
             << endl;
        all_ok = false;
    }
    return all_ok;
}



bool OfflineProducerHelper::select_gen_bb_bb (NanoAODTree& nat, EventInfo& ei)
{
    if (!ei.gen_H1 || !ei.gen_H2)
    {
        cout << "** [WARNING] : select_gen_bb_bb : you need to search for H1 and H2 before" << endl;
        return false;
    }

    bool all_ok = true;
    for (uint igp = 0; igp < *(nat.nGenPart); ++igp)
    {
        GenPart gp (igp, &nat);
        if (abs(get_property(gp, GenPart_pdgId)) != 5) continue;
        // bool isFirst = checkBit(get_property(gp, GenPart_statusFlags), 12); // 12: isFirstCopy
        // if (!isFirst) continue;
        if (!gp.isFirstCopy()) continue;
        
        int idxMoth = get_property(gp, GenPart_genPartIdxMother);
        if (idxMoth == ei.gen_H1_last->getIdx())
        {
            if (!assign_to_uninit(gp, {&ei.gen_H1_b1, &ei.gen_H1_b2} )) {
                cout << "** [WARNING] : select_gen_bb_bb : more than two b from H1 found" << endl;
                all_ok = false;                
            }
            // if      (!ei.gen_H1_b1) ei.gen_H1_b1 = gp;
            // else if (!ei.gen_H1_b2) ei.gen_H1_b2 = gp;
            // else{
            //     cout << "** [WARNING] : select_gen_bb_bb : more than two b from H1 found" << endl;
            //     all_ok = false;
            // }
        }
        else if (idxMoth == ei.gen_H2_last->getIdx())
        {
            if (!assign_to_uninit(gp, {&ei.gen_H2_b1, &ei.gen_H2_b2} )) {
                cout << "** [WARNING] : select_gen_bb_bb : more than two b from H2 found" << endl;
                all_ok = false;                
            }

            // if      (!ei.gen_H2_b1) ei.gen_H2_b1 = gp;
            // else if (!ei.gen_H2_b2) ei.gen_H2_b2 = gp;
            // else{
            //     cout << "** [WARNING] : select_gen_bb_bb : more than two b from H2 found" << endl;
            //     all_ok = false;
            // }            
        }
        else
        {
            // cout << "** [WARNING] : select_gen_bb_bb : found a b quark of idx " << gp.getIdx() << " and mother " << idxMoth
            //      << " that does not match last H1 H2 idx " << ei.gen_H1_last->getIdx() << " " << ei.gen_H2_last->getIdx()
            //      << endl;
            //      all_ok = false;
            // possibly something that has b --> b + g --> b + (other stuff)
        }
    }
    if (!all_ok)
    {
        cout << "** [DEBUG] : select_gen_bb_bb : something went wrong, dumping gen parts" << endl;
        dump_gen_part(nat, true);
    }
    return all_ok;
}

bool OfflineProducerHelper::select_gen_VBF_partons (NanoAODTree& nat, EventInfo& ei)
{

    bool all_ok = true;

    for (uint igp = 0; igp < *(nat.nGenPart); ++igp)
    {
        GenPart gp (igp, &nat);
        if (abs(get_property(gp, GenPart_pdgId)) >= 6) continue; // only light quarks + b
        // auto flags = get_property(gp, GenPart_statusFlags);
        // search for ingoing partons
        // if (!) continue; // 12: isFirstCopy
        // search for outgoing partons

        if (get_property(gp, GenPart_status) == 21) // incoming VBF parton
        {
            // if      (!ei.gen_q1_in) ei.gen_q1_in = gp;
            // else if (!ei.gen_q2_in) ei.gen_q2_in = gp;
            // else{
            //     cout << "** [WARNING] : select_gen_VBF_partons : more than two incoming partons found" << endl;
            //     all_ok = false;
            // }    

            if (!assign_to_uninit(gp, {&ei.gen_q1_in, &ei.gen_q2_in} )) {
                cout << "** [WARNING] : select_gen_VBF_partons : more than two incoming partons found" << endl;
                all_ok = false;
            }
        }

        else
        {
            // it appears that in the VBF sample, the first objects in the list are the VBF ingoing partons
            // and that the next ones are the outgoing partons, 1st copy
            // so checking that idxMother == 0 should be enough for the VBF sample in use (checked on 80X on 19/01/2018)
            
            // FIXME: how to ensure the correspondence in_1 --> out_1, in_2 --> out_2 ?
            // unfortunately there is no valid gen info associated
            if (get_property(gp, GenPart_genPartIdxMother) == 0)
            {
                // if      (!ei.gen_q1_out) ei.gen_q1_out = gp;
                // else if (!ei.gen_q2_out) ei.gen_q2_out = gp;
                // else {
                //     cout << "** [WARNING] : select_gen_VBF_partons : more than two outgoing partons found" << endl;
                //     all_ok = false;
                // }
                if (!assign_to_uninit(gp, {&ei.gen_q1_out, &ei.gen_q2_out} )) {
                    cout << "** [WARNING] : select_gen_VBF_partons : more than two outgoing partons found" << endl;
                    all_ok = false;
                }
            }

            // the last copy of the outgoing parton can be checked by verifying two conditions:
            // 1. is last copy
            // 2. its mother is one of the outgoing VBF partons at ME. As they are before in the gen part list, at this point they should already have been identified
            // 23/01/2018: commenting out the outgoing partons, as it is not clear if this information makes sense
            else
            {
                // bool good_last = gp.isLastCopy();
                // if (ei.gen_q1_out && ei.gen_q2_out)
                // {
                //     // auto moth_idx = get_property(gp, GenPart_genPartIdxMother);
                //     auto moth_idx = recursive_gen_mother_idx(gp); // make a recursive search, if intermediate copies where radiated
                //     good_last = good_last && ((moth_idx == ei.gen_q1_out->getIdx()) || (moth_idx == ei.gen_q2_out->getIdx()));
                // }
                // else
                //     good_last = false;
                
                // // now check and save
                // if (good_last)
                // {
                //     if      (!ei.gen_q1_out_lastcopy) ei.gen_q1_out_lastcopy = gp;
                //     else if (!ei.gen_q2_out_lastcopy) ei.gen_q2_out_lastcopy = gp;
                //     else {
                //         cout << "** [WARNING] : select_gen_VBF_partons : more than two outgoing partons (last copy) found" << endl;
                //         all_ok = false;
                //     }
                // }
            }
        }
    }

    // quality checks

    if (!ei.gen_q1_in || !ei.gen_q2_in){
    cout << "** [WARNING] : select_gen_VBF_partons : didn't find two incoming partons : "
         << std::boolalpha
         << " q1_in :" << ei.gen_q1_in.is_initialized()
         << " q2_in :" << ei.gen_q2_in.is_initialized()
         << std::noboolalpha
         << endl;
        all_ok = false;
    }
    
    if (!ei.gen_q1_out || !ei.gen_q2_out){
    cout << "** [WARNING] : select_gen_VBF_partons : didn't find two outgoing partons : "
         << std::boolalpha
         << " q1_out :" << ei.gen_q1_out.is_initialized()
         << " q2_out :" << ei.gen_q2_out.is_initialized()
         << std::noboolalpha
         << endl;
        all_ok = false;
    }    
    
    // if (!ei.gen_q1_out_lastcopy || !ei.gen_q2_out_lastcopy){
    // cout << "** [WARNING] : select_gen_VBF_partons : didn't find two outgoing partons (last copy) : "
    //      << std::boolalpha
    //      << " q1_out_lastcopy :" << ei.gen_q1_out_lastcopy.is_initialized()
    //      << " q2_out_lastcopy :" << ei.gen_q2_out_lastcopy.is_initialized()
    //      << std::noboolalpha
    //      << endl;
    //     all_ok = false;
    // }    

    // // print a debug
    // if (!all_ok)
    // {
    //     cout << "** [DEBUG] select_gen_VBF_partons : something went wrong, dumping gen parts" << endl;
    //     for (uint igp = 0; igp < *(nat.nGenPart); ++igp)
    //     {
    //         GenPart gp (igp, &nat);
    //         // if (abs(get_property(gp, GenPart_pdgId)) >= 6) continue; // only light quarks + b
    //         cout << boolalpha;
    //         cout << igp << " -- "
    //              << " pdgId: "      << setw(4)  << get_property(gp, GenPart_pdgId)
    //              << " pt: "         << setw(10) << get_property(gp, GenPart_pt)
    //              << " eta: "        << setw(10) << get_property(gp, GenPart_eta)
    //              << " phi: "        << setw(10) << get_property(gp, GenPart_phi)
    //              << " status: "     << setw(4)  << get_property(gp, GenPart_status)
    //              << " moth_idx: "   << setw(4)  << get_property(gp, GenPart_genPartIdxMother)
    //              << endl;
    //         cout << "    . Flags :" << endl
    //             << "       isPrompt :                           " << gp.isPrompt() << endl
    //             << "       isDecayedLeptonHadron :              " << gp.isDecayedLeptonHadron() << endl
    //             << "       isTauDecayProduct :                  " << gp.isTauDecayProduct() << endl
    //             << "       isPromptTauDecayProduct :            " << gp.isPromptTauDecayProduct() << endl
    //             << "       isDirectTauDecayProduct :            " << gp.isDirectTauDecayProduct() << endl
    //             << "       isDirectPromptTauDecayProduct :      " << gp.isDirectPromptTauDecayProduct() << endl
    //             << "       isDirectHadronDecayProduct :         " << gp.isDirectHadronDecayProduct() << endl
    //             << "       isHardProcess :                      " << gp.isHardProcess() << endl
    //             << "       fromHardProcess :                    " << gp.fromHardProcess() << endl
    //             << "       isHardProcessTauDecayProduct :       " << gp.isHardProcessTauDecayProduct() << endl
    //             << "       isDirectHardProcessTauDecayProduct : " << gp.isDirectHardProcessTauDecayProduct() << endl
    //             << "       fromHardProcessBeforeFSR :           " << gp.fromHardProcessBeforeFSR() << endl
    //             << "       isFirstCopy :                        " << gp.isFirstCopy() << endl
    //             << "       isLastCopy :                         " << gp.isLastCopy() << endl
    //             << "       isLastCopyBeforeFSR :                " << gp.isLastCopyBeforeFSR() << endl
    //             << endl;
    //         cout << noboolalpha;
    //     }
    //     cout << endl << endl;
    // } // end of debug block

    return all_ok;
}

void OfflineProducerHelper::dump_gen_part (NanoAODTree& nat, bool printFlags)
{
    // print a debug
    cout << "** [DEBUG] dumping gen parts of event " << *(nat.event) << endl;
    cout << boolalpha;
    for (uint igp = 0; igp < *(nat.nGenPart); ++igp)
    {
        GenPart gp (igp, &nat);
        // if (abs(get_property(gp, GenPart_pdgId)) >= 6) continue; // only light quarks + b
        cout << igp << " -- "
             << " pdgId: "      << setw(4)  << get_property(gp, GenPart_pdgId)
             << " pt: "         << setw(10) << get_property(gp, GenPart_pt)
             << " eta: "        << setw(10) << get_property(gp, GenPart_eta)
             << " phi: "        << setw(10) << get_property(gp, GenPart_phi)
             << " status: "     << setw(4)  << get_property(gp, GenPart_status)
             << " moth_idx: "   << setw(4)  << get_property(gp, GenPart_genPartIdxMother)
             << endl;
        if (printFlags)
        {
            cout << "    . Flags :" << endl
                << "       isPrompt :                           " << gp.isPrompt() << endl
                << "       isDecayedLeptonHadron :              " << gp.isDecayedLeptonHadron() << endl
                << "       isTauDecayProduct :                  " << gp.isTauDecayProduct() << endl
                << "       isPromptTauDecayProduct :            " << gp.isPromptTauDecayProduct() << endl
                << "       isDirectTauDecayProduct :            " << gp.isDirectTauDecayProduct() << endl
                << "       isDirectPromptTauDecayProduct :      " << gp.isDirectPromptTauDecayProduct() << endl
                << "       isDirectHadronDecayProduct :         " << gp.isDirectHadronDecayProduct() << endl
                << "       isHardProcess :                      " << gp.isHardProcess() << endl
                << "       fromHardProcess :                    " << gp.fromHardProcess() << endl
                << "       isHardProcessTauDecayProduct :       " << gp.isHardProcessTauDecayProduct() << endl
                << "       isDirectHardProcessTauDecayProduct : " << gp.isDirectHardProcessTauDecayProduct() << endl
                << "       fromHardProcessBeforeFSR :           " << gp.fromHardProcessBeforeFSR() << endl
                << "       isFirstCopy :                        " << gp.isFirstCopy() << endl
                << "       isLastCopy :                         " << gp.isLastCopy() << endl
                << "       isLastCopyBeforeFSR :                " << gp.isLastCopyBeforeFSR() << endl
                << endl;
        }
    }
    cout << noboolalpha;
    cout << endl << endl;
}

// bool OfflineProducerHelper::checkBit (int number, int bitpos)
// {
//     bool res = number & (1 << bitpos);
//     return res;
// }

int OfflineProducerHelper::recursive_gen_mother_idx(const GenPart& gp, bool stop_at_moth_zero)
{
    int imoth = get_property(gp, GenPart_genPartIdxMother);
    if (imoth < 0)
        return gp.getIdx();
    if (imoth == 0 && stop_at_moth_zero)
        return gp.getIdx();
    GenPart gp_moth (imoth, gp.getNanoAODTree());
    return recursive_gen_mother_idx(gp_moth, stop_at_moth_zero);
}