#include "Riostream.h"
#include "TFile.h"
#include "THStack.h"
#include "TH1F.h"
#include "TCanvas.h"
#include "TROOT.h"
#include "TLegend.h"
#include "TList.h"
#include <algorithm>
// #include <filesystem>

#define NO_PLOT "null"

// int rebinValue = 4;

// bool CreateDirectoryRecursive(std::string const & dirName, std::error_code & err)
// {
//     err.clear();
//     if (!std::filesystem::create_directories(dirName, err))
//     {
//         if (std::filesystem::exists(dirName))
//         {
//             // The folder already exists:
//             err.clear();
//             return true;
//         }
//         return false;
//     }
//     return true;
// }

template<typename THA, typename THB>
std::tuple<TH1F*, TH1F*> dividePlots(const THA* referencePlot, const THB* inputPlot)
{
    std::string ratioPlotName = std::string(inputPlot->GetName()) + "_ratio";
    std::string errorPlotName = ratioPlotName + "Error";
    int numberOfBins = inputPlot->GetNbinsX();
    TH1F* ratioPlot  = (TH1F*)inputPlot->Clone(ratioPlotName.data());
    TH1F* ratioError = (TH1F*)inputPlot->Clone(errorPlotName.data());
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
    ratioError->SetMarkerSize(0.);

    return {ratioPlot,ratioError};
}

std::tuple<TH1F*, TH1F*> splitErrorAndPlots(const THStack* inputStack)
{
    std::string valuePlotName = std::string(inputStack->GetName()) + "_value";
    std::string errorPlotName = valuePlotName + "Error";
    auto histogramList = inputStack->GetHists();
    const TH1F* theFirstPlot = (TH1F*)histogramList->At(0);

    int numberOfBins = theFirstPlot->GetNbinsX();
    TH1F* outputPlot  = (TH1F*)theFirstPlot->Clone(valuePlotName.data());
    outputPlot->SetDirectory(0);
    TH1F* outputError = (TH1F*)theFirstPlot->Clone(errorPlotName.data());
    outputError->SetDirectory(0);
    for(int nHist=0; nHist<histogramList->GetSize(); ++nHist)
    {
        TH1F* inputPlot = (TH1F*)histogramList->At(nHist);
        for(int nBin = 1; nBin<=numberOfBins; ++nBin)
        {
            if(nHist == 0)
            {
                outputPlot->SetBinError  (nBin,0.);
                outputPlot->SetBinContent (nBin,0.);
                outputError->SetBinError (nBin,0.);
                outputError->SetBinContent (nBin,0.);
            }
            outputPlot ->SetBinContent(nBin, outputPlot->GetBinContent(nBin) + inputPlot->GetBinContent(nBin) );
            outputError->SetBinContent(nBin, outputError->GetBinContent(nBin) + inputPlot->GetBinContent(nBin) );
            outputError->SetBinError  (nBin, sqrt(outputError->GetBinError(nBin)*outputError->GetBinError(nBin) + inputPlot->GetBinError(nBin)*inputPlot->GetBinError(nBin) ));
        }
    }

    outputError->SetFillStyle(3002);
    outputError->SetFillColor(kBlack);

    return {outputPlot,outputError};
}

template<typename TH>
void normalizeByBinSize1D(TH* inputPlot)
{
    for(int nBin = 1; nBin<=inputPlot->GetNbinsX(); ++nBin)
    {
        float binWidth = inputPlot->GetXaxis()->GetBinWidth(nBin);
        inputPlot->SetBinContent(nBin,inputPlot->GetBinContent(nBin)/binWidth);
        inputPlot->SetBinError(nBin,inputPlot->GetBinError(nBin)/binWidth);
    }
    return;

}


