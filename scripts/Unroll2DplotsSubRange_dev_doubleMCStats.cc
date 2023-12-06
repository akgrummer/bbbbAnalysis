#include "Riostream.h"
#include "TH2F.h"
#include "TH1F.h"
#include "TFile.h"
#include "TArrayD.h"
#include "TClass.h"
#include "TCollection.h"
#include "TKey.h"
#include "TObject.h"
#include "TObjectTable.h"
#include "TROOT.h"
#include "TSystem.h"
#include <iostream>
#include <cmath>

// g++  -std=c++17 -I `root-config --incdir` -o Unroll2DplotsSubRange Unroll2DplotsSubRange.cc `root-config --libs` -O3

float higgsMass = 120;
float mYmin =    0.;
float mYmax = 2400.;
float mXmin;
float mXmax;
bool firstTime = true;

//------------------------------------------------------------------------//

bool isNeededBin(TH2F *the2Dplot, uint xBin, uint yBin)
{
    float mX = the2Dplot->GetXaxis()->GetBinCenter(xBin);
    float mY = the2Dplot->GetYaxis()->GetBinCenter(yBin);
    if(mY < mYmin || mY > mYmax) return false;

    if( mX - mY < higgsMass)  return false;
    if( mX > 1200 && mY < 80) return false;
    if( mX > mXmax) return false;
    if( mX < mXmin) return false;


    return true;
}

//---------------------------------------------------------------------------//

TH1F* UnrollPlot(TH2F* the2Dplot, bool isBkg)
{
    uint nXbin = the2Dplot->GetNbinsX();
    uint nYbin = the2Dplot->GetNbinsY();
    // uint numberOfBins = nXbin*nYbin;
    // float theBinArray[numberOfBins+1];
    // theBinArray[0] = the2Dplot->GetXaxis()->GetBinLowEdge(1);

    uint totalNumberOfBins = 0;
    for(uint yBin=1; yBin<=nYbin; ++yBin)
    {
        for(uint xBin=1; xBin<=nXbin; ++xBin)
        {
            if(isNeededBin(the2Dplot, xBin, yBin)) ++totalNumberOfBins;
        }
    }
    if(firstTime)
    {
        std::cout<<"Total number of bins = " << totalNumberOfBins << std::endl;
        firstTime = false;
    }
    // keep the rebinned in the name to match next stages of analysis - legacy reason
    std::string unRolledPlotName = std::string(the2Dplot->GetName()) + "_Rebinned_Unrolled";
    TH1F *the1Dplot = new TH1F(unRolledPlotName.data(),unRolledPlotName.data(),totalNumberOfBins,0, totalNumberOfBins);
    the1Dplot->SetDirectory(0);

    uint newBinNumber = 1;
    float statsFactor=1.;
    // if (isBkg){statsFactor=1.5;}
    for(uint yBin = 1; yBin <= nYbin; yBin++)
    {
        for(uint xBin = 1; xBin <= nXbin; xBin++)
        {
            float mX = the2Dplot->GetXaxis()->GetBinCenter(xBin);
            float mY = the2Dplot->GetYaxis()->GetBinCenter(yBin);
            if(!isNeededBin(the2Dplot, xBin, yBin)) continue;

            float value = the2Dplot->GetBinContent(xBin,yBin);
            float error = the2Dplot->GetBinError(xBin,yBin);
            if(value == 0 && isBkg)
            {
                std::cout<<"This should never happen!!!"<<std::endl;
                value = 1e-5;
                error = 1e-5;
            }
            if(isBkg && 62<mY && mY<188){error = sqrt(error*error + (value*0.1)*(value*0.1));}
            the1Dplot->SetBinContent(newBinNumber, value);
            the1Dplot->SetBinError(newBinNumber++, error*statsFactor);
        }
    }
    // delete the2Dplot;
    return the1Dplot;
}

//-------------------------------------------------------------------------//

