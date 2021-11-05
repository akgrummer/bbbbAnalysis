#include "Riostream.h"
#include "TH1D.h"
#include "TFile.h"
#include "TROOT.h"
#include "TCanvas.h"
#include <vector>
#include <map>
#include "TChain.h"
#include "TLegend.h"

std::string selectionThreeBtag = "NbJets == 3";
std::string selectionFourBtag = "NbJets >= 4";

std::string selectionbJetsPt          = "(H1_b1_pt > 30 && H1_b2_pt > 30 && H2_b1_pt > 30 && H2_b2_pt > 30)";
std::string selectionbJetsPtRegressed = "(H1_b1_ptRegressed > 30 && H1_b2_ptRegressed > 30 && H2_b1_ptRegressed > 30 && H2_b2_ptRegressed > 30)";
std::string selectionbJetsEta         = "(H1_b1_eta > -2.4 && H1_b1_eta < 2.4 && H1_b2_eta > -2.4 && H1_b2_eta < 2.4 && H2_b1_eta > -2.4 && H2_b1_eta < 2.4 && H2_b2_eta > -2.4 && H2_b2_eta < 2.4)";

std::string vetoIsoLeptons            = "(IsolatedElectron_pt<15 && IsolatedMuon_pt<10)";

std::string selectionbJets            = selectionbJetsPt + " && " + selectionbJetsPtRegressed + " && " + selectionbJetsEta + " && " + vetoIsoLeptons;

std::string blinded                   = "(H2_m > 125+20 || H2_m < 125-20)";
std::string validationRegion          = "((H1_m > 125-30 && H1_m < 125-20) || (H1_m > 125+20 && H1_m < 125+30))";
std::string kinFitCut                 = "(H1_kinFit_m > 124 && H1_kinFit_m < 126)";
std::string validationRegionBlinded   = validationRegion + " && " + blinded + " && " + kinFitCut;

std::string eventSelection             = selectionbJets + " && " + validationRegionBlinded;

std::string plotCut = "(HH_kinFit_m > 212 && HH_kinFit_m < 2320 && H2_m > 36 && H2_m < 2204)";

std::map<int, std::string> triggerSelectionMap;

float gRatioLowLimit  = 0.5;
float gRatioHighLimit = 1.5;

std::vector<std::string> splitByLine(const std::string& inputFileName)
{
    std::vector<std::string> fileNameList;
    std::ifstream fList (inputFileName);
    if (!fList.good())
    {
        std::cerr << "*** Sample::openFileAndTree : ERROR : could not open file " << inputFileName << std::endl;
        abort();
    }
    std::string line;
    while (std::getline(fList, line))
    {
        line = line.substr(0, line.find("#", 0)); // remove comments introduced by #
        while (line.find(" ") != std::string::npos) line = line.erase(line.find(" "), 1); // remove white spaces
        while (line.find("\n") != std::string::npos) line = line.erase(line.find("\n"), 1); // remove new line characters
        while (line.find("\r") != std::string::npos) line = line.erase(line.find("\r"), 1); // remove carriage return characters
        if (!line.empty()) fileNameList.emplace_back(line);
        break;
    }
    return fileNameList;
}

std::unique_ptr<TChain> getChainFromFileList(std::vector<std::string>& fileNameList, const std::string& treeName)
{
    std::unique_ptr<TChain> theChain = std::make_unique<TChain>(treeName.c_str());
    for(const auto& fileName : fileNameList) theChain->Add(fileName.c_str());

    return std::move(theChain);
}

std::string getSampleNameFromFile(std::string fileName)
{
    size_t end_pos = fileName.rfind('.');
    size_t start_pos = fileName.rfind('/')+1;
    return fileName.substr(start_pos, end_pos-start_pos);

}

std::pair<std::string, std::string> getMxMyFromSample(std::string sampleName)
{
    std::string mxStringStart = "_MX_";
    std::string mxStringEnd   = "_NANOAOD_";
    std::string myStringStart = "_MY_";
    size_t mxStart = sampleName.find(mxStringStart) + mxStringStart.size();
    size_t mxEnd   = sampleName.find(mxStringEnd);
    size_t myStart = sampleName.find(myStringStart) + myStringStart.size();
    size_t myEnd   = sampleName.size();

    std::string mx = sampleName.substr(mxStart, mxEnd-mxStart);
    std::string my = sampleName.substr(myStart, myEnd-myStart);

    return std::make_pair(mx, my);
}

void normalizeByBinSize(TH1D* inputPlot)
{
    for(int nBin = 1; nBin<=inputPlot->GetNbinsX(); ++nBin)
    {
        float binWidth = inputPlot->GetXaxis()->GetBinWidth(nBin);
        inputPlot->SetBinContent(nBin,inputPlot->GetBinContent(nBin)/binWidth);
        inputPlot->SetBinError(nBin,inputPlot->GetBinError(nBin)/binWidth);
    }
    return;

}
std::tuple<TH1D*, TH1D*> dividePlots(const TH1D* referencePlot, const TH1D* inputPlot)
{
    std::string ratioPlotName = std::string(inputPlot->GetName()) + "_ratio";
    std::string errorPlotName = ratioPlotName + "Error";
    int numberOfBins = inputPlot->GetNbinsX();
    TH1D* ratioPlot  = (TH1D*)inputPlot->Clone(ratioPlotName.data());
    TH1D* ratioError = (TH1D*)inputPlot->Clone(errorPlotName.data());
    for(int nBin = 1; nBin<=numberOfBins; ++nBin)
    {
        float referenceValue = referencePlot->GetBinContent(nBin);
        float referenceError = referencePlot->GetBinError  (nBin);
        if(referenceValue == 0.) 
        {
            referenceValue = 1.;
            referenceError = 1.;
        }
        ratioPlot->SetBinContent(nBin,inputPlot->GetBinContent(nBin)/referenceValue);
        ratioPlot->SetBinError  (nBin,inputPlot->GetBinError  (nBin)/referenceValue);
        ratioError->SetBinContent(nBin,1.);
        ratioError->SetBinError(nBin,referenceError/referenceValue);
    }

    ratioError->SetFillStyle(3002);
    ratioError->SetFillColor(kBlack);

    return {ratioPlot,ratioError};
}


