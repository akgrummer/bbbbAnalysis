#include "OfflineProducerHelper.h"
#include <iostream>
#include <iomanip>
#include <cmath>

#include "CompositeCandidate.h"
#include "Jet.h"
#include "Electron.h"
#include "Muon.h"
#include "GenPart.h"
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



// ----------------- Compute weights - BEGIN ----------------- //

void OfflineProducerHelper::initializeObjectsForWeights(OutputTree &ot){

    string weightsMethod = any_cast<string>(parameterList_->at("WeightsMethod"));

    if(weightsMethod == "None"){
        //do nothing
    }
    else if(weightsMethod == "FourBtag_EventReweighting"){
        ot.declareUserFloatBranch("bTagWeight_central"          , 1.);
        ot.declareUserFloatBranch("bTagWeight_bJets_up"         , 1.);
        ot.declareUserFloatBranch("bTagWeight_bJets_down"       , 1.);
        ot.declareUserFloatBranch("bTagWeight_cJets_up"         , 1.);
        ot.declareUserFloatBranch("bTagWeight_cJets_down"       , 1.);
        ot.declareUserFloatBranch("bTagWeight_lightJets_up"     , 1.);
        ot.declareUserFloatBranch("bTagWeight_lightJets_down"   , 1.);

        BTagCalibration btagCalibration("DeepCSV","weights/DeepCSV_Moriond17_B_H.csv");    
        btagCalibrationReader_lightJets_ = new BTagCalibrationReader(BTagEntry::OP_MEDIUM,"central",{"up", "down"});      
        btagCalibrationReader_cJets_     = new BTagCalibrationReader(BTagEntry::OP_MEDIUM,"central",{"up", "down"});      
        btagCalibrationReader_bJets_     = new BTagCalibrationReader(BTagEntry::OP_MEDIUM,"central",{"up", "down"}); 

        btagCalibrationReader_lightJets_->load(btagCalibration, BTagEntry::FLAV_UDSG, "incl"  );
        btagCalibrationReader_cJets_    ->load(btagCalibration, BTagEntry::FLAV_C   , "mujets");
        btagCalibrationReader_bJets_    ->load(btagCalibration, BTagEntry::FLAV_B   , "mujets");
    }

    return;

}


// reject events with leptons that may come from W and Z decays
void OfflineProducerHelper::compute_weights_fourBtag_eventReweighting (const std::vector<Jet> &jets, NanoAODTree& nat, OutputTree &ot){
    
    float tmpWeight_bJets_central     = 1.;
    float tmpWeight_bJets_up          = 1.;
    float tmpWeight_bJets_down        = 1.;
    float tmpWeight_cJets_central     = 1.;
    float tmpWeight_cJets_up          = 1.;
    float tmpWeight_cJets_down        = 1.;
    float tmpWeight_lightJets_central = 1.;
    float tmpWeight_lightJets_up      = 1.;
    float tmpWeight_lightJets_down    = 1.;

    for(const auto &iJet : jets){
        int jetFlavour = abs(get_property(iJet,Jet_partonFlavour));
        if(jetFlavour==5){
            tmpWeight_bJets_central     *= btagCalibrationReader_bJets_    ->eval_auto_bounds("central", BTagEntry::FLAV_B   , iJet.P4().Eta(), iJet.P4().Pt());
            tmpWeight_bJets_up          *= btagCalibrationReader_bJets_    ->eval_auto_bounds("up"     , BTagEntry::FLAV_B   , iJet.P4().Eta(), iJet.P4().Pt());
            tmpWeight_bJets_down        *= btagCalibrationReader_bJets_    ->eval_auto_bounds("down"   , BTagEntry::FLAV_B   , iJet.P4().Eta(), iJet.P4().Pt());
        }
        else if(jetFlavour==4){
            tmpWeight_cJets_central     *= btagCalibrationReader_cJets_    ->eval_auto_bounds("central", BTagEntry::FLAV_C   , iJet.P4().Eta(), iJet.P4().Pt());
            tmpWeight_cJets_up          *= btagCalibrationReader_cJets_    ->eval_auto_bounds("up"     , BTagEntry::FLAV_C   , iJet.P4().Eta(), iJet.P4().Pt());
            tmpWeight_cJets_down        *= btagCalibrationReader_cJets_    ->eval_auto_bounds("down"   , BTagEntry::FLAV_C   , iJet.P4().Eta(), iJet.P4().Pt());
        }
        else{
            tmpWeight_lightJets_central *= btagCalibrationReader_lightJets_->eval_auto_bounds("central", BTagEntry::FLAV_UDSG, iJet.P4().Eta(), iJet.P4().Pt());
            tmpWeight_lightJets_up      *= btagCalibrationReader_lightJets_->eval_auto_bounds("up"     , BTagEntry::FLAV_UDSG, iJet.P4().Eta(), iJet.P4().Pt());
            tmpWeight_lightJets_down    *= btagCalibrationReader_lightJets_->eval_auto_bounds("down"   , BTagEntry::FLAV_UDSG, iJet.P4().Eta(), iJet.P4().Pt());
        }   
    }

    ot.userFloat("bTagWeight_central"          ) = tmpWeight_bJets_central * tmpWeight_cJets_central * tmpWeight_lightJets_central ;
    ot.userFloat("bTagWeight_bJets_up"         ) = tmpWeight_bJets_up      * tmpWeight_cJets_central * tmpWeight_lightJets_central ;
    ot.userFloat("bTagWeight_bJets_down"       ) = tmpWeight_bJets_down    * tmpWeight_cJets_central * tmpWeight_lightJets_central ;
    ot.userFloat("bTagWeight_cJets_up"         ) = tmpWeight_bJets_central * tmpWeight_cJets_up      * tmpWeight_lightJets_central ;
    ot.userFloat("bTagWeight_cJets_down"       ) = tmpWeight_bJets_central * tmpWeight_cJets_down    * tmpWeight_lightJets_central ;
    ot.userFloat("bTagWeight_lightJets_up"     ) = tmpWeight_bJets_central * tmpWeight_cJets_central * tmpWeight_lightJets_up      ;
    ot.userFloat("bTagWeight_lightJets_down"   ) = tmpWeight_bJets_central * tmpWeight_cJets_central * tmpWeight_lightJets_down    ;

    return;
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
    else throw std::runtime_error("cannot recognize cut strategy " + preselectionCutStrategy);

    //at least 4 jets required
    if(jets.size()<4) return false;

    // calculate weights after preselection cuts
    if(parameterList_->find("WeightsMethod") != parameterList_->end()){ //is it a MC event
        const string weightsMethod = any_cast<string>(parameterList_->at("WeightsMethod"));

        if(weightsMethod == "FourBtag_EventReweighting"){
            compute_weights_fourBtag_eventReweighting(jets,nat,ot);
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