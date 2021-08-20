#include "Riostream.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TFile.h"
#include "TROOT.h"
#include "TCanvas.h"
#include <vector>
#include <map>
#include "TChain.h"
#include "TF1.h"
#include "TMath.h"
#include <fstream>

std::string selection = "NbJets >= 4";
std::string signalRegion = " && H1_m > 125-20 && H1_m < 125+20";

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


float getHalfWidthHalfMaximum(TH1F *variablePlot, float xMin, float xMax)
{
    //In this way you find the maximum
    int binWithMaximum = variablePlot->GetMaximumBin();
    float maxValue = variablePlot->GetBinContent(binWithMaximum);
    float maxBinCenter = variablePlot->GetBinCenter(binWithMaximum);

    //let's search for the point of half maximum, 
    //one will be on the left and the other one on the right
    //so the reason for the two call, using he lower and upper bound
    //of the x range for the fuction.
    float fwhm_left  = variablePlot->GetBinCenter(variablePlot->FindFirstBinAbove(maxValue/2., 1));//, -1, binWithMaximum));
    float fwhm_right = variablePlot->GetBinCenter(variablePlot->FindLastBinAbove (maxValue/2., 1));//, binWithMaximum, -1));
    
    return (fwhm_right - fwhm_left)/2.;
}


// float getVariableAndFit(std::string fileName, std::string variable, int year, float xMin, float xMax)
std::pair<double, double> getVariableAndFit(TVirtualPad *theCanvas, std::string fileName, std::string variable, int year, float xMin, float xMax, float quantile)
{
    // gROOT->SetBatch(true);
    std::vector<std::string> fileList     = splitByLine(fileName    );
    auto theTree     = getChainFromFileList(fileList    , "bbbbTree");

    auto sampleName = getSampleNameFromFile(fileName);
    auto pairMxMy   = getMxMyFromSample(sampleName);

    theCanvas->cd();

    std::string xAxisLabel = "";

    if(variable == "H1_m" || variable == "H1_kinFit_m")
    {
        xAxisLabel = "m_{H}";
    }
    if(variable == "H2_m"                             )
    {
        xAxisLabel = "m_{Y}";
    }
    if(variable == "HH_m" || variable == "HH_kinFit_m")
    {
        xAxisLabel = "m_{X}";
    }

    TH1F *variablePlot = new TH1F((sampleName + "_" + variable).c_str(), ("m_{X} = " + pairMxMy.first + " Gev - m_{Y} = " + pairMxMy.second + "; " + xAxisLabel.c_str() + " [GeV]; entries [a.u.]" ).c_str()
        , 600, xMin, xMax);
    std::string plotMxKinFirCmd = variable + std::string(">>") + sampleName + "_" + variable;
    std::string theCurrentSelection = selection;
    if(variable != "H1_m" && variable != "H1_kinFit_m") theCurrentSelection += signalRegion;

    // std::string selectionGenMatched = "&& gen_H1_b1_matchedflag >= 0 && gen_H1_b2_matchedflag >= 0 && gen_H2_b1_matchedflag >= 0 && gen_H2_b2_matchedflag >= 0";
    // if(stoi(pairMxMy.second) == 125) selectionGenMatched = "&& ((gen_H1_b1_matchedflag >= 0 && gen_H1_b2_matchedflag >= 0) || (gen_H1_b1_matchedflag_swapped >= 0 && gen_H1_b2_matchedflag_swapped >= 0)) && ((gen_H2_b1_matchedflag >= 0 && gen_H2_b2_matchedflag >= 0) || (gen_H2_b1_matchedflag_swapped >= 0 && gen_H2_b2_matchedflag_swapped >= 0))";
    // theCurrentSelection += selectionGenMatched;

    std::string massCut = " && " + variable + ">" + std::to_string(xMin) + " && "  + variable + "<" + std::to_string(xMax);
    std::cout<<massCut<<std::endl;
    theCurrentSelection += massCut;

    theTree->Draw(plotMxKinFirCmd.c_str(), theCurrentSelection.data());
    variablePlot->Scale(1./variablePlot->Integral());
    float halfWidthHalfMaximum =  getHalfWidthHalfMaximum(variablePlot, xMin, xMax);
    size_t numberOfQuantiles = 2;
    double xq[numberOfQuantiles];  // position where to compute the quantiles in [0,1]
    double yq[numberOfQuantiles];  // array to contain the quantiles
    xq[0] = quantile;
    xq[1] = 1 - quantile;
    variablePlot->GetQuantiles(numberOfQuantiles, yq, xq);
    std::cout << yq[0] << " - " << yq[1] <<std::endl;
    variablePlot->SetLineColor(kBlue);
    variablePlot->SetMaximum(variablePlot->GetMaximum()*1.2);
    variablePlot->SetDirectory(0);
    variablePlot->Draw();
    return std::make_pair(yq[0], yq[1]);
    
}