std::tuple<TH1D*, TH1D*> splitErrorAndPlots(const TH1D* inputPlot)
{
    std::string valuePlotName = std::string(inputPlot->GetName()) + "_value";
    std::string errorPlotName = valuePlotName + "Error";
    int numberOfBins = inputPlot->GetNbinsX();
    TH1D* outputPlot  = (TH1D*)inputPlot->Clone(valuePlotName.data());
    TH1D* outputError = (TH1D*)inputPlot->Clone(errorPlotName.data());
    for(int nBin = 1; nBin<=numberOfBins; ++nBin)
    {
        outputPlot->SetBinError  (nBin,0.);
    }

    outputError->SetFillStyle(3002);
    outputError->SetFillColor(kBlack);

    return {outputPlot,outputError};
}


void RatioPlot(TVirtualPad *theCanvas, TH1D *referenceHistogram, std::vector<TH1D*> inputHistogramVector, std::vector<EColor> plotColorVector, bool normalize, float normalizeValue, float xMin=0, float xMax = 1500, int rebinNumber = 1, std::string xAxis = "", std::string yAxis = "", std::string title = "", std::string referencePlotName = "", std::vector<std::string> inputPlotNameVector = std::vector<std::string>(), bool normByBin = false)
{

    // std::cout<<normalize<<std::endl;
    // std::cout<<normalizeValue<<std::endl;

    if(inputPlotNameVector.size() == 0) inputPlotNameVector = std::vector<std::string>(plotColorVector.size(),"");
    assert(inputHistogramVector.size() == plotColorVector.size() == inputPlotNameVector.size());
    
    if(rebinNumber!=1)
    {
        referenceHistogram->Rebin(rebinNumber);
        for(auto inputHistogram : inputHistogramVector) inputHistogram->Rebin(rebinNumber);
    }
    referenceHistogram->SetAxisRange(xMin,xMax);
    for(auto inputHistogram : inputHistogramVector) inputHistogram->SetAxisRange(xMin,xMax);
    if(normalize){
        for(auto inputHistogram : inputHistogramVector) 
        {
            if(normalizeValue < 0.) 
                normalizeValue = float(referenceHistogram->Integral(-1,999999999))/float(inputHistogram->Integral(-1,999999999));
            std::cout<<normalizeValue<<std::endl;
            inputHistogram->Scale(normalizeValue);
        }
    }
    std::vector<std::tuple<TH1D*, TH1D*>> theRatioPlotList;
    for(auto inputHistogram : inputHistogramVector)
    {
        theRatioPlotList.emplace_back(dividePlots(referenceHistogram, inputHistogram));
    }
    // auto theRatioPlots = dividePlots(referenceHistogram, inputHistogramVector.at(0));
    if(normByBin)
    {
        normalizeByBinSize(referenceHistogram);
        for(auto inputHistogram : inputHistogramVector) 
        {
            normalizeByBinSize(inputHistogram);
        }
    }
    auto theLegend = new TLegend(0.3,0.75,0.88,0.88);
    theLegend->SetNColumns(3);
    theLegend->SetTextSize(0.05);


    // Upper plot will be in pad1
    TPad *pad1 = new TPad("pad1", "pad1", 0, 0.35, 1, 1.0);
    pad1->SetLeftMargin(0.12);
    pad1->SetBottomMargin(0); // Upper and lower plot are joined
    pad1->SetGridx();         // Vertical grid
    pad1->Draw();             // Draw the upper pad: pad1
    pad1->cd();               // pad1 becomes the current pad
    auto referenceHistAndError = splitErrorAndPlots(referenceHistogram);
    std::get<0>(referenceHistAndError)->Draw("hist");         // Draw referenceHistogram on top of inputHistogram
    theLegend->AddEntry(std::get<0>(referenceHistAndError),referencePlotName.data(), "pl");
    theLegend->AddEntry(std::get<1>(referenceHistAndError),(referencePlotName + " unc.").data(), "f");
    // Y axis inputHistogram plot settings
    std::get<0>(referenceHistAndError)->SetStats(0);          // No statistics on upper plot
    std::get<0>(referenceHistAndError)->GetYaxis()->SetTitleSize(0.07);
    std::get<0>(referenceHistAndError)->GetYaxis()->SetTitleFont(62);
    std::get<0>(referenceHistAndError)->GetYaxis()->SetTitleOffset(0.95);
    std::get<0>(referenceHistAndError)->GetYaxis()->SetLabelFont(62); // Absolute font size in pixel (precision 3)
    std::get<0>(referenceHistAndError)->GetYaxis()->SetLabelSize(0.06);
    std::get<0>(referenceHistAndError)->GetYaxis()->SetTitle(yAxis.data());
    std::get<0>(referenceHistAndError)->SetTitle(title.data());
    // std::get<0>(referenceHistAndError) settings
    std::get<0>(referenceHistAndError)->SetLineColor(kBlack);
    std::get<0>(referenceHistAndError)->SetMarkerColor(kBlack);
    std::get<0>(referenceHistAndError)->SetLineWidth(1);
    std::get<1>(referenceHistAndError)->Draw("same E2");         // Draw referenceHistogram on top of inputHistogram
    float yMaximum = std::get<0>(referenceHistAndError)->GetMaximum();


    for(uint hIt = 0; hIt <inputHistogramVector.size(); ++hIt)
    {
        TH1D* inputHistogram = inputHistogramVector.at(hIt);
        theLegend->AddEntry(inputHistogram,inputPlotNameVector[hIt].data(), "epl");
        inputHistogram->SetStats(0);          // No statistics on upper plot
        inputHistogram->SetTitle(title.data()); // Remove the ratio title
        inputHistogram->Draw("E same");               // Draw inputHistogram
        // inputHistogram settings
        assert(plotColorVector.at(hIt) != kBlack);
        inputHistogram->SetLineColor(plotColorVector.at(hIt));
        inputHistogram->SetMarkerColor(plotColorVector.at(hIt));
        inputHistogram->SetLineWidth(2);
        // if(yMaximum < inputHistogram->GetMaximum()) yMaximum = inputHistogram->GetMaximum();
    }
    if(std::string(inputHistogramVector.at(0)->GetName()).find("selectionbJets_ControlRegionAndSignalRegion") != std::string::npos) yMaximum = 18000;
    std::get<0>(referenceHistAndError)->SetMaximum(yMaximum * 1.3);
    // gROOT->ForceStyle();
    theLegend->Draw("");

    // lower plot will be in pad
    theCanvas->cd();          // Go back to the main canvas before defining pad2
    TPad *pad2 = new TPad("pad2", "pad2", 0, 0., 1, 0.35);
    pad2->SetTopMargin(0);
    pad2->SetBottomMargin(0.2);
    pad2->SetGridx(); // vertical grid
    pad2->SetGridy(); // horizontal grid
    pad2->Draw();
    pad2->SetLeftMargin(0.12);
    pad2->SetBottomMargin(0.3);
    pad2->cd();       // pad2 becomes the current pad

        // Define the ratio plot
    for(uint hIt = 0; hIt <inputHistogramVector.size(); ++hIt)
    {
        std::cout<<"Ratio plot number = " << hIt << std::endl;

        // TH1D *ratio = std::get<0>(theRatioPlots);
        // TH1D *ratioError = std::get<1>(theRatioPlots);
        TH1D *ratio      = std::get<0>(theRatioPlotList.at(hIt));
        // TH1D *ratio = (TH1D*)inputHistogramVector.at(hIt)->Clone("ratio");
        ratio->SetLineColor(plotColorVector.at(hIt));
        ratio->SetMarkerColor(plotColorVector.at(hIt));
        ratio->SetMinimum(gRatioLowLimit );  // Define Y ..
        ratio->SetMaximum(gRatioHighLimit); // .. range
        ratio->SetStats(0);      // No statistics on lower plot
        // ratio->Divide(referenceHistogram);
        ratio->SetMarkerStyle(21);
        ratio->SetMarkerSize(0.3);

        // Ratio plot (ratio) settings
        ratio->SetTitle(""); // Remove the ratio title

        if(hIt==0)
        {
            TH1D *ratioError = std::get<1>(theRatioPlotList.at(hIt));
            ratio->SetAxisRange(xMin,xMax);
            ratio->Draw("ep");       // Draw the ratio plot
            ratioError->Draw("same E2");
            // Y axis ratio plot settings
            ratio->GetYaxis()->SetTitle("ratio");
            ratio->GetYaxis()->SetNdivisions(505);
            ratio->GetYaxis()->SetTitleSize(0.1);
            ratio->GetYaxis()->SetTitleFont(62);
            ratio->GetYaxis()->SetTitleOffset(0.5);
            ratio->GetYaxis()->SetLabelFont(62); // Absolute font size in pixel (precision 3)
            ratio->GetYaxis()->SetLabelSize(0.1);

            // X axis ratio plot settings
            ratio->GetXaxis()->SetTitle(xAxis.data());
            ratio->GetXaxis()->SetTitleSize(0.15);
            ratio->GetXaxis()->SetTitleFont(62);
            ratio->GetXaxis()->SetTitleOffset(0.85);
            ratio->GetXaxis()->SetLabelFont(62); // Absolute font size in pixel (precision 3)
            ratio->GetXaxis()->SetLabelSize(0.13);
        }
        else
        {
            std::cout << "plotting second ratio" << hIt << std::endl;
            ratio->Draw("ep same");       // Draw the ratio plot
        }
    }

    theCanvas->cd();

}