int main(int argc, char *argv[])
{

        /* Root.MemStat: 1 */
        /* Root.MemStat.size: -1 */
        /* Root.MemStat.cnt: -1 */
        /* Root.ObjectStat: 1 */
        TObject::SetObjectStat(1);
        // TObject::SetMemStat(1);
    std::map<int, std::pair<float, float>> theMassGroupList;
    theMassGroupList[0] = std::make_pair(340.,  800.);
    theMassGroupList[1] = std::make_pair(340., 1000.);
    theMassGroupList[2] = std::make_pair(450., 1200.);
    theMassGroupList[3] = std::make_pair(600., 1600.);
    theMassGroupList[4] = std::make_pair(950., 1936.);

    gSystem->ResetSignal(kSigSegmentationViolation, kTRUE);

    if(argc < 6)
    {
        std::cout << "Usage: ./Unroll2DplotsSubRange <fileName> <dataset> <selection> <variable> <minMumberOfEntries> <otherSelectionToUnroll - optional>" << std::endl;
        return EXIT_FAILURE;
    }

    std::string inputFileName = argv[1];
    std::string dataDataset = argv[2];
    std::string selection   = argv[3];
    std::string variable    = argv[4];
    std::string groupNumIn    = argv[5];
    int groupNum;
    try {
        std::size_t pos;
        groupNum = std::stoi(groupNumIn, &pos);
        if (pos < groupNumIn.size()) {
            std::cerr << "Trailing characters after number: " << groupNumIn << '\n';
        }
    } catch (std::invalid_argument const &ex) {
        std::cerr << "Invalid number: " << groupNumIn << '\n';
    } catch (std::out_of_range const &ex) {
        std::cerr << "Number out of range: " << groupNumIn << '\n';
    }
    std::vector<std::string> selectionsToUnrollList = {selection};
    for(uint i=6; i<argc; ++i) selectionsToUnrollList.push_back(argv[i]);
    // TFile theInputFile (inputFileName.c_str() );
    std::unique_ptr<TFile> theInputFile( TFile::Open(inputFileName.c_str()) );
    // TFile *theInputFile = TFile::Open(inputFileName.c_str(), "READ");


    float integralBackgroundPlot = -1.;

    // for(const auto& massGroup : theMassGroupList)
    // {
    std::pair<float, float> massGroup = theMassGroupList[groupNum];
        mXmin    = massGroup.first ;
        mXmax    = massGroup.second;
        std::string outputFileName = inputFileName.substr(0,inputFileName.find(".root")) + "_massGroup" + std::to_string(groupNum) + ".root";
        // TFile theOutputFile(outputFileName.c_str(), "RECREATE");
        std::unique_ptr<TFile> theOutputFile( TFile::Open(outputFileName.c_str(), "RECREATE") );
        // TFile *theOutputFile = TFile::Open(outputFileName.c_str(), "RECREATE");
        std::string dataHistogramName = dataDataset + "/" + selection + "/" + dataDataset + "_" + selection + "_"  + variable;
        TH2F *the2Dplot = (TH2F*)theInputFile->Get(dataHistogramName.data());
        the2Dplot->SetDirectory(0);

        uint nXbin = the2Dplot->GetNbinsX();
        uint nYbin = the2Dplot->GetNbinsY();
        const double* xBinArray = the2Dplot->GetXaxis()->GetXbins()->GetArray();
        const double* yBinArray = the2Dplot->GetYaxis()->GetXbins()->GetArray();
        // std::cout<<__PRETTY_FUNCTION__<<__LINE__<<std::endl;

        TList* dirKeys = theInputFile->GetListOfKeys();
        TIter next(dirKeys);
        TKey *key;
        // std::cout<<__PRETTY_FUNCTION__<<__LINE__<<std::endl;

        while ((key = (TKey*)next()))
        {
            TClass *cl = gROOT->GetClass(key->GetClassName());
            if (!cl->InheritsFrom("TDirectoryFile")) continue;
            /* if (!gROOT->GetClass(key->GetClassName())->InheritsFrom("TDirectoryFile")) continue; */
            std::string theCurrentDataDataset = key->GetName();
            theOutputFile->mkdir(theCurrentDataDataset.c_str());
            //std::cout << theCurrentDataDataset <<std::endl;
            for(const auto& selectionName : selectionsToUnrollList)
            {
                theInputFile->cd();
                theInputFile->cd((theCurrentDataDataset + "/" + selectionName).c_str());
                theOutputFile->mkdir((theCurrentDataDataset + "/" + selectionName).c_str());
                std::string theCurrentDirectory = theCurrentDataDataset + "/" + selectionName + "/";
                std::string theCurrentHistogramName = theCurrentDataDataset + "_" + selectionName + "_"  + variable;
                TList* histKeys = gDirectory->GetListOfKeys();
                TIter nextHistogram(histKeys);
                // gObjectTable->Print();
                // abort();
                TKey *keyHistogram;

                while ((keyHistogram = (TKey*)nextHistogram()))
                {
                    std::string theCurrentHistogramFullName = keyHistogram->GetName();
                    TClass *cl2 = gROOT->GetClass(keyHistogram->GetClassName());
                    if (!cl2->InheritsFrom("TH2F")) continue;
                    // if (!gROOT->GetClass(keyHistogram->GetClassName())->InheritsFrom("TH2F")){continue;}
                    if(theCurrentHistogramFullName.find(theCurrentHistogramName) == std::string::npos){continue;}
                    // why is this line needed??? Rebinned should only be in the output file???
                    if(theCurrentHistogramFullName.find("_Rebinned") != std::string::npos){continue;}
                    // std::cout<<theCurrentHistogramFullName<<" - "<<theCurrentHistogramName<<std::endl;

                    TH2F *theCurrent2Dplot = (TH2F*)theInputFile->Get((theCurrentDirectory+theCurrentHistogramFullName).data());
                    bool isBkg = false;
                    if(theCurrentDataDataset == dataDataset) isBkg = true;

                    theOutputFile->cd((theCurrentDataDataset + "/" + selectionName).c_str());
                    TH1F* the1Dplot = UnrollPlot(theCurrent2Dplot, isBkg);
                    if(selection == selectionName)
                    {
                        if(isBkg)
                        {
                            integralBackgroundPlot = the1Dplot->Integral();
                            std::cout<< "Getting integral reference from " << the1Dplot->GetName() << std::endl;
                            std::cout<< "Integral reference = " << integralBackgroundPlot << std::endl;
                        }
                        else if( (theCurrentDataDataset == (dataDataset + "_up")) ||  (theCurrentDataDataset == (dataDataset + "_down")))
                        {
                            if(integralBackgroundPlot<0.)
                            {
                                std::cout<< "integralBackgroundPlot not set!!! Aborting..."<<std::endl;
                                abort();
                            }
                            float originalIntegral = the1Dplot->Integral();
                            the1Dplot->Scale(integralBackgroundPlot/originalIntegral);
                            std::cout<< "Scaled plot " << theCurrentDataDataset <<std::endl;
                            std::cout<< "Original integral = " << originalIntegral <<std::endl;
                            std::cout<< "Integral from Background Plot = " << integralBackgroundPlot <<std::endl;
                            std::cout<< "New Integral = " << the1Dplot->Integral() <<std::endl;
                        }
                    }
                    the1Dplot->Write(the1Dplot->GetName(), TObject::kOverwrite);
                    delete theCurrent2Dplot;
                    delete the1Dplot;
                }
                histKeys->Clear();
            }
        }
        dirKeys->Clear();
        // std::cout<<"close ofile here"<<std::endl;
        /* Root.MemStat: 1 */
        /* Root.MemStat.size: -1 */
        /* Root.MemStat.cnt: -1 */
        /* Root.ObjectStat: 1 */
        // gSystem->GetProcInfo();
        // TObjectTable myTable;
        // myTable.Print();
        // MemInfo_t memInfo;
        // gSystem->GetMemInfo(&memInfo);
        gObjectTable->Print();
        Int_t memUsage = 0;
        theOutputFile->Close();
        std::cout<<"ofile closed"<<std::endl;
        // std::cout<<"try remove file from gROOT"<<std::endl;
        // gROOT->GetListOfFiles()->Remove(theOutputFile);
    // }

    // std::cout<<"try remove file from gROOT"<<std::endl;
    //gROOT->GetListOfFiles()->Remove(theInputFile);
    theInputFile->Close();
    std::cout<<"iFile closed"<<std::endl;

}

