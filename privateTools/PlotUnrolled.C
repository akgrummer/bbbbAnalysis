#include "Riostream.h"
#include "TFile.h"
#include "TH1F.h"
#include "TH2I.h"
#include "TH2F.h"
#include "TCanvas.h"
#include "TROOT.h"
#include "TLegend.h"

typedef std::tuple<std::string, std::string> FileAndHistName;
typedef std::tuple<FileAndHistName, std::string, EColor, float> SignalInfo;

template <typename Hist>
using SignalPlot = std::tuple<Hist*, std::string, EColor>;

template<typename Hist>
Hist* getHistogramFromFileAndClose(FileAndHistName& histogramInfo)
{
    TFile inputFile(std::get<0>(histogramInfo).c_str());
    Hist* histogram = (Hist*)inputFile.Get(std::get<1>(histogramInfo).c_str());
    if(histogram == nullptr)
    {
        std::cout<< "Histogram " << std::get<1>(histogramInfo) << " does not exist" << std::endl;
        exit(EXIT_FAILURE);
    }
    histogram->SetDirectory(0);
    inputFile.Close();
    return histogram;
}

void normalizeByBinSize2D(TH2F* inputPlot)
{
    for(int nBinX = 1; nBinX<=inputPlot->GetNbinsX(); ++nBinX)
    {
        for(int nBinY = 1; nBinY<=inputPlot->GetNbinsY(); ++nBinY)
        {
            float binWidth = inputPlot->GetXaxis()->GetBinWidth(nBinX)*inputPlot->GetYaxis()->GetBinWidth(nBinY);
            inputPlot->SetBinContent(nBinX,nBinY,inputPlot->GetBinContent(nBinX,nBinY)/binWidth);
            inputPlot->SetBinError  (nBinX,nBinY,inputPlot->GetBinError  (nBinX,nBinY)/binWidth);
        }
    }
    return;

}

void fill2DplotFromUnrolled(TH2I *binningPlot, TH1F* backgroundPlot, TH2F *plotHistogram, float extraError, bool useError = true)
{
    for(int nBinX = 1; nBinX<=binningPlot->GetNbinsX(); ++nBinX)
    {
        for(int nBinY = 1; nBinY<=binningPlot->GetNbinsY(); ++nBinY)
        {
            float binContent = backgroundPlot->GetBinContent(binningPlot->GetBinContent(nBinX,nBinY));
            plotHistogram->SetBinContent(nBinX,nBinY,binContent);
            if(useError)
            {
                float binError = sqrt(binContent + binContent*binContent*extraError*extraError);
                plotHistogram->SetBinError  (nBinX,nBinY,binError);
            }
        }
    }
    return;

}

std::pair<std::vector<float>, std::vector<float>> get2DPlotBinning(const TH2I* inputPlot)
{
    std::vector<float> xBinList;
    std::vector<float> yBinList;

    for(int nBinX = 1; nBinX<=inputPlot->GetNbinsX(); ++nBinX)
    {
        xBinList.push_back(inputPlot->GetXaxis()->GetBinLowEdge(nBinX));
    }
    xBinList.push_back(inputPlot->GetXaxis()->GetBinUpEdge(inputPlot->GetNbinsX()));

    for(int nBinY = 1; nBinY<=inputPlot->GetNbinsY(); ++nBinY)
    {
        yBinList.push_back(inputPlot->GetYaxis()->GetBinLowEdge(nBinY));
    }
    yBinList.push_back(inputPlot->GetYaxis()->GetBinUpEdge(inputPlot->GetNbinsY()));

    return std::make_pair(xBinList, yBinList);
}


std::tuple<TH1F*, TH1F*> splitErrorAndPlots(const TH1F* inputPlot)
{
    std::string valuePlotName = std::string(inputPlot->GetName()) + "_value";
    std::string errorPlotName = valuePlotName + "Error";
    int numberOfBins = inputPlot->GetNbinsX();
    TH1F* outputPlot  = (TH1F*)inputPlot->Clone(valuePlotName.data());
    TH1F* outputError = (TH1F*)inputPlot->Clone(errorPlotName.data());
    for(int nBin = 1; nBin<=numberOfBins; ++nBin)
    {
        outputPlot->SetBinError  (nBin,0.);
    }

    outputError->SetFillStyle(3002);
    outputError->SetFillColor(kBlack);
    outputError->SetLineColor(kBlack);

    return {outputPlot,outputError};
}



