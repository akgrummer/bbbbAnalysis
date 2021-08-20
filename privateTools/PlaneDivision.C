#include "TFile.h"
#include "TH2D.h"
#include "TCanvas.h"
#include <fstream>
#include <vector>
#include <Riostream.h>
#include "TMarker.h"
#include "TBox.h"
#include "TStyle.h"

class MassGroups
{

  public:
    MassGroups(float mXmin, float mXmax)
    : fMXmin(mXmin)
    , fMXmax(mXmax)
    {}

    float fMXmin;
    float fMXmax;

    size_t countNumberOfBins(TH2F* mXmYplane)
    {
        size_t numberOfBins = 0;

        for(int xBin = 1; xBin <= mXmYplane->GetNbinsX(); xBin++)
        {
            for(int yBin = 1; yBin <= mXmYplane->GetNbinsY(); yBin++)
            {
                if(isNeededBin(mXmYplane,xBin,yBin)) ++numberOfBins;
            }
        }
        return numberOfBins;
    }

  private:
    float higgsMass = 120;

    bool isNeededBin(TH2F *the2Dplot, uint xBin, uint yBin)
    {
        float mX = the2Dplot->GetXaxis()->GetBinCenter(xBin);
        float mY = the2Dplot->GetYaxis()->GetBinCenter(yBin);
        if(mX - mY < higgsMass)  return false;
        if(mX > 1200 && mY < 80) return false;

        if(mX < fMXmin) return false;
        if(mX > fMXmax) return false;

        return true;
    }

};



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

void PlaneDivision()
{
    TFile quantileFile("QuantilePlot.root");
    TFile plotterFile("DataPlots_fullSubmission_2016_v30/outPlotter.root");

    TH2F* mXmYplane = (TH2F*)plotterFile.Get("data_BTagCSV_dataDriven_kinFit/selectionbJets_SignalRegion/data_BTagCSV_dataDriven_kinFit_selectionbJets_SignalRegion_HH_kinFit_m_H2_m");
    mXmYplane->SetDirectory(0);

    // TH2F* quantilePlotMxLow  = (TH2F*)((TCanvas*)quantileFile.Get("QuantilePlot_HH_kinFit_m_2016_QuantileLow" ))->GetPrimitive("ResolutionPlot_HH_kinFit_m_2016_QuantileLow" );
    // TH2F* quantilePlotMxHigh = (TH2F*)((TCanvas*)quantileFile.Get("QuantilePlot_HH_kinFit_m_2016_QuantileHigh"))->GetPrimitive("ResolutionPlot_HH_kinFit_m_2016_QuantileHigh");
    
    // TH2F* quantilePlotMyLow  = (TH2F*)((TCanvas*)quantileFile.Get("QuantilePlot_H2_m_2016_QuantileLow" ))->GetPrimitive("ResolutionPlot_H2_m_2016_QuantileLow" );
    // TH2F* quantilePlotMyHigh = (TH2F*)((TCanvas*)quantileFile.Get("QuantilePlot_H2_m_2016_QuantileHigh"))->GetPrimitive("ResolutionPlot_H2_m_2016_QuantileHigh");

    std::vector<std::tuple<EColor, float, float, MassGroups>> theMassGroupList;
    
    theMassGroupList.emplace_back(std::make_tuple(kBlue   ,  200.,  650., MassGroups(  212,  800))); // group 0 ->  300 -  600
    theMassGroupList.emplace_back(std::make_tuple(kRed    ,  650.,  850., MassGroups(  300, 1000))); // group 1 ->  700 -  800
    theMassGroupList.emplace_back(std::make_tuple(kBlack  ,  850., 1050., MassGroups(  450, 1200))); // group 2 ->  900 - 1000
    theMassGroupList.emplace_back(std::make_tuple(kViolet , 1050., 1450., MassGroups(  600, 1600))); // group 3 -> 1100 - 1400
    theMassGroupList.emplace_back(std::make_tuple(kGreen  , 1450., 2050., MassGroups(  950, 2320))); // group 4 -> 1600 - 2000
    // theMassGroupList.emplace_back(std::make_pair(kRed    , MassGroups( 250,  350,  105, 2400))); // group 1
    // theMassGroupList.emplace_back(std::make_pair(kGreen  , MassGroups( 350,  650,    0, 2400))); // group 2
    // theMassGroupList.emplace_back(std::make_pair(kBlue   , MassGroups( 650,  850,    0,  105))); // group 3
    // theMassGroupList.emplace_back(std::make_pair(kMagenta, MassGroups( 650,  850,  105, 2400))); // group 4
    // theMassGroupList.emplace_back(std::make_pair(kCyan   , MassGroups( 850, 1150,    0,  105))); // group 5
    // theMassGroupList.emplace_back(std::make_pair(kOrange , MassGroups( 850, 1150,  105, 2400))); // group 6
    // theMassGroupList.emplace_back(std::make_pair(kSpring , MassGroups(1150, 1550,    0,  225))); // group 7
    // theMassGroupList.emplace_back(std::make_pair(kBlack  , MassGroups(1150, 1550,  225, 2400))); // group 8
    // theMassGroupList.emplace_back(std::make_pair(kViolet , MassGroups(1550, 2050,  225,  750))); // group 9
    // theMassGroupList.emplace_back(std::make_pair(kPink   , MassGroups(1550, 2050,  750, 2400))); // group 10


    std::vector<std::pair<float, float>> pointList;

    std::vector<std::string> signalList = splitByLine("privateTools/listOfSamples.txt");

    for(const auto& signal : signalList)
    {
        const auto xAndYmass = getMassesFromSignalName(signal);
        pointList.push_back(xAndYmass);
    }

    gStyle->SetPalette(kAquamarine);
    TCanvas *theNewCanvas = new TCanvas("canvas", "canvas", 1400, 800);
    mXmYplane->SetStats(false);
    mXmYplane->Draw("colz");

    for(auto& signal : pointList) 
    {
        for(const auto& massGroup : theMassGroupList)
        {
            if(std::get<1>(massGroup) < signal.first && std::get<2>(massGroup) > signal.first)
            {
                TMarker *theMarker = new TMarker(signal.first, signal.second, 20);
                theMarker->SetMarkerStyle(20);
                theMarker->SetMarkerColor(std::get<0>(massGroup));
                theMarker->Draw("same");
                break;
            }
        }
    }



    for(size_t gIt = 0; gIt < theMassGroupList.size(); ++gIt)
    {
        auto& massGroup = std::get<3>(theMassGroupList[gIt]);
        std::cout << "Group\t" << gIt << "\tbin number =\t" << massGroup.countNumberOfBins(mXmYplane) << std::endl;
        
        TBox *theBox = new TBox(massGroup.fMXmin, 37. + (gIt*2), massGroup.fMXmax, 2203. - (gIt*2));
        theBox->SetLineColor(std::get<0>(theMassGroupList[gIt]));
        theBox->SetLineWidth(2);
        theBox->SetFillStyle(0);
        theBox->Draw("same");
    }


    
    return;

}