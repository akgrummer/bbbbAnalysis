#include "TFile.h"
#include "TF1.h"
#include "TFitResult.h"
#include "TGraphErrors.h"
#include "Math/WrappedMultiTF1.h"

namespace TriggerFitCurves2016
{
    TFile triggerFitFile("TriggerEfficiency_Fit_2016.root");
    class KFitResult : public TFitResult
    {
    public:
        using TFitResult::TFitResult;
        KFitResult* ResetModelFunction(TF1* func){
            this->SetModelFunction(std::shared_ptr<IModelFunction>(dynamic_cast<IModelFunction*>(ROOT::Math::WrappedMultiTF1(*func).Clone())));
            return this;
        }
    };
    std::pair<TF1*,KFitResult*> createPair(TF1* theFunction, KFitResult* theFitResult )
    {
        theFitResult->ResetModelFunction(theFunction);
        return {theFunction, theFitResult};
    }

    std::pair<TF1*, KFitResult*> fSingleMuon_Double90Quad30_Efficiency_L1filterHTPair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon_Double90Quad30_Efficiency_L1filterHT"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon_Double90Quad30_Efficiency_L1filterHT_FitResult")
    );

    std::pair<TF1*, KFitResult*> fSingleMuon_Double90Quad30_Efficiency_QuadCentralJet30Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon_Double90Quad30_Efficiency_QuadCentralJet30"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon_Double90Quad30_Efficiency_QuadCentralJet30_FitResult")
    );

    std::pair<TF1*, KFitResult*> fSingleMuon_Double90Quad30_Efficiency_DoubleCentralJet90Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon_Double90Quad30_Efficiency_DoubleCentralJet90"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon_Double90Quad30_Efficiency_DoubleCentralJet90_FitResult")
    );

    std::pair<TF1*, KFitResult*> fSingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087TriplePair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087Triple"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon_Double90Quad30_Efficiency_BTagCaloCSVp087Triple_FitResult")
    );

    std::pair<TF1*, KFitResult*> fSingleMuon_Double90Quad30_Efficiency_QuadPFCentralJetLooseID30Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon_Double90Quad30_Efficiency_QuadPFCentralJetLooseID30"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon_Double90Quad30_Efficiency_QuadPFCentralJetLooseID30_FitResult")
    );

    std::pair<TF1*, KFitResult*> fSingleMuon_Double90Quad30_Efficiency_DoublePFCentralJetLooseID90Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon_Double90Quad30_Efficiency_DoublePFCentralJetLooseID90"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon_Double90Quad30_Efficiency_DoublePFCentralJetLooseID90_FitResult")
    );

    std::pair<TF1*, KFitResult*> fSingleMuon_Quad45_Efficiency_L1filterHTPair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon_Quad45_Efficiency_L1filterHT"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon_Quad45_Efficiency_L1filterHT_FitResult")
    );

    std::pair<TF1*, KFitResult*> fSingleMuon_Quad45_Efficiency_QuadCentralJet45Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon_Quad45_Efficiency_QuadCentralJet45"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon_Quad45_Efficiency_QuadCentralJet45_FitResult")
    );

    std::pair<TF1*, KFitResult*> fSingleMuon_Quad45_Efficiency_BTagCaloCSVp087TriplePair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon_Quad45_Efficiency_BTagCaloCSVp087Triple"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon_Quad45_Efficiency_BTagCaloCSVp087Triple_FitResult")
    );

    std::pair<TF1*, KFitResult*> fSingleMuon_Quad45_Efficiency_QuadPFCentralJetLooseID45Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon_Quad45_Efficiency_QuadPFCentralJetLooseID45"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon_Quad45_Efficiency_QuadPFCentralJetLooseID45_FitResult")
    );

    std::pair<TF1*, KFitResult*> fSingleMuon_And_Efficiency_L1filterQuad45HTPair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon_And_Efficiency_L1filterQuad45HT"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon_And_Efficiency_L1filterQuad45HT_FitResult")
    );

    std::pair<TF1*, KFitResult*> fSingleMuon_And_Efficiency_QuadCentralJet45Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon_And_Efficiency_QuadCentralJet45"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon_And_Efficiency_QuadCentralJet45_FitResult")
    );

    std::pair<TF1*, KFitResult*> fSingleMuon_And_Efficiency_QuadPFCentralJetLooseID45Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon_And_Efficiency_QuadPFCentralJetLooseID45"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon_And_Efficiency_QuadPFCentralJetLooseID45_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar_Double90Quad30_Efficiency_L1filterHTPair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar_Double90Quad30_Efficiency_L1filterHT"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar_Double90Quad30_Efficiency_L1filterHT_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar_Double90Quad30_Efficiency_QuadCentralJet30Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar_Double90Quad30_Efficiency_QuadCentralJet30"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar_Double90Quad30_Efficiency_QuadCentralJet30_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar_Double90Quad30_Efficiency_DoubleCentralJet90Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar_Double90Quad30_Efficiency_DoubleCentralJet90"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar_Double90Quad30_Efficiency_DoubleCentralJet90_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar_Double90Quad30_Efficiency_BTagCaloCSVp087TriplePair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar_Double90Quad30_Efficiency_BTagCaloCSVp087Triple"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar_Double90Quad30_Efficiency_BTagCaloCSVp087Triple_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar_Double90Quad30_Efficiency_QuadPFCentralJetLooseID30Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar_Double90Quad30_Efficiency_QuadPFCentralJetLooseID30"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar_Double90Quad30_Efficiency_QuadPFCentralJetLooseID30_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar_Double90Quad30_Efficiency_DoublePFCentralJetLooseID90Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar_Double90Quad30_Efficiency_DoublePFCentralJetLooseID90"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar_Double90Quad30_Efficiency_DoublePFCentralJetLooseID90_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar_Quad45_Efficiency_L1filterHTPair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar_Quad45_Efficiency_L1filterHT"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar_Quad45_Efficiency_L1filterHT_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar_Quad45_Efficiency_QuadCentralJet45Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar_Quad45_Efficiency_QuadCentralJet45"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar_Quad45_Efficiency_QuadCentralJet45_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar_Quad45_Efficiency_BTagCaloCSVp087TriplePair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar_Quad45_Efficiency_BTagCaloCSVp087Triple"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar_Quad45_Efficiency_BTagCaloCSVp087Triple_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar_Quad45_Efficiency_QuadPFCentralJetLooseID45Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar_Quad45_Efficiency_QuadPFCentralJetLooseID45"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar_Quad45_Efficiency_QuadPFCentralJetLooseID45_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar_And_Efficiency_L1filterQuad45HTPair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar_And_Efficiency_L1filterQuad45HT"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar_And_Efficiency_L1filterQuad45HT_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar_And_Efficiency_QuadCentralJet45Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar_And_Efficiency_QuadCentralJet45"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar_And_Efficiency_QuadCentralJet45_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar_And_Efficiency_QuadPFCentralJetLooseID45Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar_And_Efficiency_QuadPFCentralJetLooseID45"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar_And_Efficiency_QuadPFCentralJetLooseID45_FitResult")
    );


};
#include "TFile.h"
#include "TF1.h"
#include "TFitResult.h"
#include "TGraphErrors.h"
#include "Math/WrappedMultiTF1.h"