void StackPlot(TVirtualPad *theCanvas, TFile* inputFile, TFile* inputFile1, TFile* inputFile2, const std::string& selectionAndRegion, const std::string& variableName, const std::vector<std::string>& datasetList, const std::vector<std::string>& datasetNameList, std::vector<Int_t> colorList, const std::string& modelDataset, const std::string& modelName, const std::vector<std::string>& signalDatasetList, const std::string& signalName, std::string dataDataset, std::string dataName, bool normalizeBinByBin, const std::string& xAxisName, const std::string& yAxisName, const int year, const TString mYlabel, const TString sample)
{
    gPad->SetTickx();
    gPad->SetTicky();

    double totalIntegral = 0.;
    double totalIntegralError = 0.;
    double qcdIntegral   = 0.;
    double qcdIntegralError = 0.;
    double ttbarIntegral = 0.;
    double ttbarIntegralError = 0.;

    std::vector<TH1F*> plotList;

    auto theLegend = new TLegend(0.45,0.75,0.88,0.88);
    theLegend->SetNColumns(3);
    theLegend->SetTextSize(0.04);
    theLegend->SetBorderSize(0);
    auto theSignalLegend = new TLegend(0.45,0.5,0.88,0.6);
    theSignalLegend->SetTextSize(0.04);

    std::vector<std::tuple<TH1F*, const char*, const char*>> legendList;

    std::cout<<"datasetName"<<" "<< "Integral"<< " "<< "Error"<< std::endl;
    double theCurrentError = 0;
    double theCurrentIntegral = 0;
    std::string datasetNameSpecial= "";
    std::string plotName = "";
    TH1F* datasetPlot;
    TH1F* datasetPlot2;

    datasetNameSpecial= "data_BTagCSV_dataDriven_kinFit";
    plotName = datasetNameSpecial + "/" + selectionAndRegion + "/" + datasetNameSpecial + "_" + selectionAndRegion + "_" + variableName;
    datasetPlot = (TH1F*)inputFile->Get( plotName.data() );
    theCurrentIntegral = datasetPlot->IntegralAndError(-1,999999999, theCurrentError);
    std::cout<<datasetNameSpecial <<" "<< theCurrentIntegral<< " "<< theCurrentError<< std::endl;

    datasetNameSpecial= "data_BTagCSV";
    plotName = datasetNameSpecial + "/" + selectionAndRegion + "/" + datasetNameSpecial + "_" + selectionAndRegion + "_" + variableName;
    datasetPlot = (TH1F*)inputFile->Get( plotName.data() );
    theCurrentIntegral = datasetPlot->IntegralAndError(-1,999999999, theCurrentError);
    std::cout<<datasetNameSpecial <<" "<< theCurrentIntegral<< " "<< theCurrentError<< std::endl;

    // gStyle->SetPalette(kPastel);
    for(size_t dIt=0; dIt<datasetList.size(); ++dIt)
    {
        const std::string &datasetName = datasetList[dIt];
        plotName = datasetName + "/" + selectionAndRegion + "/" + datasetName + "_" + selectionAndRegion + "_" + variableName;
        if(datasetName == "Zjets"){
            if(year==2016){
                datasetPlot2 = (TH1F*)inputFile2->Get( plotName.data() );
                datasetPlot2->SetNameTitle("ZjetspreVFP", "ZjetspreVFPTitle");
            }
            datasetPlot = (TH1F*)inputFile1->Get( plotName.data() );
            if(year==2016) datasetPlot->Add(datasetPlot2);
        }
        else datasetPlot = (TH1F*)inputFile->Get( plotName.data() );
        if(datasetPlot == nullptr) std::cout<<"Plot "<< plotName << " does not exist" <<std::endl;
        datasetPlot->SetDirectory(0);
        // datasetPlot->Rebin(rebinValue);
        datasetPlot->SetFillColor(colorList[dIt]);
        // datasetPlot->SetFillStyle(3002);
        datasetPlot->SetNameTitle(datasetName.data(), datasetName.data());
        plotList.emplace_back(datasetPlot);
        if(datasetName == "ttbar") ttbarIntegral = datasetPlot->IntegralAndError(-1,999999999,ttbarIntegralError);
        if(datasetName == "QCD")   qcdIntegral   = datasetPlot->IntegralAndError(-1,999999999,qcdIntegralError);
        theCurrentError = 0;
        theCurrentIntegral = 0;
        theCurrentIntegral = datasetPlot->IntegralAndError(-1,999999999,theCurrentError);
        totalIntegral += theCurrentIntegral;
        totalIntegralError = sqrt(totalIntegralError*totalIntegralError + theCurrentError*theCurrentError);
        std::cout<<datasetName<<" "<< theCurrentIntegral<< " "<< theCurrentError<< std::endl;
    }
    std::cout << "QCD   BKG ratio = " << qcdIntegral/totalIntegral*100.   << " +- " << qcdIntegral/totalIntegral*100.   *sqrt(totalIntegralError*totalIntegralError/(totalIntegral*totalIntegral) + qcdIntegralError*qcdIntegralError/(qcdIntegral*qcdIntegral) )         << " \%"<<std::endl;
    std::cout << "ttbar BKG ratio = " << ttbarIntegral/totalIntegral*100. << " +- " << ttbarIntegral/totalIntegral*100. *sqrt(totalIntegralError*totalIntegralError/(totalIntegral*totalIntegral) + ttbarIntegralError*ttbarIntegralError/(ttbarIntegral*ttbarIntegral) ) << " \%"<<std::endl;

    // std::stable_sort(plotList.begin(), plotList.end(), [](const TH1F* aPlot, const TH1F* bPlot) -> bool
    //     {return aPlot->Integral() < bPlot->Integral();}
    // );

    theCanvas->cd();
        // Upper plot will be in pad1
    // TPad *pad1 = new TPad("pad1", "pad1", 0, 0.25, 1, 1.0);
    // pad1->SetLeftMargin(0.12);
    // pad1->SetBottomMargin(0); // Upper and lower plot are joined
    // pad1->SetGridx();         // Vertical grid
    // pad1->Draw();             // Draw the upper pad: pad1
    // pad1->cd();               // pad1 becomes the current pad


    THStack * theBackgroundStack = new THStack(variableName.data(), variableName.data());
    for(auto & plot : plotList)
    {
        legendList.insert(legendList.begin(), {plot, plot->GetName(), "f"});
        if(normalizeBinByBin) normalizeByBinSize1D(plot);
        theBackgroundStack->Add(plot);
    }
    theBackgroundStack->Draw("HIST");
    theBackgroundStack->SetTitle("");
    theBackgroundStack->GetXaxis()->SetTitle(xAxisName.data());
    theBackgroundStack->GetYaxis()->SetTitle(yAxisName.data());
    theBackgroundStack->GetYaxis()->SetTitleSize(0.06);
    theBackgroundStack->GetYaxis()->SetTitleFont(62);
    theBackgroundStack->GetYaxis()->SetTitleOffset(0.7);
    theBackgroundStack->GetYaxis()->SetLabelFont(62); // Absolute font size in pixel (precision 3)
    theBackgroundStack->GetYaxis()->SetLabelSize(0.055);

    std::tuple<TH1F*, TH1F*> backgroundAndError  = splitErrorAndPlots(theBackgroundStack);
    std::get<1>(backgroundAndError)->Draw("same e2");

    float theMaxY = theBackgroundStack->GetMaximum();

    plotName = modelDataset + "/" + selectionAndRegion + "/" + modelDataset + "_" + selectionAndRegion + "_" + variableName;
    TH1F* bkgModelPlot = (TH1F*)inputFile->Get( plotName.data() );
    if(bkgModelPlot == nullptr) std::cout<<"Plot "<< plotName << " does not exist" <<std::endl;
    bkgModelPlot->SetDirectory(0);
    // bkgModelPlot->Rebin(rebinValue);
    if(normalizeBinByBin) normalizeByBinSize1D(bkgModelPlot);
    bkgModelPlot->SetNameTitle(modelName.data(), modelName.data());
    bkgModelPlot->SetMarkerStyle(20);
    bkgModelPlot->SetMarkerSize(0.3);
    bkgModelPlot->SetMarkerColor(kRed);
    bkgModelPlot->SetLineColor(kRed);
    // bkgModelPlot->Draw("same C E0");
    float theLocalMax = bkgModelPlot->GetMaximum();
    if(theLocalMax > theMaxY) theMaxY = theLocalMax;
    // legendList.insert(legendList.begin(), {bkgModelPlot, bkgModelPlot->GetName(), "lpe"});

    // if(dataDataset != NO_PLOT)
    // {
    //     std::string plotName = dataDataset + "/" + selectionAndRegion + "/" + dataDataset + "_" + selectionAndRegion + "_" + variableName;
    //     TH1F* datasetPlot = (TH1F*)inputFile->Get( plotName.data() );
    //     if(datasetPlot == nullptr) std::cout<<"Plot "<< plotName << " does not exist" <<std::endl;
    //     datasetPlot->SetDirectory(0);
    //     // datasetPlot->Rebin(rebinValue);
    //     if(normalizeBinByBin) normalizeByBinSize1D(datasetPlot);
    //     datasetPlot->SetNameTitle(dataName.data(), dataName.data());
    //     datasetPlot->SetMarkerStyle(20);
    //     datasetPlot->SetMarkerSize(0.3);
    //     datasetPlot->SetMarkerColor(kBlack);
    //     datasetPlot->SetLineColor(kBlack);
    //     datasetPlot->Draw("same C E0");
    //     float theLocalMax = datasetPlot->GetMaximum();
    //     if(theLocalMax > theMaxY) theMaxY = theLocalMax;
    //     legendList.insert(legendList.begin(), {datasetPlot, datasetPlot->GetName(), "lpe"});
    // }

    theBackgroundStack->SetMaximum(theMaxY*100.);
    if (mYlabel.Contains(91)) theBackgroundStack->SetMinimum(0.00001);
    else if (mYlabel.Contains(100)) theBackgroundStack->SetMinimum(0.0001);

    else if (mYlabel.Contains("340<mX<488") && sample.Contains("4b")){ theBackgroundStack->SetMinimum(0.0001);theBackgroundStack->GetXaxis()->SetRangeUser(0,500);}
    else if (mYlabel.Contains("488<mX<648") && sample.Contains("4b")){ theBackgroundStack->SetMinimum(0.0001);theBackgroundStack->GetXaxis()->SetRangeUser(0,700);}
    else if (mYlabel.Contains("648<mX<960") && sample.Contains("4b")){ theBackgroundStack->SetMinimum(0.0001);theBackgroundStack->GetXaxis()->SetRangeUser(0,1000);}
    else if (mYlabel.Contains("960<mX<1216") && sample.Contains("4b")){ theBackgroundStack->SetMinimum(0.0001);theBackgroundStack->GetXaxis()->SetRangeUser(0,1300);}
    else if (mYlabel.Contains("340<mX<1216") && sample.Contains("4b")){ theBackgroundStack->SetMinimum(0.0001);theBackgroundStack->GetXaxis()->SetRangeUser(0,1300);}

    else if (mYlabel.Contains("340<mX<488") && sample.Contains("3b")){ theBackgroundStack->SetMinimum(0.0001);theBackgroundStack->GetXaxis()->SetRangeUser(0,500);}
    else if (mYlabel.Contains("488<mX<648") && sample.Contains("3b")){ theBackgroundStack->SetMinimum(0.0001);theBackgroundStack->GetXaxis()->SetRangeUser(0,700);}
    else if (mYlabel.Contains("648<mX<960") && sample.Contains("3b")){ theBackgroundStack->SetMinimum(0.0001);theBackgroundStack->GetXaxis()->SetRangeUser(0,1000);}
    else if (mYlabel.Contains("960<mX<1216") && sample.Contains("3b")){ theBackgroundStack->SetMinimum(0.0001);theBackgroundStack->GetXaxis()->SetRangeUser(0,1300);}
    else if (mYlabel.Contains("340<mX<1216") && sample.Contains("3b")){ theBackgroundStack->SetMinimum(0.0001);theBackgroundStack->GetXaxis()->SetRangeUser(0,1300);}

    else theBackgroundStack->SetMinimum(0.001);


    // for(size_t dIt=0; dIt<signalDatasetList.size(); ++dIt)
    // {
    //     const std::string &datasetName = signalDatasetList[dIt];
    //     // cout<< "iterator: "<< datasetName<<"\n";
    //     std::string plotName = datasetName + "/" + selectionAndRegion + "/" + datasetName + "_" + selectionAndRegion + "_" + variableName;
    //     TH1F* datasetPlot = (TH1F*)inputFile->Get( plotName.data() );
    //     if(datasetPlot == nullptr) std::cout<<"Plot "<< plotName << " does not exist" <<std::endl;
    //     datasetPlot->SetDirectory(0);
    //     if(normalizeBinByBin) normalizeByBinSize1D(datasetPlot);
    //     datasetPlot->SetLineColor(kBlue);
    //     datasetPlot->SetLineWidth(2);
    //     datasetPlot->SetNameTitle(datasetName.data(), datasetName.data());
    //     datasetPlot->Draw("same hist");
    //     if(dIt==0) theSignalLegend->AddEntry(datasetPlot, signalName.data(), "l");
    // }

    for(auto& legend : legendList) theLegend->AddEntry(std::get<0>(legend), std::get<1>(legend), std::get<2>(legend));
    theLegend->Draw("same");
    if(signalDatasetList.size()>0) theSignalLegend->Draw("same");

    // pad1->SetLogy();
    theCanvas->SetLogy();

    TString Region = TString(selectionAndRegion);
    TString labelText="";
    TLatex CMSlabel;
    CMSlabel.SetTextFont(63);
    CMSlabel.SetTextSize( 38 );
    CMSlabel.DrawLatexNDC(0.12, 0.93, "CMS #scale[0.8]{#it{#bf{Work In Progress}}}");
    TLatex plotlabels;
    plotlabels.SetTextFont(63);
    plotlabels.SetTextSize(28);
    if(Region.Contains("SignalRegion")) labelText="Signal Region";
    if(Region.Contains("ValidationRegion")) labelText="Validation Region";
    if(Region.Contains("ControlRegion")) labelText="Control Region";
    plotlabels.DrawLatexNDC(0.60, 0.93, labelText);
    plotlabels.SetTextFont(53);
    plotlabels.SetTextSize(28);
    plotlabels.DrawTextNDC(0.83, 0.93,labelText.Format("%d", year));
    plotlabels.SetTextFont(63);
    plotlabels.SetTextSize(28);
    plotlabels.DrawTextNDC(0.2, 0.84, sample);
    plotlabels.DrawTextNDC(0.2, 0.80, mYlabel);
    std::cout<<sample<< " " <<mYlabel<<std::endl;

    theCanvas->cd();

}