std::tuple<TH1F*, TH1F*> dividePlots(const TH1F* backgroundPlot, const TH1F* dataPlot)
{
    std::string errorPlotName = std::string(backgroundPlot->GetName()) + "_error";
    TH1F* ratioError = (TH1F*)backgroundPlot->Clone(errorPlotName.data());
    int numberOfBins = backgroundPlot->GetNbinsX();
    for(int nBin = 1; nBin<=numberOfBins; ++nBin)
    {
        float backgroundValue = backgroundPlot->GetBinContent(nBin);
        float backgroundError = backgroundPlot->GetBinError  (nBin);
        if(backgroundValue == 0.) continue;
        ratioError->SetBinContent(nBin, 1.                             );
        ratioError->SetBinError  (nBin, backgroundError/backgroundValue);
    }
    ratioError->SetFillStyle(3002);
    ratioError->SetFillColor(kBlack);

    TH1F* ratioPlot = nullptr;
    if(dataPlot != nullptr)
    {
        std::string ratioPlotName = std::string(dataPlot    ->GetName()) + "_ratio";
        ratioPlot  = (TH1F*)dataPlot->Clone(ratioPlotName.data());
        for(int nBin = 1; nBin<=numberOfBins; ++nBin)
        {
            float backgroundValue = backgroundPlot->GetBinContent(nBin);
            float backgroundError = backgroundPlot->GetBinError  (nBin);
            if(backgroundValue == 0.) continue;
            ratioPlot->SetBinContent(nBin,dataPlot->GetBinContent(nBin)/backgroundValue);
            ratioPlot->SetBinError  (nBin,dataPlot->GetBinError  (nBin)/backgroundValue);
        }
    }

    return {ratioPlot,ratioError};
}

std::tuple<TH1F*, TH1F*> RatioPlot(TVirtualPad *theCanvas, TH1F *backgroundHistogram, TH1F* dataHistogram, std::string title)
{

    std::string xAxis = "m_{X} [GeV]";
    std::string yAxis = "events [1/GeV^{2}]";
    
    // Upper plot will be in pad1
    TPad *pad1 = new TPad("pad1", "pad1", 0, 0.35, 1, 1.0);
    pad1->SetNumber(1);
    pad1->SetLeftMargin(0.12);
    pad1->SetBottomMargin(0); // Upper and lower plot are joined
    pad1->SetGridx();         // Vertical grid
    pad1->SetLogy();         
    pad1->Draw();             // Draw the upper pad: pad1
    pad1->cd();               // pad1 becomes the current pad
    auto backgroundHistAndError = splitErrorAndPlots(backgroundHistogram);
    std::get<0>(backgroundHistAndError)->Draw("hist");         // Draw backgroundHistogram on top of dataHistogram
    // Y axis dataHistogram plot settings
    std::get<0>(backgroundHistAndError)->SetStats(0);          // No statistics on upper plot
    std::get<0>(backgroundHistAndError)->GetYaxis()->SetTitleSize(0.07);
    std::get<0>(backgroundHistAndError)->GetYaxis()->SetTitleFont(62);
    std::get<0>(backgroundHistAndError)->GetYaxis()->SetTitleOffset(0.75);
    std::get<0>(backgroundHistAndError)->GetYaxis()->SetLabelFont(62); // Absolute font size in pixel (precision 3)
    std::get<0>(backgroundHistAndError)->GetYaxis()->SetLabelSize(0.06);
    std::get<0>(backgroundHistAndError)->GetYaxis()->SetTitle(yAxis.c_str());
    std::get<0>(backgroundHistAndError)->SetTitle(title.c_str());
    // std::get<0>(backgroundHistAndError) settings
    std::get<0>(backgroundHistAndError)->SetLineColor(kBlack);
    std::get<0>(backgroundHistAndError)->SetMarkerColor(kBlack);
    std::get<0>(backgroundHistAndError)->SetLineWidth(1);
    std::get<1>(backgroundHistAndError)->Draw("same E2");         // Draw backgroundHistogram on top of dataHistogram
    float yMaximum = std::get<0>(backgroundHistAndError)->GetMaximum();
    std::get<0>(backgroundHistAndError)->SetMaximum(yMaximum*100000.);


    if(dataHistogram != nullptr)
    {
        dataHistogram->SetStats(0);          // No statistics on upper plot
        dataHistogram->SetTitle("data"); // Remove the ratio title
        dataHistogram->Draw("ep same");               // Draw dataHistogram
        dataHistogram->SetLineColor(kBlack);
        dataHistogram->SetMarkerColor(kBlack);
        dataHistogram->SetMarkerStyle(20);
        dataHistogram->SetLineWidth(2);
    }
    
    
    // lower plot will be in pad
    theCanvas->cd();          // Go back to the main canvas before defining pad2
    TPad *pad2 = new TPad("pad2", "pad2", 0, 0., 1, 0.35);
    pad2->SetNumber(2);
    pad2->SetTopMargin(0);
    pad2->SetBottomMargin(0.2);
    pad2->SetGridx(); // vertical grid
    pad2->SetGridy(); // horizontal grid
    pad2->Draw();
    pad2->SetLeftMargin(0.12);
    pad2->SetBottomMargin(0.3);
    pad2->cd();       // pad2 becomes the current pad

    std::tuple<TH1F*, TH1F*> theRatioPlot = dividePlots(backgroundHistogram, dataHistogram);

    TH1F *ratioError = std::get<1>(theRatioPlot);
    ratioError->Draw("E2");
    ratioError->SetTitle("");
    ratioError->SetStats(0);
    // Y axis ratio plot settings
    ratioError->GetYaxis()->SetTitle("ratio");
    ratioError->GetYaxis()->SetNdivisions(505);
    ratioError->GetYaxis()->SetTitleSize(0.1);
    ratioError->GetYaxis()->SetTitleFont(62);
    ratioError->GetYaxis()->SetTitleOffset(0.4);
    ratioError->GetYaxis()->SetLabelFont(62); // Absolute font size in pixel (precision 3)
    ratioError->GetYaxis()->SetLabelSize(0.1);
    ratioError->SetMaximum(2.);
    ratioError->SetMinimum(0.);

    // X axis ratio plot settings
    ratioError->GetXaxis()->SetTitle(xAxis.c_str());
    ratioError->GetXaxis()->SetTitleSize(0.12);
    ratioError->GetXaxis()->SetTitleFont(62);
    ratioError->GetXaxis()->SetTitleOffset(0.82);
    ratioError->GetXaxis()->SetLabelFont(62); // Absolute font size in pixel (precision 3)
    ratioError->GetXaxis()->SetLabelSize(0.10);

    TH1F *ratio      = std::get<0>(theRatioPlot);
    if(ratio != nullptr)
    {
        ratio->Draw("ep same");       // Draw the ratio plot
    }
    
    theCanvas->cd();

    return backgroundHistAndError;

}