namespace TriggerFitCurves2017
{
    TFile triggerFitFile("TriggerEfficiency_Fit_2017.root");
    class KFitResult : public TFitResult
    {
    public:
        using TFitResult::TFitResult;
        KFitResult* ResetModelFunction(TF1* func){
            this->SetModelFunction(std::shared_ptr<IModelFunction>(dynamic_cast<IModelFunction*>(ROOT::Math::WrappedMultiTF1(*func).Clone())));
            return this;
        }
    };
    std::pair<TF1*,KFitResult*> createPair(TF1* theFunction, KFitResult* theFitResult )
    {
        theFitResult->ResetModelFunction(theFunction);
        return {theFunction, theFitResult};
    }

    std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_L1filterHTPair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon__Efficiency_L1filterHT"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon__Efficiency_L1filterHT_FitResult")
    );

    std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_QuadCentralJet30Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon__Efficiency_QuadCentralJet30"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon__Efficiency_QuadCentralJet30_FitResult")
    );

    std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_CaloQuadJet30HT300Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon__Efficiency_CaloQuadJet30HT300"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon__Efficiency_CaloQuadJet30HT300_FitResult")
    );

    std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_BTagCaloCSVp05DoublePair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon__Efficiency_BTagCaloCSVp05Double"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon__Efficiency_BTagCaloCSVp05Double_FitResult")
    );

    std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_PFCentralJetLooseIDQuad30Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon__Efficiency_PFCentralJetLooseIDQuad30"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon__Efficiency_PFCentralJetLooseIDQuad30_FitResult")
    );

    std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_1PFCentralJetLooseID75Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon__Efficiency_1PFCentralJetLooseID75"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon__Efficiency_1PFCentralJetLooseID75_FitResult")
    );

    std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_2PFCentralJetLooseID60Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon__Efficiency_2PFCentralJetLooseID60"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon__Efficiency_2PFCentralJetLooseID60_FitResult")
    );

    std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_3PFCentralJetLooseID45Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon__Efficiency_3PFCentralJetLooseID45"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon__Efficiency_3PFCentralJetLooseID45_FitResult")
    );

    std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_4PFCentralJetLooseID40Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon__Efficiency_4PFCentralJetLooseID40"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon__Efficiency_4PFCentralJetLooseID40_FitResult")
    );

    std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_PFCentralJetsLooseIDQuad30HT300Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon__Efficiency_PFCentralJetsLooseIDQuad30HT300"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon__Efficiency_PFCentralJetsLooseIDQuad30HT300_FitResult")
    );

    std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_BTagPFCSVp070TriplePair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon__Efficiency_BTagPFCSVp070Triple"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon__Efficiency_BTagPFCSVp070Triple_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar__Efficiency_L1filterHTPair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar__Efficiency_L1filterHT"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar__Efficiency_L1filterHT_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar__Efficiency_QuadCentralJet30Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar__Efficiency_QuadCentralJet30"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar__Efficiency_QuadCentralJet30_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar__Efficiency_CaloQuadJet30HT300Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar__Efficiency_CaloQuadJet30HT300"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar__Efficiency_CaloQuadJet30HT300_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar__Efficiency_BTagCaloCSVp05DoublePair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar__Efficiency_BTagCaloCSVp05Double"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar__Efficiency_BTagCaloCSVp05Double_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar__Efficiency_PFCentralJetLooseIDQuad30Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar__Efficiency_PFCentralJetLooseIDQuad30"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar__Efficiency_PFCentralJetLooseIDQuad30_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar__Efficiency_1PFCentralJetLooseID75Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar__Efficiency_1PFCentralJetLooseID75"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar__Efficiency_1PFCentralJetLooseID75_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar__Efficiency_2PFCentralJetLooseID60Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar__Efficiency_2PFCentralJetLooseID60"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar__Efficiency_2PFCentralJetLooseID60_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar__Efficiency_3PFCentralJetLooseID45Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar__Efficiency_3PFCentralJetLooseID45"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar__Efficiency_3PFCentralJetLooseID45_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar__Efficiency_4PFCentralJetLooseID40Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar__Efficiency_4PFCentralJetLooseID40"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar__Efficiency_4PFCentralJetLooseID40_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar__Efficiency_PFCentralJetsLooseIDQuad30HT300Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar__Efficiency_PFCentralJetsLooseIDQuad30HT300"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar__Efficiency_PFCentralJetsLooseIDQuad30HT300_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar__Efficiency_BTagPFCSVp070TriplePair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar__Efficiency_BTagPFCSVp070Triple"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar__Efficiency_BTagPFCSVp070Triple_FitResult")
    );


};
#include "TFile.h"
#include "TF1.h"
#include "TFitResult.h"
#include "TGraphErrors.h"
#include "Math/WrappedMultiTF1.h"