void StackAllDatasets(TVirtualPad *theCanvas, TFile* inputFile, TFile* inputFile1, TFile* inputFile2, const std::string& selectionAndRegion, const std::string& variableName, const std::string& modelDataset, const std::string& modelName, const std::vector<std::string>& signalDatasetList, const std::string& signalName, const std::string& dataDataset, const std::string& dataName, bool normalizeBinByBin, const std::string& xAxisName, const std::string& yAxisName, const int year, const TString mYlabel, const TString sample)
{

    // std::vector<std::string> datasetList     = {"ggF_Hbb","VBF_Hbb","QCD"   ,"ttbar","WH"    ,"ZH"  ,"ZZ"  ,"ttH"   };
    // std::vector<std::string> datasetNameList = {"ggF_Hbb","VBF_Hbb","QCD"   ,"ttbar","WH"    ,"ZH"  ,"ZZ"  ,"ttH"   };
    std::vector<std::string> datasetList     = { "ggF_Hbb","VBF_Hbb", "WH" ,"ZH"  ,"ZZ", "ttH", "Zjets", "ttbar", "QCD" };
    std::vector<std::string> datasetNameList = { "ggF_Hbb","VBF_Hbb", "WH" ,"ZH"  ,"ZZ", "ttH", "Zjets", "ttbar", "QCD" };
    // std::vector<EColor>      colorList       = {kRed     , kBlue   , kYellow, kGreen, kViolet, kCyan, kGray, kOrange};
    std::vector<Int_t>      colorList       = { TColor::GetColor("#fdffb6"), TColor::GetColor("#9bf6ff"), TColor::GetColor("#daae66"), TColor::GetColor("#cc00cc"), TColor::GetColor("#16537e"), TColor::GetColor("#caffbf"), TColor::GetColor("#a0c4ff"), TColor::GetColor("#ffc6ff"), TColor::GetColor("#ff8b94") };

    StackPlot(theCanvas, inputFile, inputFile1, inputFile2, selectionAndRegion, variableName, datasetList, datasetNameList, colorList, modelDataset, modelName, signalDatasetList, signalName, dataDataset, dataName, normalizeBinByBin, xAxisName, yAxisName, year, mYlabel, sample);

}