TH1D* getVariableInValidationRegion(std::string fileName, std::string variable, std::string btagSelection, int year, std::pair<std::string, std::tuple<std::string, int, float, float>> cut, std::string weight = "")
{
    gROOT->SetBatch(true);
    std::vector<std::string> fileList     = splitByLine(fileName    );
    auto theTree     = getChainFromFileList(fileList    , "bbbbTree");

    auto sampleName = getSampleNameFromFile(fileName);
    auto pairMxMy   = getMxMyFromSample(sampleName);

    // std::string theCurrentSelection = cut;
    std::string theCurrentSelection = btagSelection;
    theCurrentSelection = theCurrentSelection + " && " + eventSelection + " && " + plotCut;
    theCurrentSelection = theCurrentSelection + " && " + triggerSelectionMap[year];
    if(std::get<0>(cut.second) != "") theCurrentSelection = theCurrentSelection + " && (" + std::get<0>(cut.second) + ")";
    if(weight != "") theCurrentSelection = weight +  " * (" + theCurrentSelection + ")";
    // std::cout << theCurrentSelection << std::endl;
    
    std::string xAxisLabel = "Distance from diagonal";

    std::string plotName = sampleName + "_Distance_" + cut.first + "_" + weight;
    TH1D *variablePlot = new TH1D(plotName.c_str(), ("m_{X} = " + pairMxMy.first + " GeV - m_{Y} = " + pairMxMy.second + " GeV; " + xAxisLabel + " [GeV]; entries [a.u.]" ).c_str()
        , std::get<1>(cut.second), std::get<2>(cut.second), std::get<3>(cut.second));
    variablePlot->GetYaxis()->SetTitleOffset(1.2);
    std::string plotMxKinFirCmd = variable + ">>" + plotName;
    theTree->Draw(plotMxKinFirCmd.c_str(), theCurrentSelection.data(), "same");
    variablePlot->SetLineColor(kBlue);
    variablePlot->SetMaximum(variablePlot->GetMaximum()*1.2);
    variablePlot->SetDirectory(0);
    gROOT->SetBatch(false);

    return variablePlot;
    
}


