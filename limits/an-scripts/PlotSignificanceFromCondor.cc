#include "TH2D.h"
#include "TTree.h"
#include "TFile.h"
#include "iostream"
#include "TGraph.h"
#include "TGraphAsymmErrors.h"
#include <stdlib.h>
#include <map>
#include <tuple>
#include <vector>
#include <fstream>
#include <algorithm>

// #include <boost/program_options.hpp>
// namespace po = boost::program_options;

// g++  -std=c++17 -I `root-config --incdir`  -o PlotLimitsFromCondor PlotLimitsFromCondor.cc `root-config --libs` -O3

std::vector<float> getBinning(const std::vector<float>& listOfPoints)
{
    uint numberOfPoints = listOfPoints.size();
    std::vector<float> binning(numberOfPoints+1);
    for (int point=0; point<numberOfPoints-1; ++point) binning[point+1] = (listOfPoints[point]+listOfPoints[point+1])/2.;
    binning[0]              = 2.*listOfPoints[0] - binning[1];
    binning[numberOfPoints] = 2.*listOfPoints[numberOfPoints-1] - binning[numberOfPoints-1];
    for(auto bin : binning) std::cout << bin << " - ";
    std::cout<<std::endl;
    return binning;
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

std::string getLimitFileName(std::string username, std::string tag, std::string year, std::string signal, std::string option)
{
    std::string fileName = "root://cmseos.fnal.gov//store/user/" + username + "/bbbb_limits/" + tag + "/HistogramFiles_" + year + "/Limit_" + year + "_" + signal + "_" + option + ".root";
    // std::cout<<fileName<<std::endl;
    return fileName;
}


int main(int argc, char** argv)
{

    // gSystem->ResetSignal(kSigSegmentationViolation, kTRUE);

    if(argc < 2 || argc>3)
    {
        std::cout << "Usage: ./PlotLimitsFromCondor <tagName> <impacts [optional]>" << std::endl;
        return EXIT_FAILURE;
    }

    std::string tagName = argv[1];
    bool runImpacts = false;
    if(argc == 3)
    {
        std::string impacts = argv[2];
        if(impacts == "impacts") runImpacts = true;
        else
        {
            std::cout << "Second argument should be 'impacts' " << std::endl;
            return EXIT_FAILURE;
        }

    }

    ////////////////////////////////////////////////////////////////////////

    std::string username = getenv ("USER");

    const std::vector<std::string> yearList          {"2016", "2017", "2018", "RunII"};
    std::vector<std::string> minLimitOptions      {"syst"};
    std::vector<std::string> allLimitOptions = minLimitOptions;

    std::vector<std::string> signalList = splitByLine("prepareModels/listOfSamples.txt");

    std::vector<float> xMassList;
    std::vector<float> yMassList;

    for(const auto& signal : signalList)
    {
        const auto xAndYmass = getMassesFromSignalName(signal);
        if(std::find (xMassList.begin(), xMassList.end(), xAndYmass.first ) == xMassList.end()) xMassList.emplace_back(xAndYmass.first );
        if(std::find (yMassList.begin(), yMassList.end(), xAndYmass.second) == yMassList.end()) yMassList.emplace_back(xAndYmass.second);
    }

    std::sort(xMassList.begin(), xMassList.end());
    std::sort(yMassList.begin(), yMassList.end());

    auto xBinning = getBinning(xMassList);
    auto yBinning = getBinning(yMassList);
    // for(auto bin : xBinning) std::cout<< bin << " - ";
    // std::cout<<std::endl;
    // for(auto bin : yBinning) std::cout<< bin << " - ";
    // std::cout<<std::endl;
    std::cout<<"Doing custom binning though"<<std::endl;

    xBinning.clear();
    yBinning.clear();
    // binning before mx=650 with different mY values added
    //                       350, 450, 550, 650, 750, 850, 950, 1050, 1150, 1300, 1500, 1700
    xBinning.assign({ 350, 450, 550, 625, 675, 750, 850, 950, 1050, 1150, 1300, 1500, 1700 });
    //                        55, 65, 75, 85, 95, 112.5, 137.5, 175, 225, 275, 350, 450, 550, 650, 750, 850, 950, 1100, 1300, 1500
    yBinning.assign({55, 65, 75, 85, 95, 112.5, 137.5, 175, 225, 275, 325, 375, 425, 470, 550, 650, 750, 850, 950, 1100, 1300, 1500});

    std::map<std::string, std::map<std::string, std::tuple<std::map<std::string, TH2D*>, std::map<float, std::tuple<TGraph*, TGraphAsymmErrors*, TGraphAsymmErrors*, TGraph*>>>>> theFullMapOfPlots;
    std::map<float, std::tuple<TGraph*, TGraphAsymmErrors*, TGraphAsymmErrors*, TGraph*>> mapOfLimitsVsY;

    for(const auto & year : yearList)
    {
        std::vector<std::string> limitOptions;
        if(year == "RunII") limitOptions = minLimitOptions;
        else limitOptions = allLimitOptions;
        for(const auto & option : limitOptions)
        {
            std::map<std::string, TH2D*> the2Dmap;
            the2Dmap["LimitMapCentral"   ] = new TH2D(("LimitMapCentral_"    + year + "_" + option).c_str(), ("Significance "      + year + " " + option + "; m_{X} [GeV]; m_{Y} [GeV]; Significance").c_str(), xBinning.size()-1, xBinning.data(), yBinning.size()-1, yBinning.data());

            std::map<float, std::tuple<TGraph*, TGraphAsymmErrors*, TGraphAsymmErrors*, TGraph*>> the1Dmap;
            for(const auto yMass : yMassList)
            {
                the1Dmap[yMass] = std::make_tuple(new TGraph(), new TGraphAsymmErrors(), new TGraphAsymmErrors(), new TGraph());
                std::get<0>(the1Dmap[yMass])->GetXaxis()->SetTitle("m_{X} [GeV]");
                std::get<0>(the1Dmap[yMass])->SetNameTitle(("LimitMapCentral_" + year + "_" + option + "_massY_" + std::to_string(int(yMass))).c_str(), ("Signficance - " + year + " " + option + " m_{Y} = " + std::to_string(int(yMass))).c_str());
                std::get<0>(the1Dmap[yMass])->GetYaxis()->SetTitle("Significance");

            }
            theFullMapOfPlots[year][option] = {the2Dmap, the1Dmap};

            if(option == "syst" && year == "RunII")
            {
                for(const auto xMass : xMassList)
                {
                    mapOfLimitsVsY[xMass] = std::make_tuple(new TGraph(), new TGraphAsymmErrors(), new TGraphAsymmErrors(), new TGraph());
                    std::get<0>(mapOfLimitsVsY[xMass])->SetNameTitle(("LimitMapCentral_" + year + "_" + option + "_massX_" + std::to_string(int(xMass))).c_str(), ("Significance - " + year + " " + option + " m_{Y} = " + std::to_string(int(xMass))).c_str());
                    std::get<0>(mapOfLimitsVsY[xMass])->GetXaxis()->SetTitle("m_{Y} [GeV]");
                    std::get<0>(mapOfLimitsVsY[xMass])->GetYaxis()->SetTitle("Significance");

                }
            }
        }
    }


    for(const auto& signal : signalList)
    {
        std::cout<<"Reading signal " << signal << std::endl;
        const auto xAndYmass = getMassesFromSignalName(signal);
        float xMass = xAndYmass.first ;
        float yMass = xAndYmass.second;

        for(const auto & year : yearList)
        {
            // if(year == "RunII" && xMass == 1000 && yMass == 150) continue; // TMP !!!!!!!!!!!!!!!!!!!!!
            std::vector<std::string> limitOptions;
            if(year == "RunII") limitOptions = minLimitOptions;
            else limitOptions = allLimitOptions;
            for(const auto & option : limitOptions)
            {
                auto theSignalMap2Dmap = std::get<0>(theFullMapOfPlots[year][option]);
                std::string fileName = getLimitFileName(username, tagName, year, signal, option);
                TFile *theFile = TFile::Open(fileName.c_str());
                if(theFile == nullptr)
                {
                    std::cout<<"File " << fileName << " does not exist" << std::endl;
                    continue;
                }
                TTree *theTree = (TTree*)theFile->Get("limit");
                if(theTree == nullptr)
                {
                    std::cout<<"File " << fileName << " does not have limit tree" << std::endl;
                    continue;
                }
                double limitVal;
                theTree->SetBranchAddress("limit",&limitVal);
                theTree->GetEntry(0); double limitCentral    = limitVal;
                // std::cout<<limitCentral<<std::endl;
                if (limitCentral==0.) limitCentral=0.001;

                // std::cout<<__LINE__<<std::endl;
                // }
                theFile->Close();
                delete theFile;

                // std::cout<<__LINE__<<std::endl;

                theSignalMap2Dmap["LimitMapCentral"]->Fill(xMass,yMass,limitCentral   );
                // std::cout<<__LINE__<<std::endl;

                auto theSignalMap1Dmap = std::get<1>(theFullMapOfPlots[year][option]);

                std::get<0>(theSignalMap1Dmap[yMass])->SetPoint     (std::get<0>(theSignalMap1Dmap[yMass])->GetN()  , xMass, limitCentral);
                // std::cout<<__LINE__<<std::endl;

                if(option == "syst" && year == "RunII")
                {
                    std::get<0>(mapOfLimitsVsY[xMass])->SetPoint     (std::get<0>(mapOfLimitsVsY[xMass])->GetN()  , yMass, limitCentral);
                }
            }
        }
    }


    TFile outputFile(("hists/Signficance/Limits_" + tagName + ".root").c_str(), "RECREATE");
    for(const auto& year : yearList)
    {
                // std::cout<<__LINE__<<std::endl;
        outputFile.mkdir(("Limits_" + year).c_str());
            std::vector<std::string> limitOptions;
        if(year == "RunII") limitOptions = minLimitOptions;
        else limitOptions = allLimitOptions;
        for(const auto& option : limitOptions)
        {
                // std::cout<<__LINE__<<std::endl;
            outputFile.mkdir(("Limits_" + year + "/Option_" + option).c_str());
            outputFile.cd   (("Limits_" + year + "/Option_" + option).c_str());
            std::get<0>(theFullMapOfPlots[year][option])["LimitMapCentral"   ]->Write();
            for(const auto yMass : yMassList)
            {
                // std::cout<<__LINE__<<std::endl;
                std::get<0>(std::get<1>(theFullMapOfPlots[year][option])[yMass])->Write();
            }
            if(option == "syst" && year == "RunII")
            {
                for(const auto xMass : xMassList)
                {
                // std::cout<<__LINE__<<std::endl;
                    std::get<0>(mapOfLimitsVsY[xMass])->Write();
                }
            }
                // std::cout<<__LINE__<<std::endl;
            outputFile.cd();
        }
    }

    return EXIT_SUCCESS;

}