//  void StackAllVariables(const TString inputFileName, TString tag, const TString mYlabel, const TString sample, const std::string& selectionAndRegion, int year, const std::string& modelDataset=NO_PLOT, const std::string& modelName="BKG model",  const std::vector<std::string>& signalDatasetList = {}, const std::string& signalName="X{#rightarrow}YH", const bool vsMY=false)
void StackAllVariables( TString tag, const TString mYlabel, const TString sample, const std::string& selectionAndRegion, int year, const bool vsMY=false, TString tag2="") {

    gROOT->SetBatch();

    TString yearString=Form ("%d", year);

    TString inputFileName= "VarPlots/rootHists/fullSubmission_2022Nov/"+yearString+"DataPlots_"+tag+"/outPlotter.root";
    TString inputFileName1= "VarPlots/rootHists/fullSubmission_2022Nov/"+yearString+"DataPlots_"+tag2+"/outPlotter.root";
    // always calling 2016, because I don't know how to initialize a TFile without loading the file
    TString inputFileName2= "VarPlots/rootHists/fullSubmission_2022Nov/2016preVFPDataPlots_"+tag2+"/outPlotter.root";;
    // if (year==2016) inputFileName2= "VarPlots/rootHists/fullSubmission_2022Nov/"+yearString+"preVFPDataPlots_"+tag2+"/outPlotter.root";

    const std::string& modelDataset= "data_BTagCSV_dataDriven_kinFit";
    const std::string& modelName="BKG model";
    const std::vector<std::string>& signalDatasetList = {};
    const std::string& signalName="X{#rightarrow}YH";


    const std::string& dataDataset=NO_PLOT;
    const std::string& dataName="data";
    std::cout<<year<< " "<< selectionAndRegion<<"\n";

    TFile inputFile(inputFileName);
    TFile inputFile1(inputFileName1);
    TFile inputFile2(inputFileName2);
    // doesn't work:
    // if (year==2016) inputFile2.Open(inputFileName2);

    std::string canvasName = "BackgroundOverlap_" + selectionAndRegion + "_" + std::to_string(year);
    TCanvas *theCanvas = new TCanvas(canvasName.data(), canvasName.data(), 1400, 900);

    std::vector<std::string> variableVector = {};
    std::vector<std::string> xAxisVector = {};
    if (vsMY) {variableVector.push_back("H2_m"); xAxisVector.push_back("m_{Y} [GeV]"); }
    else {variableVector.push_back("HH_kinFit_m"); xAxisVector.push_back("m^{kinFit}_{Xreco} [GeV]"); }
    std::vector<bool>        normalizeBinByBinVector = {true};
    std::vector<std::string> yAxisVector = {"events/GeV"};
    // std::vector<std::string> variableVector = {"H1_b1_ptRegressed", "H1_b2_ptRegressed", "H2_b1_ptRegressed", "H2_b2_ptRegressed", "H1_m", "H2_m", "HH_m", "FourBjet_sphericity"};
    // std::vector<bool>        normalizeBinByBinVector = {true, true, true, true, true, true, true, false};
    // std::vector<std::string> xAxisVector = {"pT(Hb1) [GeV]", "pT(Hb2) [GeV]", "pT(Yb1) [GeV]", "pT(Yb2) [GeV]", "m_{Hreco} [GeV]", "m_{Yreco} [GeV]", "m_{Xreco} [GeV]", "Four b-jet sphericity" };
    // std::vector<std::string> yAxisVector = {"events/GeV", "events/GeV", "events/GeV", "events/GeV", "events/GeV", "events/GeV", "events/GeV", "events/GeV"};
    theCanvas->DivideSquare(variableVector.size(),0.005,0.005);
    for(size_t vIt = 0; vIt<variableVector.size(); ++vIt)
        StackAllDatasets(theCanvas->cd(vIt+1), &inputFile, &inputFile1, &inputFile2, selectionAndRegion, variableVector[vIt], modelDataset, modelName, signalDatasetList, signalName, dataDataset, dataName, normalizeBinByBinVector[vIt], xAxisVector[vIt], yAxisVector[vIt], year, mYlabel, sample);
    // TString odir = "VarPlots/BkgCompositionZjets2024Jun30/";
    TString odir = "VarPlots/BkgCompositionZjets2024Jun30_pngs/";
    odir=odir+tag+"/";
    std::error_code err;
    // if (!CreateDirectoryRecursive(odir.Data(), err))
    // {
    //     // Report the error:
    //     std::cout << "CreateDirectoryRecursive FAILED, err: " << err.message() << std::endl;
    // }
    theCanvas->SaveAs(odir + theCanvas->GetName() + ".png");
    // theCanvas->SaveAs(odir + theCanvas->GetName() + ".pdf");
    // theCanvas->SaveAs(odir + theCanvas->GetName() + ".C");

    inputFile.Close();
    delete theCanvas;

    gROOT->SetBatch(false);
}

