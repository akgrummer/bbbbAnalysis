#include "Riostream.h"
#include "TH1F.h"
#include "TFile.h"
#include "TROOT.h"
#include "TCanvas.h"
#include <string>
#include <vector>
#include <map>
#include "TChain.h"
#include "TGraph.h"
#include <algorithm>

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

// std::pair<std::string, std::string> getMxMyFromSample(std::string sampleName)
// {
//     std::string mxStringStart = "_MX_";
//     std::string mxStringEnd   = "_NANOAOD_";
//     std::string myStringStart = "_MY_";
//     size_t mxStart = sampleName.find(mxStringStart) + mxStringStart.size();
//     size_t mxEnd   = sampleName.find(mxStringEnd);
//     size_t myStart = sampleName.find(myStringStart) + myStringStart.size();
//     size_t myEnd   = sampleName.size();

//     std::string mx = sampleName.substr(mxStart, mxEnd-mxStart);
//     std::string my = sampleName.substr(myStart, myEnd-myStart);

//     return std::make_pair(mx, my);
// }

float getGenMatchEfficiency(const int year, const int xMass, const int yMass, const float dR)
{
    gROOT->SetBatch(true);

    auto getFileName = [year](std::pair<const int,const int> massPoint) -> std::string
    {
        std::string fileName;
        // if(massPoint.second == 125) fileName = "plotterListFiles/" + std::to_string(year) + "Resonant_NMSSM_XYH_bbbb/HHSignal/FileList_NMSSM_XYH_bbbb_MX_"
        //     + std::to_string(massPoint.first) + "_NANOAOD_v7_Full_MY_" + std::to_string(massPoint.second) + ".txt";
        // else                        fileName = "plotterListFiles/" + std::to_string(year) + "Resonant_NMSSM_XYH_bbbb/Signal/FileList_NMSSM_XYH_bbbb_MX_"
        //     + std::to_string(massPoint.first) + "_NANOAOD_v7_Full_MY_" + std::to_string(massPoint.second) + ".txt";
        // "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_150_rerun.txt" ,
        if ((year==2017) && (massPoint.first==1000) && (massPoint.second==150)){
            fileName = "plotterListFiles/" + std::to_string(year) + "Resonant_NMSSM_XYH_bbbb/Signal/FileList_NMSSM_XYH_bbbb_MX_"
                + std::to_string(massPoint.first) + "_NANOAOD_v7_Full_MY_" + std::to_string(massPoint.second) + "_rerun.txt";}
        else if(massPoint.first==650){
            fileName = "plotterListFiles/MX650/"+ std::to_string(year) +"/Signal/FileList_NMSSM_XToYHTo4B_MX-650_MY-" + std::to_string(massPoint.second)+"_"+ std::to_string(year) +".txt";}
        else {fileName = "plotterListFiles/" + std::to_string(year) + "Resonant_NMSSM_XYH_bbbb/Signal/FileList_NMSSM_XYH_bbbb_MX_"
            + std::to_string(massPoint.first) + "_NANOAOD_v7_Full_MY_" + std::to_string(massPoint.second) + ".txt";}
        return fileName;
    };

    const std::string fileName = getFileName({xMass,yMass});
    const std::string variable = "gen_H1_b1_matchedflag";

    std::vector<std::string> fileList     = splitByLine(fileName    );
    auto theTree     = getChainFromFileList(fileList    , "bbbbTree");

    std::string selection           = "NbJets >= 4 && H1_m > 125-20 && H1_m < 125+20";
    // TString selectionGenBs           = "";
    // "plotterListFiles/MX650/2017/"
    // H1_b1_deepCSV>0.0614 &&  H1_b2_deepCSV>0.0614 && H2_b1_deepCSV>0.0614 && H2_b2_deepCSV>0.0614
    std::string selectionGenMatched = "NbJets >= 4 && H1_m > 125-20 && H1_m < 125+20 && gen_H1_b1_matchedflag >= 0 && gen_H1_b2_matchedflag >= 0 && gen_H2_b1_matchedflag >= 0 && gen_H2_b2_matchedflag >= 0";
    if(yMass == 125) selectionGenMatched = "NbJets >= 4 && H1_m > 125-20 && H1_m < 125+20 && ((gen_H1_b1_matchedflag >= 0 && gen_H1_b2_matchedflag >= 0) || (gen_H1_b1_matchedflag_swapped >= 0 && gen_H1_b2_matchedflag_swapped >= 0)) && ((gen_H2_b1_matchedflag >= 0 && gen_H2_b2_matchedflag >= 0) || (gen_H2_b1_matchedflag_swapped >= 0 && gen_H2_b2_matchedflag_swapped >= 0))";
    std::string deltaR = std::to_string(dR);
    std::string selectionPairMatch = selectionGenMatched + " && sqrt((H1_eta - gen_H1_eta)*(H1_eta - gen_H1_eta) + (H1_phi - gen_H1_phi)*(H1_phi - gen_H1_phi)) <" + deltaR + "&& sqrt((H2_eta - gen_H2_eta)*(H2_eta - gen_H2_eta) + (H2_phi - gen_H2_phi)*(H2_phi - gen_H2_phi)) < " + deltaR;
    // std::string selectionGenMatched = "NbJets >= 4 && H1_m > 125-20 && H1_m < 125+20 && gen_H1_b1_matchedflag >= 0 && gen_H1_b2_matchedflag >= 0";
    // if(yMass == 125) selectionGenMatched = "NbJets >= 4 && H1_m > 125-20 && H1_m < 125+20 && ((gen_H1_b1_matchedflag >= 0 && gen_H1_b2_matchedflag >= 0) || (gen_H1_b1_matchedflag_swapped >= 0 && gen_H1_b2_matchedflag_swapped >= 0))";

    auto sampleName = getSampleNameFromFile(fileName);

    // TH1F *variablePlot = new TH1F((sampleName + "_" + variable).c_str(), ("m_{X} = " + std::to_string(xMass) + " Gev - m_{Y} = " + std::to_string(yMass) + "; m_{X} [GeV]; entries [a.u.]" ).c_str()
    //     , 50, -10, 10);
    // std::string plotMxKinFirCmd = variable + std::string(">>") + sampleName + "_" + variable;
    // theTree->Draw(plotMxKinFirCmd.c_str(), selection.data(), "");


    TH1F *variableGenMatchedPlot = new TH1F((sampleName + "_" + variable + "_getMatched").c_str(), ("m_{X} = " + std::to_string(xMass) + " Gev - m_{Y} = " + std::to_string(yMass) + "; m_{X} [GeV]; entries [a.u.]" ).c_str()
        , 50, -10, 10);
    std::string plotMxKinFirCmdGenMatched = variable + std::string(">>") + sampleName + "_" + variable + "_getMatched";
    theTree->Draw(plotMxKinFirCmdGenMatched.c_str(), selectionGenMatched.data(), "");

    TH1F *variablePairMatchedPlot = new TH1F((sampleName + "_" + variable + "_pairMatched").c_str(), ("m_{X} = " + std::to_string(xMass) + " Gev - m_{Y} = " + std::to_string(yMass) + "; m_{X} [GeV]; entries [a.u.]" ).c_str()
        , 50, -10, 10);

    std::string plotMxKinFirCmdPairMatched = variable + std::string(">>") + sampleName + "_" + variable + "_pairMatched";
    theTree->Draw(plotMxKinFirCmdPairMatched.c_str(), selectionPairMatch.data(), "");

    float eff_val = float(variablePairMatchedPlot->GetEntries())/float(variableGenMatchedPlot->GetEntries());

    delete variableGenMatchedPlot;
    delete variablePairMatchedPlot;

    return eff_val;

}