void plotComparison(int year, std::string variable, std::pair<std::string, std::tuple<std::string, int, float, float>> cut, bool useWeight)
{
    std::string weight = "";
    std::string bkgName = "3b-tag scaled";
    bool normalize = true;
    if(useWeight)
    {
        weight = "Weight_forBackground_PtRegressedAndHigherLevel_kinFit";
        normalize = false;
        bkgName = "BKG model";    
    }
    
    auto getFileName = [year]() -> std::string
    {
        if(year != 2018) return "plotterListFiles/" + std::to_string(year) + "Resonant_NMSSM_XYH_bbbb/FileList_BTagCSV_Data.txt";
        return "plotterListFiles/" + std::to_string(year) + "Resonant_NMSSM_XYH_bbbb/FileList_JetHT_Data.txt";
    };

    TH1D* variable3Btag = getVariableInValidationRegion(getFileName(), variable, selectionThreeBtag, year, cut, weight);
    TH1D* variable4Btag = getVariableInValidationRegion(getFileName(), variable, selectionFourBtag , year, cut        );

    std::string canvasName = "PlotComparison_year_" + std::to_string(year) + "_" + cut.first;
    TCanvas* theCanvasPlot = new TCanvas(canvasName.c_str(), canvasName.c_str(), 1400, 800);;

    std::string title = "Background comparison - Run " + std::to_string(year);
    RatioPlot(theCanvasPlot, variable4Btag, {variable3Btag}, {kRed}, normalize, 0., std::get<2>(cut.second), std::get<3>(cut.second), 1, "Distance from Diagonal [GeV]", "events", title, "4b-tag", {std::string(bkgName)});

    // variable4Btag->SetLineColor(kBlack);
    // variable4Btag->Draw("hist");
    // variable3Btag->SetLineColor(kRed);
    // variable3Btag->Draw("same");
    std::string outputFileName = canvasName + ".png"; 
    theCanvasPlot->SaveAs(outputFileName.c_str());
}

void plotAllVariableComparisons(int year, bool divideInRegions, bool useWeight)
{
    std::string variable = "(HH_kinFit_m - H2_m - 125.) / sqrt(2)";

    auto cutLine = [](int nBins, float mXmin, float mXmax) -> std::tuple<std::string, int, float, float>
    {
        std::string cutLine = "H2_m > (" + std::to_string(2.*mXmin - 125) + " - HH_kinFit_m) && H2_m < (" + std::to_string(2.*mXmax - 125) + " - HH_kinFit_m)";
        float xMin  = -10;
        float xMax  = (mXmax-125.)*sqrt(2);
        return std::make_tuple(cutLine, nBins, xMin, xMax);
    };

    std::map<std::string, std::tuple<std::string, int, float, float>> xMassCutList;
    if(divideInRegions)
    {
        xMassCutList["mX_0_400"]     = cutLine( 50,    0.,  400.); //"HH_kinFit_m >    0.  && HH_kinFit_m <  400.";
        xMassCutList["mX_400_700"]   = cutLine( 50,  400.,  700.); //"HH_kinFit_m >  400.  && HH_kinFit_m <  700.";
        xMassCutList["mX_700_1000"]  = cutLine( 50,  700., 1000.); //"HH_kinFit_m >  700.  && HH_kinFit_m < 1000.";
        xMassCutList["mX_1000_2000"] = cutLine( 50, 1000., 2000.); //"HH_kinFit_m > 1000.  && HH_kinFit_m < 2000.";
    }
    else xMassCutList["full"] = std::make_tuple<std::string, int, float, float>("", 150, -10., 2000.); //"HH_kinFit_m > 1000.  && HH_kinFit_m < 2000.";

    for(const auto& xMassCut : xMassCutList)
    {
        plotComparison(year, variable, xMassCut, useWeight);
    }
}

void plotAllComparisons(bool divideInRegions = false, bool useWeight = true)
{
    gROOT->SetBatch(true);
    triggerSelectionMap[2016] = "(( (HLT_DoubleJet90_Double30_TripleBTagCSV_p087_Fired==1 && HLT_DoubleJet90_Double30_TripleBTagCSV_p087_ObjectMatched>0) || (HLT_QuadJet45_TripleBTagCSV_p087_Fired==1 && HLT_QuadJet45_TripleBTagCSV_p087_ObjectMatched > 0) ))";
    triggerSelectionMap[2017] = "(( (HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0_Fired==1 && HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0_ObjectMatched>0) || (HLT_HT300PT30_QuadJet_75_60_45_40_TripeCSV_p07_Fired==1 && HLT_HT300PT30_QuadJet_75_60_45_40_TripeCSV_p07_ObjectMatched > 0) ))";
    triggerSelectionMap[2018] = "((HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5_Fired==1 && HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5_ObjectMatched>0))";

    std::vector<int> yearList {2016, 2017, 2018};

    for(const auto year : yearList) plotAllVariableComparisons(year, divideInRegions, useWeight);
    gROOT->SetBatch(false);

}






