TH2F* prepare2Dplot(TH2I *binningPlot, TH1F* unrolledPlot, float extraError, std::vector<float> xBinList, std::vector<float> yBinList, bool useError = true)
{
    std::string histName = std::string(unrolledPlot->GetName()) + "_reRolled";
    TH2F *plotHistogram = new TH2F(histName.c_str(), histName.c_str(), xBinList.size()-1, xBinList.data(), yBinList.size()-1, yBinList.data());
    fill2DplotFromUnrolled(binningPlot, unrolledPlot, plotHistogram, extraError, useError);
    normalizeByBinSize2D(plotHistogram);

    return plotHistogram;
}

void fillUnrolled(TH1F* theUnrolledPlot, TH2F* plotHistogram, int nBinY)
{
    for(int nBinX = 1; nBinX<=plotHistogram->GetNbinsX(); ++nBinX)
    {
        theUnrolledPlot->SetBinContent(nBinX, plotHistogram->GetBinContent(nBinX, nBinY));
        theUnrolledPlot->SetBinError  (nBinX, plotHistogram->GetBinError  (nBinX, nBinY));
    }
}

void PlotUnrolledFromHist(TH2I *binningPlot, TH1F *backgroundPlot, TH1F *dataPlot, float extraError, int year, std::vector<SignalPlot<TH1F>> signalPlotList)
{

    auto binList = get2DPlotBinning(binningPlot);
    std::vector<float> &xBinList = std::get<0>(binList);
    std::vector<float> &yBinList = std::get<1>(binList);


    TH2F *dataPlot2D       = nullptr;
    if(dataPlot != nullptr)
    {
        dataPlot2D = prepare2Dplot(binningPlot, dataPlot, 0., xBinList, yBinList);
        std::cout<<"Is error correct for data???"<<std::endl;
    }

    TH2F *backgroundPlot2D = prepare2Dplot(binningPlot, backgroundPlot, extraError, xBinList, yBinList);

    std::vector<SignalPlot<TH2F>> signalPlot2DList;
    for(auto& signalPlot : signalPlotList)
    {
        signalPlot2DList.push_back({prepare2Dplot(binningPlot, std::get<0>(signalPlot), 0, xBinList, yBinList, false), std::get<1>(signalPlot), std::get<2>(signalPlot)});
    }

    gROOT->SetBatch(true);
    for(size_t yMassPoint = 0; yMassPoint<yBinList.size()-1; ++yMassPoint)
    {
        float yMassMin = yBinList.at(yMassPoint  );
        float yMassMax = yBinList.at(yMassPoint+1);
        std::string histogramTitle = "Run " + std::to_string(year) + " - " + std::to_string(int(yMassMin)) + " GeV < m_{Y} < " + std::to_string(int(yMassMax)) + " GeV";

        std::string backgroundHistogramName  = "Background_mY_" + std::to_string(int(yMassMin)) + "_" + std::to_string(int(yMassMax));
        TH1F* backgroundUnrolledHistogram = new TH1F(backgroundHistogramName.c_str(), histogramTitle.c_str(), xBinList.size()-1, xBinList.data());
        fillUnrolled(backgroundUnrolledHistogram, backgroundPlot2D, yMassPoint+1);

        auto theLegend = new TLegend(0.17,0.58,0.88,0.88);
        theLegend->SetNColumns(2);
        theLegend->SetTextSize(0.04);
        
        TH1F* dataUnrolledHistogram = nullptr;
        if(dataPlot != nullptr)
        {
            std::string dataHistogramName  = "Data_mY_" + std::to_string(int(yMassMin)) + "_" + std::to_string(int(yMassMax));
            dataUnrolledHistogram = new TH1F(dataHistogramName.c_str(), histogramTitle.c_str(), xBinList.size()-1, xBinList.data());
            fillUnrolled(dataUnrolledHistogram, dataPlot2D, yMassPoint+1);
            theLegend->AddEntry(dataUnrolledHistogram, "data", "pl");
        }


        std::string canvasName = "UnrolledPlot_" + std::to_string(year) + "_mY_" + std::to_string(int(yMassMin)) + "_" + std::to_string(int(yMassMax));
        TCanvas theCanvas(canvasName.c_str(), canvasName.c_str(), 1200, 800);
        auto backgroundHistAndError = RatioPlot(&theCanvas, backgroundUnrolledHistogram, dataUnrolledHistogram, histogramTitle);

        theLegend->AddEntry(std::get<0>(backgroundHistAndError), "BKG model"     , "l");
        theLegend->AddEntry(std::get<1>(backgroundHistAndError), "BKG model unc.", "f");

        TPad* MyPad= (TPad*)theCanvas.GetPad(1);
        MyPad->cd();

        int signalCounter = 0;
        for(auto& signalPlot2D : signalPlot2DList)
        {
            std::string signalHistogramName  = "signal_" + std::to_string(signalCounter++) + "_mY_" + std::to_string(int(yMassMin)) + "_" + std::to_string(int(yMassMax));
            TH1F* signalUnrolledHistogram = new TH1F(signalHistogramName.c_str(), histogramTitle.c_str(), xBinList.size()-1, xBinList.data());
            fillUnrolled(signalUnrolledHistogram, std::get<0>(signalPlot2D), yMassPoint+1);
            signalUnrolledHistogram->SetLineColor(std::get<2>(signalPlot2D));
            signalUnrolledHistogram->Draw("hist same");
            signalUnrolledHistogram->SetLineWidth(2);
            theLegend->AddEntry(signalUnrolledHistogram, std::get<1>(signalPlot2D).c_str(), "l");
        }

        theLegend->Draw("");

        theCanvas.cd();
        theCanvas.SaveAs((canvasName + ".png").data());

        // delete backgroundUnrolledHistogram;
        // delete dataPlot;

    }
    gROOT->SetBatch(false);

    // delete backgroundPlot2D;
    // delete dataPlot2D      ;

}