void StackPlots_mY90GeV_Zjets(TString tag, TString tag2, TString mYlabel, TString sample, TString plotAgainstMY, TString iyear="0")
// void StackPlots_mY90GeV_Zjets()
{

    // TString tag= "2022Nov14_bJetScoreLoose_shapes_allVars_selectSigs"
    int year=iyear.Atoi();
    bool vsMY= plotAgainstMY.Contains("true");
    // std::cout<<"here\n";
    // TString tag= "2023Jul5_vars";
    // TString tag= "2024Jun11_vars"; TString mYlabel = ""; TString sample="4b Sample";
    // TString tag= "2024Jun11_vars_3b"; TString mYlabel = ""; TString sample="3b Sample";
    // TString tag= "2024Jun11_vars_mY90pm10"; TString mYlabel = "80<mY<100"; TString sample="4b Sample";
    // TString tag= "2024Jun11_vars_mY90pm1"; TString mYlabel = "89<mY<91"; TString sample="4b Sample";
    // TString tag= "2024Jun11_vars_mY90pm10_3b"; TString mYlabel = "80<mY<100"; TString sample="3b Sample";
    // TString tag= "2024Jun11_vars_mY90pm1_3b"; TString mYlabel = "89<mY<91"; TString sample="3b Sample";

    StackAllVariables(tag, mYlabel, sample,  "selectionbJets_SignalRegion", year, vsMY, tag2);
    StackAllVariables(tag, mYlabel, sample,  "selectionbJets_ValidationRegionBlinded", year, vsMY, tag2);
    StackAllVariables(tag, mYlabel, sample,  "selectionbJets_ControlRegionBlinded", year, vsMY, tag2);

    // StackAllVariables(tag, mYlabel, sample, "selectionbJets_SignalRegion", 2017, vsMY, tag2);
    // StackAllVariables(tag, mYlabel, sample, "selectionbJets_ValidationRegionBlinded", 2017, vsMY, tag2);
    // StackAllVariables(tag, mYlabel, sample, "selectionbJets_ControlRegionBlinded", 2017, vsMY, tag2);

    // StackAllVariables(tag, mYlabel, sample, "selectionbJets_SignalRegion", 2018, vsMY, tag2);
    // StackAllVariables(tag, mYlabel, sample, "selectionbJets_ValidationRegionBlinded", 2018, vsMY, tag2);
    // StackAllVariables(tag, mYlabel, sample, "selectionbJets_ControlRegionBlinded", 2018, vsMY, tag2);


}