#include "Riostream.h"
#include "TH1D.h"
#include "TFile.h"
#include "TROOT.h"
#include "TCanvas.h"
#include <vector>
#include <map>
#include "TChain.h"
#include "TLegend.h"

std::string selectionThreeBtag = "NbJets == 3";
std::string selectionFourBtag = "NbJets >= 4";

std::string selectionbJetsPt          = "(H1_b1_pt > 30 && H1_b2_pt > 30 && H2_b1_pt > 30 && H2_b2_pt > 30)";
std::string selectionbJetsPtRegressed = "(H1_b1_ptRegressed > 30 && H1_b2_ptRegressed > 30 && H2_b1_ptRegressed > 30 && H2_b2_ptRegressed > 30)";
std::string selectionbJetsEta         = "(H1_b1_eta > -2.4 && H1_b1_eta < 2.4 && H1_b2_eta > -2.4 && H1_b2_eta < 2.4 && H2_b1_eta > -2.4 && H2_b1_eta < 2.4 && H2_b2_eta > -2.4 && H2_b2_eta < 2.4)";

std::string vetoIsoLeptons            = "(IsolatedElectron_pt<15 && IsolatedMuon_pt<10)";

std::string selectionbJets            = selectionbJetsPt + " && " + selectionbJetsPtRegressed + " && " + selectionbJetsEta + " && " + vetoIsoLeptons;

std::string blinded                   = "(H2_m > 125+20 || H2_m < 125-20)";
std::string validationRegion          = "((H1_m > 125-30 && H1_m < 125-20) || (H1_m > 125+20 && H1_m < 125+30))";
std::string kinFitCut                 = "(H1_kinFit_m > 124 && H1_kinFit_m < 126)";
std::string validationRegionBlinded   = validationRegion + " && " + blinded + " && " + kinFitCut;

std::string eventSelection             = selectionbJets + " && " + validationRegionBlinded;

std::map<int, std::string> triggerSelectionMap;

float gRatioLowLimit  = 0.5;
float gRatioHighLimit = 1.5;

std::vector<std::string> splitByLine(const std::string& inputFileName)
{
    std::vector<std::string> fileNameList;
    std::ifstream fList (inputFileName);
    if (!fList.good())
    {
        std::cerr << "*** Sample::openFileAndTree : ERROR : could not open file " << inputFileName << std::endl;
        abort();
    }
    std::string line;
    while (std::getline(fList, line))
    {
        line = line.substr(0, line.find("#", 0)); // remove comments introduced by #
        while (line.find(" ") != std::string::npos) line = line.erase(line.find(" "), 1); // remove white spaces
        while (line.find("\n") != std::string::npos) line = line.erase(line.find("\n"), 1); // remove new line characters
        while (line.find("\r") != std::string::npos) line = line.erase(line.find("\r"), 1); // remove carriage return characters
        if (!line.empty()) fileNameList.emplace_back(line);
        // break;
    }
    return fileNameList;
}

std::unique_ptr<TChain> getChainFromFileList(std::vector<std::string>& fileNameList, const std::string& treeName)
{
    std::unique_ptr<TChain> theChain = std::make_unique<TChain>(treeName.c_str());
    for(const auto& fileName : fileNameList) theChain->Add(fileName.c_str());

    return std::move(theChain);
}

std::string getSampleNameFromFile(std::string fileName)
{
    size_t end_pos = fileName.rfind('.');
    size_t start_pos = fileName.rfind('/')+1;
    return fileName.substr(start_pos, end_pos-start_pos);

}

std::pair<std::string, std::string> getMxMyFromSample(std::string sampleName)
{
    std::string mxStringStart = "_MX_";
    std::string mxStringEnd   = "_NANOAOD_";
    std::string myStringStart = "_MY_";
    size_t mxStart = sampleName.find(mxStringStart) + mxStringStart.size();
    size_t mxEnd   = sampleName.find(mxStringEnd);
    size_t myStart = sampleName.find(myStringStart) + myStringStart.size();
    size_t myEnd   = sampleName.size();

    std::string mx = sampleName.substr(mxStart, mxEnd-mxStart);
    std::string my = sampleName.substr(myStart, myEnd-myStart);

    return std::make_pair(mx, my);
}

void normalizeByBinSize(TH1D* inputPlot)
{
    for(int nBin = 1; nBin<=inputPlot->GetNbinsX(); ++nBin)
    {
        float binWidth = inputPlot->GetXaxis()->GetBinWidth(nBin);
        inputPlot->SetBinContent(nBin,inputPlot->GetBinContent(nBin)/binWidth);
        inputPlot->SetBinError(nBin,inputPlot->GetBinError(nBin)/binWidth);
    }
    return;

}
std::tuple<TH1D*, TH1D*> dividePlots(const TH1D* referencePlot, const TH1D* inputPlot)
{
    std::string ratioPlotName = std::string(inputPlot->GetName()) + "_ratio";
    std::string errorPlotName = ratioPlotName + "Error";
    int numberOfBins = inputPlot->GetNbinsX();
    TH1D* ratioPlot  = (TH1D*)inputPlot->Clone(ratioPlotName.data());
    TH1D* ratioError = (TH1D*)inputPlot->Clone(errorPlotName.data());
    for(int nBin = 1; nBin<=numberOfBins; ++nBin)
    {
        float referenceValue = referencePlot->GetBinContent(nBin);
        float referenceError = referencePlot->GetBinError  (nBin);
        if(referenceValue == 0.) 
        {
            referenceValue = 1.;
            referenceError = 1.;
        }
        ratioPlot->SetBinContent(nBin,inputPlot->GetBinContent(nBin)/referenceValue);
        ratioPlot->SetBinError  (nBin,inputPlot->GetBinError  (nBin)/referenceValue);
        ratioError->SetBinContent(nBin,1.);
        ratioError->SetBinError(nBin,referenceError/referenceValue);
    }

    ratioError->SetFillStyle(3002);
    ratioError->SetFillColor(kBlack);

    return {ratioPlot,ratioError};
}