void PlotUnrolled(FileAndHistName& binningInfo, FileAndHistName& backgroundInfo, FileAndHistName& dataInfo, float extraError, int year, std::vector<SignalInfo> signalInfoList)
{
    TH2I *binningPlot    = getHistogramFromFileAndClose<TH2I>(binningInfo   );
    TH1F *backgroundPlot = getHistogramFromFileAndClose<TH1F>(backgroundInfo);

    TH1F *dataPlot = nullptr;
    if(std::get<0>(dataInfo) != "")
    {
        dataPlot = getHistogramFromFileAndClose<TH1F>(dataInfo);
    }

    std::vector<SignalPlot<TH1F>> signalPlotList;
    for(auto& signalInfo : signalInfoList)
    {
        TH1F *signalPlot = getHistogramFromFileAndClose<TH1F>(std::get<0>(signalInfo));
        signalPlot->Scale(std::get<3>(signalInfo));
        signalPlotList.push_back({signalPlot, std::get<1>(signalInfo), std::get<2>(signalInfo)});
    }

    PlotUnrolledFromHist(binningPlot, backgroundPlot, dataPlot, extraError, year, signalPlotList);

}

std::vector<std::tuple<int, int, std::map<int, float>, EColor>> infoForSignalList
{
    {300 , 125 , { {2016, 7.7}, {2017, 11.}, {2018, 6.1} }, kRed    }, 
    // {400 , 80  , { {2016, 2.0}, {2017, 2.8}, {2018, 1.9} }, kGreen  }, 
    {600 , 125 , { {2016, 3.6}, {2017, 4.4}, {2018, 2.7} }, kBlue   }, 
    {700 , 300 , { {2016, 5.5}, {2017, 6.3}, {2018, 3.9} }, kOrange }, 
    // {900 , 500 , { {2016, 3.2}, {2017, 3.8}, {2018, 2.3} }, kMagenta}, 
    {1000, 125 , { {2016, .96}, {2017, 1.3}, {2018, .73} }, kCyan   }, 
    // {1200, 800 , { {2016, 1.9}, {2017, 2.2}, {2018, 1.3} }, kOrange }, 
    {1400, 500 , { {2016, 1.1}, {2017, 1.4}, {2018, .80} }, kSpring }, 
    // {1600, 300 , { {2016, 11.}, {2017, 15.}, {2018, 9.0} }, kTeal   }, 
    // {1600, 1000, { {2016, 8.9}, {2017, 11.}, {2018, 6.4} }, kAzure  }, 
    // {1800, 600 , { {2016, 12.}, {2017, 14.}, {2018, 8.8} }, kViolet }, 
    {1800, 1400, { {2016, 9.8}, {2017, 12.}, {2018, 7.4} }, kViolet   }
};