std::pair<double, double> plotVariableQuantile(std::string variable, int year, int mX, int mY, float quantile)
{
    // gROOT->SetBatch(true);
    auto getFileName = [year](std::pair<int,int> massPoint) -> std::string
    {
        return "plotterListFiles/" + std::to_string(year) + "Resonant_NMSSM_XYH_bbbb/Signal/FileList_NMSSM_XYH_bbbb_MX_" 
            + std::to_string(massPoint.first) + "_NANOAOD_v7_Full_MY_" + std::to_string(massPoint.second) + ".txt";
    };

    float xMin=0.;
    float xMax=0.;
    if(variable == "H1_m" || variable == "H1_kinFit_m")
    {
        xMin = 125.*0.5;
        xMax = 125.*1.5;
    }
    if(variable == "H2_m"                             )
    {
        xMin = 0.;
        xMax = 2400.;
    }
    if(variable == "HH_m" || variable == "HH_kinFit_m")
    {
        xMin = 0.;
        xMax = 2400.;
    }

    std::string canvasName = "Variable_" + variable + "_MX_" + std::to_string(mX) + "_MY_" + std::to_string(mY) + "_" + std::to_string(year);
    TCanvas *theCanvasKinFitImpact = new TCanvas(canvasName.c_str(), canvasName.c_str(), 1400, 1000);
    // float halfWidthHalfMaximum = getVariableAndFit(getFileName({mX,mY}), variable, year, xMin, xMax);
    std::pair<double, double> quantiles = getVariableAndFit(theCanvasKinFitImpact,getFileName({mX,mY}), variable, year, xMin, xMax, quantile);
    theCanvasKinFitImpact->SaveAs((std::string(theCanvasKinFitImpact->GetName()) + ".png").c_str());
    // gROOT->SetBatch(false);
    return quantiles;
}


std::pair<float, float> getMassesFromSignalName(const std::string& signalName)
{

    std::string mXbeginString = "sig_NMSSM_bbbb_MX_"      ;
    std::string mXendString   = "_MY_" ;
    std::string mYbeginString = "_MY_"      ;
    std::string mYendString   = "\0"   ;

    int mXbegin = signalName.find(mXbeginString) + mXbeginString.size();
    int mXend   = signalName.find(mXendString);
    int mYbegin = signalName.find(mYbeginString) + mYbeginString.size();
    int mYend   = signalName.find(mYendString);
    int xMass = atoi(signalName.substr(mXbegin, mXend-mXbegin).c_str());
    int yMass = atoi(signalName.substr(mYbegin, mYend-mYbegin).c_str());

    return std::make_pair(xMass, yMass);
}

std::vector<float> getBinning(const std::vector<float>& listOfPoints)
{
    uint numberOfPoints = listOfPoints.size();
    std::vector<float> binning(numberOfPoints+1);
    for (uint point=0; point<numberOfPoints-1; ++point) binning[point+1] = (listOfPoints[point]+listOfPoints[point+1])/2.;
    binning[0]              = 2.*listOfPoints[0] - binning[1];
    binning[numberOfPoints] = 2.*listOfPoints[numberOfPoints-1] - binning[numberOfPoints-1];
    return binning;
}