std::tuple<TH1D*, TH1D*> splitErrorAndPlots(const TH1D* inputPlot)
{
    std::string valuePlotName = std::string(inputPlot->GetName()) + "_value";
    std::string errorPlotName = valuePlotName + "Error";
    int numberOfBins = inputPlot->GetNbinsX();
    TH1D* outputPlot  = (TH1D*)inputPlot->Clone(valuePlotName.data());
    TH1D* outputError = (TH1D*)inputPlot->Clone(errorPlotName.data());
    for(int nBin = 1; nBin<=numberOfBins; ++nBin)
    {
        outputPlot->SetBinError  (nBin,0.);
    }

    outputError->SetFillStyle(3002);
    outputError->SetFillColor(kBlack);

    return {outputPlot,outputError};
}


void RatioPlot(TVirtualPad *theCanvas, TH1D *referenceHistogram, std::vector<TH1D*> inputHistogramVector, std::vector<EColor> plotColorVector, bool normalize, float normalizeValue, float xMin=0, float xMax = 1500, int rebinNumber = 1, std::string xAxis = "", std::string yAxis = "", std::string title = "", std::string referencePlotName = "", std::vector<std::string> inputPlotNameVector = std::vector<std::string>(), bool normByBin = false)
{

    // std::cout<<normalize<<std::endl;
    // std::cout<<normalizeValue<<std::endl;

    if(inputPlotNameVector.size() == 0) inputPlotNameVector = std::vector<std::string>(plotColorVector.size(),"");
    assert(inputHistogramVector.size() == plotColorVector.size() == inputPlotNameVector.size());
    
    if(rebinNumber!=1)
    {
        referenceHistogram->Rebin(rebinNumber);
        for(auto inputHistogram : inputHistogramVector) inputHistogram->Rebin(rebinNumber);
    }
    referenceHistogram->SetAxisRange(xMin,xMax);
    for(auto inputHistogram : inputHistogramVector) inputHistogram->SetAxisRange(xMin,xMax);
    if(normalize){
        for(auto inputHistogram : inputHistogramVector) 
        {
            if(normalizeValue < 0.) 
                normalizeValue = float(referenceHistogram->Integral(-1,999999999))/float(inputHistogram->Integral(-1,999999999));
            std::cout<<normalizeValue<<std::endl;
            inputHistogram->Scale(normalizeValue);
        }
    }
    std::vector<std::tuple<TH1D*, TH1D*>> theRatioPlotList;
    for(auto inputHistogram : inputHistogramVector)
    {
        theRatioPlotList.emplace_back(dividePlots(referenceHistogram, inputHistogram));
    }
    // auto theRatioPlots = dividePlots(referenceHistogram, inputHistogramVector.at(0));
    if(normByBin)
    {
        normalizeByBinSize(referenceHistogram);
        for(auto inputHistogram : inputHistogramVector) 
        {
            normalizeByBinSize(inputHistogram);
        }
    }
    auto theLegend = new TLegend(0.3,0.75,0.88,0.88);
    theLegend->SetNColumns(3);
    theLegend->SetTextSize(0.05);


    // Upper plot will be in pad1
    TPad *pad1 = new TPad("pad1", "pad1", 0, 0.35, 1, 1.0);
    pad1->SetLeftMargin(0.12);
    pad1->SetBottomMargin(0); // Upper and lower plot are joined
    pad1->SetGridx();         // Vertical grid
    pad1->Draw();             // Draw the upper pad: pad1
    pad1->cd();               // pad1 becomes the current pad
    auto referenceHistAndError = splitErrorAndPlots(referenceHistogram);
    std::get<0>(referenceHistAndError)->Draw("hist");         // Draw referenceHistogram on top of inputHistogram
    theLegend->AddEntry(std::get<0>(referenceHistAndError),referencePlotName.data(), "pl");
    theLegend->AddEntry(std::get<1>(referenceHistAndError),(referencePlotName + " unc.").data(), "f");
    // Y axis inputHistogram plot settings
    std::get<0>(referenceHistAndError)->SetStats(0);          // No statistics on upper plot
    std::get<0>(referenceHistAndError)->GetYaxis()->SetTitleSize(0.07);
    std::get<0>(referenceHistAndError)->GetYaxis()->SetTitleFont(62);
    std::get<0>(referenceHistAndError)->GetYaxis()->SetTitleOffset(0.95);
    std::get<0>(referenceHistAndError)->GetYaxis()->SetLabelFont(62); // Absolute font size in pixel (precision 3)
    std::get<0>(referenceHistAndError)->GetYaxis()->SetLabelSize(0.06);
    std::get<0>(referenceHistAndError)->GetYaxis()->SetTitle(yAxis.data());
    std::get<0>(referenceHistAndError)->SetTitle(title.data());
    // std::get<0>(referenceHistAndError) settings
    std::get<0>(referenceHistAndError)->SetLineColor(kBlack);
    std::get<0>(referenceHistAndError)->SetMarkerColor(kBlack);
    std::get<0>(referenceHistAndError)->SetLineWidth(1);
    std::get<1>(referenceHistAndError)->Draw("same E2");         // Draw referenceHistogram on top of inputHistogram
    float yMaximum = std::get<0>(referenceHistAndError)->GetMaximum();


    for(uint hIt = 0; hIt <inputHistogramVector.size(); ++hIt)
    {
        TH1D* inputHistogram = inputHistogramVector.at(hIt);
        theLegend->AddEntry(inputHistogram,inputPlotNameVector[hIt].data(), "epl");
        inputHistogram->SetStats(0);          // No statistics on upper plot
        inputHistogram->SetTitle(title.data()); // Remove the ratio title
        inputHistogram->Draw("E same");               // Draw inputHistogram
        // inputHistogram settings
        assert(plotColorVector.at(hIt) != kBlack);
        inputHistogram->SetLineColor(plotColorVector.at(hIt));
        inputHistogram->SetMarkerColor(plotColorVector.at(hIt));
        inputHistogram->SetLineWidth(2);
        // if(yMaximum < inputHistogram->GetMaximum()) yMaximum = inputHistogram->GetMaximum();
    }
    if(std::string(inputHistogramVector.at(0)->GetName()).find("selectionbJets_ControlRegionAndSignalRegion") != std::string::npos) yMaximum = 18000;
    std::get<0>(referenceHistAndError)->SetMaximum(yMaximum * 1.3);
    // gROOT->ForceStyle();
    theLegend->Draw("");

    // lower plot will be in pad
    theCanvas->cd();          // Go back to the main canvas before defining pad2
    TPad *pad2 = new TPad("pad2", "pad2", 0, 0., 1, 0.35);
    pad2->SetTopMargin(0);
    pad2->SetBottomMargin(0.2);
    pad2->SetGridx(); // vertical grid
    pad2->SetGridy(); // horizontal grid
    pad2->Draw();
    pad2->SetLeftMargin(0.12);
    pad2->SetBottomMargin(0.3);
    pad2->cd();       // pad2 becomes the current pad

        // Define the ratio plot
    for(uint hIt = 0; hIt <inputHistogramVector.size(); ++hIt)
    {
        std::cout<<"Ratio plot number = " << hIt << std::endl;

        // TH1D *ratio = std::get<0>(theRatioPlots);
        // TH1D *ratioError = std::get<1>(theRatioPlots);
        TH1D *ratio      = std::get<0>(theRatioPlotList.at(hIt));
        // TH1D *ratio = (TH1D*)inputHistogramVector.at(hIt)->Clone("ratio");
        ratio->SetLineColor(plotColorVector.at(hIt));
        ratio->SetMarkerColor(plotColorVector.at(hIt));
        ratio->SetMinimum(gRatioLowLimit );  // Define Y ..
        ratio->SetMaximum(gRatioHighLimit); // .. range
        ratio->SetStats(0);      // No statistics on lower plot
        // ratio->Divide(referenceHistogram);
        ratio->SetMarkerStyle(21);
        ratio->SetMarkerSize(0.3);

        // Ratio plot (ratio) settings
        ratio->SetTitle(""); // Remove the ratio title

        if(hIt==0)
        {
            TH1D *ratioError = std::get<1>(theRatioPlotList.at(hIt));
            ratio->SetAxisRange(xMin,xMax);
            ratio->Draw("ep");       // Draw the ratio plot
            ratioError->Draw("same E2");
            // Y axis ratio plot settings
            ratio->GetYaxis()->SetTitle("ratio");
            ratio->GetYaxis()->SetNdivisions(505);
            ratio->GetYaxis()->SetTitleSize(0.1);
            ratio->GetYaxis()->SetTitleFont(62);
            ratio->GetYaxis()->SetTitleOffset(0.5);
            ratio->GetYaxis()->SetLabelFont(62); // Absolute font size in pixel (precision 3)
            ratio->GetYaxis()->SetLabelSize(0.1);

            // X axis ratio plot settings
            ratio->GetXaxis()->SetTitle(xAxis.data());
            ratio->GetXaxis()->SetTitleSize(0.15);
            ratio->GetXaxis()->SetTitleFont(62);
            ratio->GetXaxis()->SetTitleOffset(0.85);
            ratio->GetXaxis()->SetLabelFont(62); // Absolute font size in pixel (precision 3)
            ratio->GetXaxis()->SetLabelSize(0.13);
        }
        else
        {
            std::cout << "plotting second ratio" << hIt << std::endl;
            ratio->Draw("ep same");       // Draw the ratio plot
        }
    }

    theCanvas->cd();

}