std::vector<std::string> signalList =
    {
        "tempFileList_MX_650_NANOAOD_MY_60.txt",
        "tempFileList_MX_650_NANOAOD_MY_70.txt",
        "tempFileList_MX_650_NANOAOD_MY_80.txt",
        "tempFileList_MX_650_NANOAOD_MY_90.txt",
        "tempFileList_MX_650_NANOAOD_MY_100.txt",
        "tempFileList_MX_650_NANOAOD_MY_125.txt",
        "tempFileList_MX_650_NANOAOD_MY_150.txt",
        "tempFileList_MX_650_NANOAOD_MY_190.txt",
        "tempFileList_MX_650_NANOAOD_MY_250.txt",
        "tempFileList_MX_650_NANOAOD_MY_300.txt",
        "tempFileList_MX_650_NANOAOD_MY_350.txt",
        "tempFileList_MX_650_NANOAOD_MY_400.txt",
        "tempFileList_MX_650_NANOAOD_MY_450.txt",
        "tempFileList_MX_650_NANOAOD_MY_500.txt",
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_100.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_125.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_150.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_200.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_250.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_300.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_400.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_500.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_60.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_600.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_70.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_700.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_80.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_800.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_90.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_100.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_125.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_150.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_200.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_250.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_300.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_400.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_500.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_600.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_700.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_800.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_90.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_900.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_100.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_1000.txt",
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_125.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_150.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_200.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_250.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_300.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_400.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_500.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_600.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_700.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_800.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_90.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_900.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_100.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_1000.txt",
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_1200.txt",
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_125.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_150.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_200.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_250.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_300.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_400.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_500.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_600.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_700.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_800.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_90.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_900.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_100.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_1000.txt",
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_1200.txt",
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_125.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_1400.txt",
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_150.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_200.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_250.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_300.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_400.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_500.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_600.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_700.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_800.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_90.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_900.txt" ,
        // // "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_100.txt" ,
        // // "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_1000.txt",
        // // "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_1200.txt",
        // // "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_125.txt" ,
        // // "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_1400.txt",
        // // "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_150.txt" ,
        // // "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_1600.txt",
        // // "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_200.txt" ,
        // // "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_250.txt" ,
        // // "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_300.txt" ,
        // // "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_400.txt" ,
        // // "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_500.txt" ,
        // // "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_600.txt" ,
        // // "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_700.txt" ,
        // // "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_800.txt" ,
        // // "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_90.txt"  ,
        // // "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_900.txt" ,
        // // "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_100.txt" ,
        // // "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_1000.txt",
        // // "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_1200.txt",
        // // "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_125.txt" ,
        // // "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_1400.txt",
        // // "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_150.txt" ,
        // // "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_1600.txt",
        // // "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_1800.txt",
        // // "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_200.txt" ,
        // // "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_250.txt" ,
        // // "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_300.txt" ,
        // // "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_400.txt" ,
        // // "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_500.txt" ,
        // // "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_600.txt" ,
        // // "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_700.txt" ,
        // // "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_800.txt" ,
        // // "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_90.txt"  ,
        // // "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_900.txt" ,
        // // "FileList_NMSSM_XYH_bbbb_MX_300_NANOAOD_v7_Full_MY_100.txt"  ,
        // // "FileList_NMSSM_XYH_bbbb_MX_300_NANOAOD_v7_Full_MY_125.txt"  ,
        // // "FileList_NMSSM_XYH_bbbb_MX_300_NANOAOD_v7_Full_MY_150.txt"  ,
        // // "FileList_NMSSM_XYH_bbbb_MX_300_NANOAOD_v7_Full_MY_60.txt"   ,
        // // "FileList_NMSSM_XYH_bbbb_MX_300_NANOAOD_v7_Full_MY_70.txt"   ,
        // // "FileList_NMSSM_XYH_bbbb_MX_300_NANOAOD_v7_Full_MY_80.txt"   ,
        // // "FileList_NMSSM_XYH_bbbb_MX_300_NANOAOD_v7_Full_MY_90.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_400_NANOAOD_v7_Full_MY_100.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_400_NANOAOD_v7_Full_MY_125.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_400_NANOAOD_v7_Full_MY_150.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_400_NANOAOD_v7_Full_MY_200.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_400_NANOAOD_v7_Full_MY_250.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_400_NANOAOD_v7_Full_MY_60.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_400_NANOAOD_v7_Full_MY_70.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_400_NANOAOD_v7_Full_MY_80.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_400_NANOAOD_v7_Full_MY_90.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_500_NANOAOD_v7_Full_MY_100.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_500_NANOAOD_v7_Full_MY_125.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_500_NANOAOD_v7_Full_MY_150.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_500_NANOAOD_v7_Full_MY_200.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_500_NANOAOD_v7_Full_MY_250.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_500_NANOAOD_v7_Full_MY_300.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_500_NANOAOD_v7_Full_MY_60.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_500_NANOAOD_v7_Full_MY_70.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_500_NANOAOD_v7_Full_MY_80.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_500_NANOAOD_v7_Full_MY_90.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_MY_100.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_MY_125.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_MY_150.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_MY_200.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_MY_250.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_MY_300.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_MY_400.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_MY_60.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_MY_70.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_MY_80.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_MY_90.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_100.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_125.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_150.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_200.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_250.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_300.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_400.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_500.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_60.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_70.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_80.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_90.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_100.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_125.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_150.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_200.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_250.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_300.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_400.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_500.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_60.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_600.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_70.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_80.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_90.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_100.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_125.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_150.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_200.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_250.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_300.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_400.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_500.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_60.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_600.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_70.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_700.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_80.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_90.txt"   ,
    };