std::map<int, float> bkgNormalizationErrorMap = { {2016, 0.01}, {2017, 0.01}, {2018, 0.013} };


std::vector<SignalInfo> makeSignalTuple(int year)
{
    std::vector<SignalInfo> signalInfoList;
    for(auto& element : infoForSignalList)
    {
        signalInfoList.push_back
        (
            {{"DataPlots_fullSubmission_" + std::to_string(year) + "_v30/outPlotter.root",
            "sig_NMSSM_bbbb_MX_" + std::to_string(std::get<0>(element)) + "_MY_" + std::to_string(std::get<1>(element)) + "/selectionbJets_SignalRegion/sig_NMSSM_bbbb_MX_" + std::to_string(std::get<0>(element)) + "_MY_" + std::to_string(std::get<1>(element)) + "_selectionbJets_SignalRegion_HH_kinFit_m_H2_m_Rebinned_Unrolled"},
            "sig. m_{X} = " + std::to_string(std::get<0>(element)) + " GeV - m_{Y} = " + std::to_string(std::get<1>(element)) + " GeV", std::get<3>(element), std::get<2>(element)[year] }
        );
    }
    return signalInfoList;
}

void PlotAllUnrolled(int year)
{
    
    FileAndHistName binningInfo    {"DataPlots_fullSubmission_" + std::to_string(year) + "_v30/outPlotter.root", "BinCorrispondancePlot"};
    FileAndHistName backgroundInfo {"DataPlots_fullSubmission_" + std::to_string(year) + "_v30/outPlotter.root", "data_BTagCSV_dataDriven_kinFit/selectionbJets_SignalRegion/data_BTagCSV_dataDriven_kinFit_selectionbJets_SignalRegion_HH_kinFit_m_H2_m_Rebinned_Unrolled"};
    // FileAndHistName dataInfo       {"DataPlots_fullSubmission_" + std::to_string(year) + "_v30/outPlotter.root", "data_BTagCSV_dataDriven_kinFit/selectionbJets_SignalRegion/data_BTagCSV_dataDriven_kinFit_selectionbJets_SignalRegion_HH_kinFit_m_H2_m_Rebinned_Unrolled"};
    FileAndHistName dataInfo       {"", ""};
    std::vector<SignalInfo> signalInfoList = makeSignalTuple(year);
    
    PlotUnrolled(binningInfo, backgroundInfo, dataInfo, bkgNormalizationErrorMap[year], year, signalInfoList);

}