TH1D* getVariableInValidationRegion(std::string fileName, std::string variable, std::string btagSelection, int year, std::pair<std::string, std::tuple<std::string, int, float, float>> cut, std::string weight = "")
{
    gROOT->SetBatch(true);
    std::vector<std::string> fileList     = splitByLine(fileName    );
    auto theTree     = getChainFromFileList(fileList    , "bbbbTree");

    auto sampleName = getSampleNameFromFile(fileName);
    auto pairMxMy   = getMxMyFromSample(sampleName);

    // std::string theCurrentSelection = cut;
    std::string theCurrentSelection = btagSelection;
    theCurrentSelection = theCurrentSelection + " && " + eventSelection;
    theCurrentSelection = theCurrentSelection + " && " + triggerSelectionMap[year];
    if(std::get<0>(cut.second) != "") theCurrentSelection = theCurrentSelection + " && (" + std::get<0>(cut.second) + ")";
    if(weight != "") theCurrentSelection = weight +  " * (" + theCurrentSelection + ")";
    // std::cout << theCurrentSelection << std::endl;
    
    std::string xAxisLabel = "Distance from diagonal";

    std::string plotName = sampleName + "_Distance_" + cut.first + "_" + weight;
    TH1D *variablePlot = new TH1D(plotName.c_str(), ("m_{X} = " + pairMxMy.first + " GeV - m_{Y} = " + pairMxMy.second + " GeV; " + xAxisLabel + " [GeV]; entries [a.u.]" ).c_str()
        , std::get<1>(cut.second), std::get<2>(cut.second), std::get<3>(cut.second));
    variablePlot->GetYaxis()->SetTitleOffset(1.2);
    std::string plotMxKinFirCmd = variable + ">>" + plotName;
    theTree->Draw(plotMxKinFirCmd.c_str(), theCurrentSelection.data(), "same");
    variablePlot->SetLineColor(kBlue);
    variablePlot->SetMaximum(variablePlot->GetMaximum()*1.2);
    variablePlot->SetDirectory(0);
    gROOT->SetBatch(false);

    return variablePlot;
    
}