std::pair<int, int> getMxMyFromSample(std::string sampleName)
{
    std::string mxStringStart = "_MX_";
    std::string mxStringEnd   = "_NANOAOD_";
    std::string myStringStart = "_MY_";
    std::string myStringEnd = ".txt";
    size_t mxStart = sampleName.find(mxStringStart) + mxStringStart.size();
    size_t mxEnd   = sampleName.find(mxStringEnd);
    size_t myStart = sampleName.find(myStringStart) + myStringStart.size();
    size_t myEnd   = sampleName.find(myStringEnd);

    std::string mx = sampleName.substr(mxStart, mxEnd-mxStart);
    std::string my = sampleName.substr(myStart, myEnd-myStart);

    // std::cout<<"Aidan: "<< "MX: "<< mx.c_str()<< " MY: "<< my.c_str() << std::endl;

    return std::make_pair(atoi(mx.c_str()), atoi(my.c_str()));
}

void GetGenMatch_higgsPair_2024Aug_tree()
{
    // std::unique_ptr<TFile> myFile( TFile::Open("Plots/PairMatchedEff/eff_vals.root", "RECREATE") );
    std::unique_ptr<TFile> myFile( TFile::Open("Plots/PairMatchedEff/eff_vals_1p45.root", "RECREATE") );
    auto otree = std::make_unique<TTree>("otree", "pairing efficiency tree");
    std::vector<int> yearList {2016, 2017, 2018};
    // std::vector<float> dRList {0.05, 0.1,0.15, 0.2,0.25, 0.3,0.35, 0.4,0.45, 0.5,0.55, 0.6,0.65, 0.7,0.75, 0.8,0.85, 0.9,0.95, 1.0,1.05, 1.1,1.15, 1.2};
    std::vector<float> dRList {1.25, 1.3, 1.35, 1.4, 1.45};
    // std::vector<float> dRList {0.3};
    float branch_dR;
    int branch_year;
    int branch_mX;
    int branch_mY;
    float branch_eff;
    otree->Branch("dR", &branch_dR);
    otree->Branch("year", &branch_year);
    otree->Branch("mX", &branch_mX);
    otree->Branch("mY", &branch_mY);
    otree->Branch("eff", &branch_eff);

    std::map<int, std::vector<float>> thePointMapList;
    for(const auto& sampleName : signalList)
    {
        auto pairMxMy = getMxMyFromSample(sampleName);
        float mX = pairMxMy.first ;
        float mY = pairMxMy.second;
        if(thePointMapList.find(mX) == thePointMapList.end()) thePointMapList[mX] = std::vector<float>();
        thePointMapList[mX].push_back(mY);
    }

    for(const auto year : yearList)
    {
        branch_year = year;
        for(const auto& mXList : thePointMapList)
        {
            std::vector<float> mYlist = mXList.second;
            std::sort(mYlist.begin(),mYlist.end());
            float mX = mXList.first;
            branch_mX = mX;
            // std::vector<float> genMatchEfficiencyList;
            for(const auto mY : mYlist)
            {
                branch_mY = mY;
                for(const auto dR : dRList)
                {
                    branch_dR = dR;
                    branch_eff = getGenMatchEfficiency(year, mX, mY, dR);
                    otree->Fill();
                }
            }
            std::cout<<"done with: year"<<year<<" mX: "<< mX<< std::endl;
            // std::cout<<genMatchEfficiencyList[0]<<std::endl;

            // TGraph theGraph(mYlist.size(), mYlist.data(), genMatchEfficiencyList.data());
            // theGraph.SetMarkerColor(kRed);
            // theGraph.SetLineColor  (kRed);
            // theGraph.GetYaxis()->SetRangeUser(0.,1.);
            // theGraph.SetLineWidth(2);
            // theGraph.SetMarkerStyle(20);
            // theGraph.SetMarkerSize(0.8);
            // theGraph.SetTitle(("m_{X} = " + std::to_string(int(mX)) + " GeV, " + std::to_string(year) + "; m_{Y} [GeV]; b-jet pairing efficiency").c_str());
            // theGraph.GetYaxis()->SetTitleOffset(1.2);

            // TCanvas theCanvas(("GenMatching_Higgs_mX_" + std::to_string(int(mX)) + "_Run_" + std::to_string(year)).c_str(), "theCanvas");
            // theCanvas.SetTicks(1,1);
            // theGraph.Draw("apl");
            // theCanvas.SaveAs(("Plots/PairMatchedEff/" + std::string(theCanvas.GetName()) + ".pdf").c_str());
            // theCanvas.Close();
        }
    }
    otree->Write();
}