namespace TriggerFitCurves2018
{
    TFile triggerFitFile("TriggerEfficiency_Fit_2018.root");
    class KFitResult : public TFitResult
    {
    public:
        using TFitResult::TFitResult;
        KFitResult* ResetModelFunction(TF1* func){
            this->SetModelFunction(std::shared_ptr<IModelFunction>(dynamic_cast<IModelFunction*>(ROOT::Math::WrappedMultiTF1(*func).Clone())));
            return this;
        }
    };
    std::pair<TF1*,KFitResult*> createPair(TF1* theFunction, KFitResult* theFitResult )
    {
        theFitResult->ResetModelFunction(theFunction);
        return {theFunction, theFitResult};
    }

    std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_L1filterHTPair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon__Efficiency_L1filterHT"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon__Efficiency_L1filterHT_FitResult")
    );

    std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_QuadCentralJet30Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon__Efficiency_QuadCentralJet30"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon__Efficiency_QuadCentralJet30_FitResult")
    );

    std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_CaloQuadJet30HT320Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon__Efficiency_CaloQuadJet30HT320"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon__Efficiency_CaloQuadJet30HT320_FitResult")
    );

    std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_BTagCaloDeepCSVp17DoublePair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon__Efficiency_BTagCaloDeepCSVp17Double"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon__Efficiency_BTagCaloDeepCSVp17Double_FitResult")
    );

    std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_PFCentralJetLooseIDQuad30Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon__Efficiency_PFCentralJetLooseIDQuad30"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon__Efficiency_PFCentralJetLooseIDQuad30_FitResult")
    );

    std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_1PFCentralJetLooseID75Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon__Efficiency_1PFCentralJetLooseID75"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon__Efficiency_1PFCentralJetLooseID75_FitResult")
    );

    std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_2PFCentralJetLooseID60Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon__Efficiency_2PFCentralJetLooseID60"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon__Efficiency_2PFCentralJetLooseID60_FitResult")
    );

    std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_3PFCentralJetLooseID45Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon__Efficiency_3PFCentralJetLooseID45"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon__Efficiency_3PFCentralJetLooseID45_FitResult")
    );

    std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_4PFCentralJetLooseID40Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon__Efficiency_4PFCentralJetLooseID40"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon__Efficiency_4PFCentralJetLooseID40_FitResult")
    );

    std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_PFCentralJetsLooseIDQuad30HT330Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon__Efficiency_PFCentralJetsLooseIDQuad30HT330"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon__Efficiency_PFCentralJetsLooseIDQuad30HT330_FitResult")
    );

    std::pair<TF1*, KFitResult*> fSingleMuon__Efficiency_BTagPFDeepCSV4p5TriplePair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("SingleMuon__Efficiency_BTagPFDeepCSV4p5Triple"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("SingleMuon__Efficiency_BTagPFDeepCSV4p5Triple_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar__Efficiency_L1filterHTPair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar__Efficiency_L1filterHT"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar__Efficiency_L1filterHT_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar__Efficiency_QuadCentralJet30Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar__Efficiency_QuadCentralJet30"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar__Efficiency_QuadCentralJet30_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar__Efficiency_CaloQuadJet30HT320Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar__Efficiency_CaloQuadJet30HT320"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar__Efficiency_CaloQuadJet30HT320_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar__Efficiency_BTagCaloDeepCSVp17DoublePair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar__Efficiency_BTagCaloDeepCSVp17Double"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar__Efficiency_BTagCaloDeepCSVp17Double_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar__Efficiency_PFCentralJetLooseIDQuad30Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar__Efficiency_PFCentralJetLooseIDQuad30"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar__Efficiency_PFCentralJetLooseIDQuad30_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar__Efficiency_1PFCentralJetLooseID75Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar__Efficiency_1PFCentralJetLooseID75"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar__Efficiency_1PFCentralJetLooseID75_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar__Efficiency_2PFCentralJetLooseID60Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar__Efficiency_2PFCentralJetLooseID60"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar__Efficiency_2PFCentralJetLooseID60_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar__Efficiency_3PFCentralJetLooseID45Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar__Efficiency_3PFCentralJetLooseID45"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar__Efficiency_3PFCentralJetLooseID45_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar__Efficiency_4PFCentralJetLooseID40Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar__Efficiency_4PFCentralJetLooseID40"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar__Efficiency_4PFCentralJetLooseID40_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar__Efficiency_PFCentralJetsLooseIDQuad30HT330Pair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar__Efficiency_PFCentralJetsLooseIDQuad30HT330"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar__Efficiency_PFCentralJetsLooseIDQuad30HT330_FitResult")
    );

    std::pair<TF1*, KFitResult*> fTTbar__Efficiency_BTagPFDeepCSV4p5TriplePair = createPair(
        ((TGraphErrors*)triggerFitFile.Get("TTbar__Efficiency_BTagPFDeepCSV4p5Triple"))->GetFunction("cdf"),
        (KFitResult*)triggerFitFile.Get("TTbar__Efficiency_BTagPFDeepCSV4p5Triple_FitResult")
    );


};