void plotComparison(int year, std::string variable, std::pair<std::string, std::tuple<std::string, int, float, float>> cut)
{
    std::string weight   = "Weight_forBackground_PtRegressedAndHigherLevel_kinFit";
    
    auto getFileName = [year]() -> std::string
    {
        if(year != 2018) return "plotterListFiles/" + std::to_string(year) + "Resonant_NMSSM_XYH_bbbb/FileList_BTagCSV_Data.txt";
        return "plotterListFiles/" + std::to_string(year) + "Resonant_NMSSM_XYH_bbbb/FileList_JetHT_Data.txt";
    };

    TH1D* variable3Btag = getVariableInValidationRegion(getFileName(), variable, selectionThreeBtag, year, cut, weight);
    TH1D* variable4Btag = getVariableInValidationRegion(getFileName(), variable, selectionFourBtag , year, cut        );

    std::string canvasName = "PlotComparison_year_" + std::to_string(year) + "_" + cut.first;
    TCanvas* theCanvasPlot = new TCanvas(canvasName.c_str(), canvasName.c_str(), 1400, 800);;

    std::string title = "Background comparison - Run " + std::to_string(year);
    RatioPlot(theCanvasPlot, variable4Btag, {variable3Btag}, {kRed}, false, 0., std::get<2>(cut.second), std::get<3>(cut.second), 1, "Distance from Diagonal [GeV]", "events", title, "4b-tag", {std::string("3b-tag scaled")});

    // variable4Btag->SetLineColor(kBlack);
    // variable4Btag->Draw("hist");
    // variable3Btag->SetLineColor(kRed);
    // variable3Btag->Draw("same");
    std::string outputFileName = canvasName + ".png"; 
    theCanvasPlot->SaveAs(outputFileName.c_str());
}

void plotAllVariableComparisons(int year)
{
    std::string variable = "(HH_kinFit_m - H2_m - 125.) / sqrt(2)";


    auto cutLine = [](int nBins, float mXmin, float mXmax) -> std::tuple<std::string, int, float, float>
    {
        std::string cutLine = "H2_m > (" + std::to_string(2.*mXmin - 125) + " - HH_kinFit_m) && H2_m < (" + std::to_string(2.*mXmax - 125) + " - HH_kinFit_m)";
        float xMin  = -10;
        float xMax  = (mXmax-125.)*sqrt(2);
        return std::make_tuple(cutLine, nBins, xMin, xMax);
    };

    std::map<std::string, std::tuple<std::string, int, float, float>> xMassCutList;
    xMassCutList["mX_0_400"]     = cutLine( 50.,    0.,  400.); //"HH_kinFit_m >    0.  && HH_kinFit_m <  400.";
    xMassCutList["mX_400_700"]   = cutLine( 50.,  400.,  700.); //"HH_kinFit_m >  400.  && HH_kinFit_m <  700.";
    xMassCutList["mX_700_1000"]  = cutLine( 50.,  700., 1000.); //"HH_kinFit_m >  700.  && HH_kinFit_m < 1000.";
    xMassCutList["mX_1000_2000"] = cutLine( 50., 1000., 2000.); //"HH_kinFit_m > 1000.  && HH_kinFit_m < 2000.";

    for(const auto& xMassCut : xMassCutList)
    {
        plotComparison(year, variable, xMassCut);
    }
}

void plotAllComparisons()
{
    gROOT->SetBatch(true);
    triggerSelectionMap[2016] = "(( (HLT_DoubleJet90_Double30_TripleBTagCSV_p087_Fired==1 && HLT_DoubleJet90_Double30_TripleBTagCSV_p087_ObjectMatched>0) || (HLT_QuadJet45_TripleBTagCSV_p087_Fired==1 && HLT_QuadJet45_TripleBTagCSV_p087_ObjectMatched > 0) ))";
    triggerSelectionMap[2017] = "(( (HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0_Fired==1 && HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0_ObjectMatched>0) || (HLT_HT300PT30_QuadJet_75_60_45_40_TripeCSV_p07_Fired==1 && HLT_HT300PT30_QuadJet_75_60_45_40_TripeCSV_p07_ObjectMatched > 0) ))";
    triggerSelectionMap[2018] = "((HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5_Fired==1 && HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5_ObjectMatched>0))";

    std::vector<int> yearList {2016, 2017, 2018};

    for(const auto year : yearList) plotAllVariableComparisons(year);
    gROOT->SetBatch(false);

}