void PlotAllQuantilesVariable(TFile& theOutputFile, std::string variable, int year, float quantile)
{
    gROOT->SetBatch(true);
    std::vector<float> xMassList;
    std::vector<float> yMassList;
    std::vector<std::pair<float, float>> pointList;

    std::vector<std::string> signalList = splitByLine("privateTools/listOfSamples.txt");

    for(const auto& signal : signalList)
    {
        const auto xAndYmass = getMassesFromSignalName(signal);
        pointList.push_back(xAndYmass);
        if(std::find (xMassList.begin(), xMassList.end(), xAndYmass.first ) == xMassList.end()) xMassList.emplace_back(xAndYmass.first );
        if(std::find (yMassList.begin(), yMassList.end(), xAndYmass.second) == yMassList.end()) yMassList.emplace_back(xAndYmass.second);
    }
    for(auto mass : xMassList)
    {
        std::cout << mass << " ";
    }
    std::cout << std::endl;
    for(auto mass : yMassList)
    {
        std::cout << mass << " ";
    }
    std::cout << std::endl;


    std::sort(xMassList.begin(), xMassList.end());
    std::sort(yMassList.begin(), yMassList.end());

    auto xBinning = getBinning(xMassList);
    auto yBinning = getBinning(yMassList);
    for(auto bin : xBinning)
    {
        std::cout << bin << " ";
    }
    std::cout << std::endl;
    for(auto bin : yBinning)
    {
        std::cout << bin << " ";
    }
    std::cout << std::endl;


    std::string titleVariable = "";

    std::string histogramTitle = titleVariable + " - Half width half maximum (GeV) " + " - year " + std::to_string(year);
    if(variable == "H1_m" || variable == "H1_kinFit_m")
    {
        titleVariable = "m_{H}";
    }
    if(variable == "H2_m"                             )
    {
        titleVariable = "m_{Y}";
        histogramTitle = titleVariable + " - HWHM/" + titleVariable + " (%) " + " - year " + std::to_string(year);
    }
    if(variable == "HH_m" || variable == "HH_kinFit_m")
    {
        titleVariable = "m_{X}";
        histogramTitle = titleVariable + " - HWHM/" + titleVariable + " (%) " + " - year " + std::to_string(year);
    }


    std::string histogramNameLow  = "ResolutionPlot_" + variable + "_" + std::to_string(year) + "_QuantileLow";
    std::string histogramTitleLow = histogramTitle  + "_Quantile Low";;
    TH2F* theQuantilePlotLow = new TH2F(histogramNameLow.c_str(), histogramTitleLow.c_str(), xBinning.size()-1, xBinning.data(), yBinning.size()-1, yBinning.data());
    theQuantilePlotLow->GetXaxis()->SetTitle("m_{X} [GeV]");
    theQuantilePlotLow->GetYaxis()->SetTitle("m_{Y} [GeV]");
    theQuantilePlotLow->GetYaxis()->SetTitleOffset(1.2);
    theQuantilePlotLow->SetStats(false);

    std::string histogramNameHigh  = "ResolutionPlot_" + variable + "_" + std::to_string(year) + "_QuantileHigh";
    std::string histogramTitleHigh = histogramTitle  + "_Quantile High";;
    TH2F* theQuantilePlotHigh = new TH2F(histogramNameHigh.c_str(), histogramTitleHigh.c_str(), xBinning.size()-1, xBinning.data(), yBinning.size()-1, yBinning.data());
    theQuantilePlotHigh->GetXaxis()->SetTitle("m_{X} [GeV]");
    theQuantilePlotHigh->GetYaxis()->SetTitle("m_{Y} [GeV]");
    theQuantilePlotHigh->GetYaxis()->SetTitleOffset(1.2);
    theQuantilePlotHigh->SetStats(false);

    for(auto& point : pointList)
    {
        std::pair<double, double> quantiles = plotVariableQuantile(variable, year, point.first, point.second, quantile);

        theQuantilePlotLow ->Fill(point.first, point.second, quantiles.first );
        theQuantilePlotHigh->Fill(point.first, point.second, quantiles.second);
    }

    std::string canvasName = "QuantilePlot_" + variable + "_" + std::to_string(year);

    std::string canvasNameLow  = canvasName + "_QuantileLow";
    TCanvas *theCanvasResolutionLow = new TCanvas(canvasNameLow.c_str(), canvasNameLow.c_str(), 1400, 1000);
    theQuantilePlotLow->Draw("colz");
    theCanvasResolutionLow->SaveAs((std::string(theCanvasResolutionLow->GetName()) + ".png").c_str());
    theCanvasResolutionLow->Write();
    theOutputFile.WriteObject(theCanvasResolutionLow, theCanvasResolutionLow->GetName());

    std::string canvasNameHigh  = canvasName + "_QuantileHigh";
    TCanvas *theCanvasResolutionHigh = new TCanvas(canvasNameHigh.c_str(), canvasNameHigh.c_str(), 1400, 1000);
    theQuantilePlotHigh->Draw("colz");
    theCanvasResolutionHigh->SaveAs((std::string(theCanvasResolutionHigh->GetName()) + ".png").c_str());
    theCanvasResolutionHigh->Write();
    theOutputFile.WriteObject(theCanvasResolutionHigh, theCanvasResolutionHigh->GetName());

    gROOT->SetBatch(false);
}

void PlotAllQuantiles()
{
    TFile theOutputFile("QuantilePlot.root", "RECREATE");
    std::vector<int> yearList = {2016};
    // std::vector<int> yearList = {2016, 2017, 2018};
    std::vector<std::string> variableList = {"H2_m", "HH_kinFit_m"};
    // std::vector<std::string> variableList = {"H1_m", "H2_m", "HH_kinFit_m"};
    float quantile = 0.025;

    for(auto year : yearList)
    {
        for(auto variable : variableList)
        {
            PlotAllQuantilesVariable(theOutputFile, variable, year, quantile);
        }
    }
    theOutputFile.Close();
}





