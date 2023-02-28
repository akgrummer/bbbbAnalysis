#include "Riostream.h"
#include "TH2F.h"
#include "TH1F.h"
#include "TFile.h"
#include "TArrayD.h"
#include "TClass.h"
#include "TCollection.h"
#include "TKey.h"
#include "TROOT.h"
#include "TSystem.h"
#include <iostream>
#include <cmath>

// year  -> minEntries per Bin
// 2016  -> 1.0
// 2017  -> 0.3
// 2018  -> 0.7

// g++  -std=c++17 -I `root-config --incdir` -o Unroll2DplotsSubRangeValidationTest Unroll2DplotsSubRangeValidationTest.cc `root-config --libs` -O3

// ./Unroll2DplotsSubRangeValidationTest ..//2016DataPlots_NMSSM_XYH_bbbb_triggerMatchedBKGNorm/outPlotter.root \
sig_privateMC_NMSSM_bbbb_MX_700_MY_300/selectionbJetsAndTrigger_SignalRegion/sig_privateMC_NMSSM_bbbb_MX_700_MY_300_selectionbJetsAndTrigger_SignalRegion_HH_m_H2_m

// ./Unroll2DplotsSubRangeValidationTest ..//2016DataPlots_NMSSM_XYH_bbbb_triggerMatchedBKGNorm/outPlotter.root \
data_BTagCSV/selectionbJetsAndTrigger_SignalRegion/data_BTagCSV_selectionbJetsAndTrigger_SignalRegion_HH_m_H2_m

//g++  -std=c++17 -I `root-config --incdir` -o Unroll2DplotsSubRangeValidationTest Unroll2DplotsSubRangeValidationTest.cc `root-config --libs` -O3 && ./Unroll2DplotsSubRangeValidationTest ../plotResults/2016DataPlots_NMSSM_XYH_bbbb/outPlotter.root data_BTagCSV_BackgroundTriggerMatched selectionbJetsAndTrigger_SignalRegion HH_m_H2_m

// ./scripts/Unroll2DplotsSubRangeValidationTest 2016DataPlots_NMSSM_XYH_bbbb_PtRegressedAndHigherLevel_VCR_30_VSR_10/outPlotter.root data_BTagCSV_dataDriven selectionbJetsAndTrigger_3bTag_SignalRegion HH_m_H2_m selectionbJetsAndTrigger_3bTag_ControlRegionBlinded selectionbJetsAndTrigger_3bTag_SideBandBlinded selectionbJetsAndTrigger_4bTag_ControlRegionBlinded selectionbJetsAndTrigger_4bTag_SideBandBlinded selectionbJetsAndTrigger_4bTag_SignalRegion
// ./scripts/Unroll2DplotsSubRangeValidationTest 2016DataPlots_NMSSM_XYH_bbbb_PtRegressedAndHigherLevel_VCR_30_VSR_10/outPlotter.root data_BTagCSV_dataDriven_noTrigMatch selectionbJets_3bTag_SignalRegion HH_m_H2_m selectionbJets_3bTag_ControlRegionBlinded selectionbJets_3bTag_SideBandBlinded selectionbJets_4bTag_ControlRegionBlinded selectionbJets_4bTag_SideBandBlinded selectionbJets_4bTag_SignalRegion
// ./scripts/Unroll2DplotsSubRangeValidationTest 2016DataPlots_NMSSM_XYH_bbbb_Fast/outPlotter.root data_BTagCSV_dataDriven selectionbJets_SignalRegion HH_m_H2_m selectionbJets_ControlRegionBlinded selectionbJets_SideBandBlinded

// float konigsbergLine = 800;

float higgsMass = 120;
float mYmin =    0.;
float mYmax = 2400.;
float mXmin;
float mXmax;
bool firstTime = true;

//-------------------------------------------------------------------------------------------------------------------------------------//

bool isNeededBin(TH2F *the2Dplot, uint xBin, uint yBin)
{
    float mX = the2Dplot->GetXaxis()->GetBinCenter(xBin);
    float mY = the2Dplot->GetYaxis()->GetBinCenter(yBin);
    if(mY < mYmin || mY > mYmax) return false;

    // if( (mX - mY > higgsMass) && (mX - mY < higgsMass + konigsbergLine) )
    // {
    //     return true;
    // }
    if( mX - mY < higgsMass)  return false;
    if( mX > 1200 && mY < 80) return false;
    if( mY > 95 && mY < 155) return false;
    if( mX > mXmax) return false;
    if( mX < mXmin) return false;
    // look at a single mass point:
    // if( ( mY<200 || mY>500 ) || ( mX<400 || mX>704 ) ) return false;
    // look at a mass slice:
    // if( ( mX>400 ) ) return false;
    // if( ( mX<212 || mX>800 ) ) return false;
    // if( ( mX<280 || mX>800 ) ) return false;


    return true;
}

//-------------------------------------------------------------------------------------------------------------------------------------//

void FillRebinnedPlot (TH2F *the2DsourcePlot, TH2F *the2DtargetPlot)
{

    for(uint xBin = 1; xBin <= the2DsourcePlot->GetNbinsX(); xBin++)
    {
        for(uint yBin = 1; yBin <= the2DsourcePlot->GetNbinsY(); yBin++)
        {
            uint newXBin = the2DtargetPlot->GetXaxis()->FindBin(the2DsourcePlot->GetXaxis()->GetBinCenter(xBin));
            uint newYBin = the2DtargetPlot->GetYaxis()->FindBin(the2DsourcePlot->GetYaxis()->GetBinCenter(yBin));
            float previousContent = the2DtargetPlot->GetBinContent(newXBin,newYBin);
            float previousError   = the2DtargetPlot->GetBinError  (newXBin,newYBin);
            the2DtargetPlot->SetBinContent(newXBin,newYBin, previousContent + the2DsourcePlot->GetBinContent(xBin,yBin));
            the2DtargetPlot->SetBinError  (newXBin,newYBin, sqrt(previousError*previousError + the2DsourcePlot->GetBinError(xBin,yBin)*the2DsourcePlot->GetBinError(xBin,yBin)));
        }
    }
}

//-------------------------------------------------------------------------------------------------------------------------------------//

void Rebin2DPlot(TH2F *&the2Dplot, float minNumberOfEntries, bool rebinX=true, uint xBinStart=1, uint yBinStart=1)
{
    std::cout<<"Rebinning\n";
  
    uint nXbin = the2Dplot->GetNbinsX();
    uint nYbin = the2Dplot->GetNbinsY();
    the2Dplot->SetName("oldPlot");
    
    uint xBin = xBinStart;
    uint yBin = yBinStart;

    bool allNeededBinsAreNotEmpty = true;
    for(xBin = xBinStart; xBin <= nXbin; xBin++)
    {
        for(yBin = yBinStart; yBin <= nYbin; yBin++)
        {
            if(isNeededBin(the2Dplot, xBin, yBin) && the2Dplot->GetBinContent(xBin,yBin) <= minNumberOfEntries)
            {
                allNeededBinsAreNotEmpty = false;
                std::cout << "First empty needed bin = " << xBin << " - " << yBin << std::endl;
                break;
            }
        }

        if(!allNeededBinsAreNotEmpty) break;
    }

    if(allNeededBinsAreNotEmpty) return;

    xBinStart = xBin;
    yBinStart = yBin;

    TArrayD theOriginalBinArray;
    TArrayD theUntouchedBinArray;
    uint binForRebinStart;
    uint binListSize = 0;
    const double *xBinArray;
    const double *yBinArray;
    if(rebinX)
    {
        theOriginalBinArray = *the2Dplot->GetXaxis()->GetXbins();
        if(theOriginalBinArray.GetSize() == 0)
        {
            std::cout<<"Empty\n";
            double binArray[nXbin+1];
            for(xBin = 1; xBin <= nXbin; xBin++)
            {
                binArray[xBin-1] = the2Dplot->GetXaxis()->GetBinLowEdge(xBin);
            }
            binArray[nXbin] = the2Dplot->GetXaxis()->GetBinUpEdge(nXbin);
            theOriginalBinArray.Set(nXbin+1,binArray);
        }

        theUntouchedBinArray = *the2Dplot->GetYaxis()->GetXbins();
        if(theUntouchedBinArray.GetSize() == 0)
        {
            std::cout<<"Empty\n";
            double binArray[nYbin+1];
            for(yBin = 1; yBin <= nYbin; yBin++)
            {
                binArray[yBin-1] = the2Dplot->GetYaxis()->GetBinLowEdge(yBin);
            }
            binArray[nYbin] = the2Dplot->GetYaxis()->GetBinUpEdge(nYbin);
            theUntouchedBinArray.Set(nYbin+1,binArray);
        }

        binForRebinStart = xBinStart;
    }
    else
    {

        theUntouchedBinArray = *the2Dplot->GetXaxis()->GetXbins();
        if(theUntouchedBinArray.GetSize() == 0)
        {
            double binArray[nXbin+1];
            for(xBin = 1; xBin <= nXbin; xBin++)
            {
                binArray[xBin-1] = the2Dplot->GetXaxis()->GetBinLowEdge(xBin);
            }
            binArray[nXbin] = the2Dplot->GetXaxis()->GetBinUpEdge(nXbin);
            theUntouchedBinArray.Set(nXbin+1,binArray);

            for(uint i=0; i<nXbin; ++i) std::cout<<binArray[i]<<" - ";
            std::cout<<std::endl;
        }

        theOriginalBinArray = *the2Dplot->GetYaxis()->GetXbins();
        if(theOriginalBinArray.GetSize() == 0)
        {
            double binArray[nYbin+1];
            for(yBin = 1; yBin <= nYbin; yBin++)
            {
                binArray[yBin-1] = the2Dplot->GetYaxis()->GetBinLowEdge(yBin);
            }
            binArray[nYbin] = the2Dplot->GetYaxis()->GetBinUpEdge(nYbin);
            theOriginalBinArray.Set(nYbin+1,binArray);
        }

        binForRebinStart = yBinStart;
    }

    std::cout<<"Axis " << (rebinX ? "X" : "Y") << " number of bins = " << theOriginalBinArray.GetSize()<<std::endl;
    std::cout<<"First empty bin = " << binForRebinStart <<std::endl;
    double theBinList[theOriginalBinArray.GetSize()];

    //Because it is a great idea
    for(uint bin = 0; bin<theOriginalBinArray.GetSize(); ++bin)
    {
        if(int(bin) < int(binForRebinStart-2)) theBinList[binListSize] = theOriginalBinArray.At(bin);
        else
        {
            // bin += rebinX ? 3 : 1; //skip one more bin
            bin += 1;
            theBinList[binListSize] = theOriginalBinArray.At(bin);
            // if(bin >= theOriginalBinArray.GetSize() - (rebinX ? 4 : 2))
            if(bin >= theOriginalBinArray.GetSize() - 2)
            {
                theBinList[binListSize] = theOriginalBinArray.At(theOriginalBinArray.GetSize()-1);
                break;
            }        
            //if just 1 bin remains, I merge it with the last one
        }
        binListSize++;
    }
    std::cout<<"New number of Bins = " <<binListSize<<std::endl;
    for(uint i=0; i<binListSize; ++i) std::cout<<theBinList[i]<<" - ";
    std::cout<<std::endl;

    uint xBinListSize;
    uint yBinListSize;
    if(rebinX)
    {
        xBinListSize = binListSize;
        yBinListSize = the2Dplot->GetNbinsY() + 1;
        xBinArray = theBinList;
        yBinArray = theUntouchedBinArray.GetArray();
    }
    else
    {
        xBinListSize = the2Dplot->GetNbinsX() + 1;
        yBinListSize = binListSize;
        xBinArray = theUntouchedBinArray.GetArray();
        yBinArray = theBinList;
    }

    TH2F *theRebinnedPlot = new TH2F("newPlot","newPlot",xBinListSize-1,xBinArray,yBinListSize-1,yBinArray);
    theRebinnedPlot->SetDirectory(0);

    FillRebinnedPlot(the2Dplot,theRebinnedPlot);

    delete the2Dplot;
    the2Dplot = theRebinnedPlot;

    Rebin2DPlot(the2Dplot, minNumberOfEntries, !rebinX, xBinStart, yBinStart);

}

//-------------------------------------------------------------------------------------------------------------------------------------//

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
    std::string unRolledPlotName = std::string(the2Dplot->GetName()) + "_Unrolled";
    TH1F *the1Dplot = new TH1F(unRolledPlotName.data(),unRolledPlotName.data(),totalNumberOfBins,0, totalNumberOfBins);
    the1Dplot->SetDirectory(0);

    uint newBinNumber = 1;
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
            // if(isBkg)
            // {
                // // value*=0.9;
                // error*=10.;
            // }
            the1Dplot->SetBinContent(newBinNumber, value);
            the1Dplot->SetBinError(newBinNumber, error);
            newBinNumber++;
        }
    }
    return the1Dplot;
}

//-------------------------------------------------------------------------------------------------------------------------------------//

int main(int argc, char *argv[])
{

    std::map<int, std::pair<float, float>> theMassGroupList;
    theMassGroupList[0] = std::make_pair(212.,  800.);
    theMassGroupList[1] = std::make_pair(300., 1000.);
    theMassGroupList[2] = std::make_pair(450., 1200.);
    theMassGroupList[3] = std::make_pair(600., 1600.);
    theMassGroupList[4] = std::make_pair(950., 2320.);

    gSystem->ResetSignal(kSigSegmentationViolation, kTRUE);

    if(argc < 6)
    {
        std::cout << "Usage: ./Unroll2DplotsSubRangeValidationTest <fileName> <dataset> <selection> <variable> <minMumberOfEntries> <massGroup> <otherSelectionToUnroll - optional>" << std::endl;
        return EXIT_FAILURE;
    }

    std::string dataDataset = argv[2];
    std::string selection   = argv[3];
    std::string variable    = argv[4];
    float minNumberOfEntries  = atof(argv[5]);
    int massGroupToUse  = atof(argv[6]);
    std::vector<std::string> selectionsToUnrollList = {selection};
    for(uint i=7; i<argc; ++i) selectionsToUnrollList.push_back(argv[i]);
    std::string inputFileName = argv[1];
    TFile theInputFile (inputFileName.c_str() );

    // std::string outputFileName = inputFileName.substr(0,inputFileName.find(".root")) + "_rebinned";
    
    float integralBackgroundPlot = -1.;

    for(const auto& massGroup : theMassGroupList)
    {
        if(massGroupToUse != massGroup.first) continue;
        mXmin    = massGroup.second.first ;
        mXmax    = massGroup.second.second;
        std::string outputFileName = inputFileName.substr(0,inputFileName.find(".root")) + "_massGroup" + std::to_string(massGroup.first) + ".root";
        TFile theOutputFile(outputFileName.c_str(), "RECREATE");
        std::string dataHistogramName = dataDataset + "/" + selection + "/" + dataDataset + "_" + selection + "_"  + variable;
        TH2F *the2Dplot = (TH2F*)theInputFile.Get(dataHistogramName.data());
        the2Dplot->SetDirectory(0);
    
        // Rebin2DPlot(the2Dplot, minNumberOfEntries);

        uint nXbin = the2Dplot->GetNbinsX();
        uint nYbin = the2Dplot->GetNbinsY();
        const double* xBinArray = the2Dplot->GetXaxis()->GetXbins()->GetArray();
        const double* yBinArray = the2Dplot->GetYaxis()->GetXbins()->GetArray();
        // std::cout<<__PRETTY_FUNCTION__<<__LINE__<<std::endl;

        TIter next(theInputFile.GetListOfKeys());
        TKey *key;
        // std::cout<<__PRETTY_FUNCTION__<<__LINE__<<std::endl;

        while ((key = (TKey*)next())) 
        {
            TClass *cl = gROOT->GetClass(key->GetClassName());
            if (!cl->InheritsFrom("TDirectoryFile")) continue;
            std::string theCurrentDataDataset = key->ReadObj()->GetName();
            theOutputFile.mkdir(theCurrentDataDataset.c_str());
            // if(theCurrentDataDataset != "sig_NMSSM_bbbb_MX_900_MY_150") continue;
            std::cout << theCurrentDataDataset <<std::endl;
            for(const auto& selectionName : selectionsToUnrollList)
            {
                theInputFile.cd();
                theInputFile.cd((theCurrentDataDataset + "/" + selectionName).c_str());
                theOutputFile.mkdir((theCurrentDataDataset + "/" + selectionName).c_str());
                std::string theCurrentDirectory = theCurrentDataDataset + "/" + selectionName + "/";
                std::string theCurrentHistogramName = theCurrentDataDataset + "_" + selectionName + "_"  + variable;
                TIter nextHistogram(gDirectory->GetListOfKeys());
                TKey *keyHistogram;

                while ((keyHistogram = (TKey*)nextHistogram())) 
                {
                    std::string theCurrentHistogramFullName = keyHistogram->ReadObj()->GetName();
                    TClass *cl2 = gROOT->GetClass(keyHistogram->GetClassName());
                    if (!cl2->InheritsFrom("TH2F")) continue;
                    if(theCurrentHistogramFullName.find(theCurrentHistogramName) == std::string::npos) continue;
                    if(theCurrentHistogramFullName.find("_Rebinned") != std::string::npos) continue;
                    // std::cout<<theCurrentHistogramFullName<<" - "<<theCurrentHistogramName<<std::endl;

                    TH2F *theCurrent2Dplot = (TH2F*)theInputFile.Get((theCurrentDirectory+theCurrentHistogramFullName).data());
                    bool isBkg = false;
                    if(theCurrentDataDataset == dataDataset) isBkg = true;
                    std::string theRebinnedPlotName = theCurrentHistogramFullName + "_Rebinned";
                    TH2F *theRebinnedPlot = new TH2F(theRebinnedPlotName.data(),theRebinnedPlotName.data(),nXbin,xBinArray,nYbin,yBinArray);

                    FillRebinnedPlot(theCurrent2Dplot,theRebinnedPlot);

                    // theRebinnedPlot->Write(theRebinnedPlot->GetName(), TObject::kOverwrite);

                    theOutputFile.cd((theCurrentDataDataset + "/" + selectionName).c_str());
                    TH1F* the1Dplot = UnrollPlot(theRebinnedPlot, isBkg);
                    if(selection == selectionName)
                    {
                        if(isBkg)
                        {
                            integralBackgroundPlot = the1Dplot->Integral();
                            std::cout<< "Getting integral reference from " << the1Dplot->GetName() << std::endl;
                            std::cout<< "Integral reference = " << integralBackgroundPlot << std::endl;
                        }
                        // else if( (theCurrentDataDataset == (dataDataset + "_up")) ||  (theCurrentDataDataset == (dataDataset + "_down")))
                        // {
                            // if(integralBackgroundPlot<0.)
                            // {
                                // std::cout<< "integralBackgroundPlot not set!!! Aborting..."<<std::endl;
                                // abort();
                            // }
                            // float originalIntegral = the1Dplot->Integral();
                            // the1Dplot->Scale(integralBackgroundPlot/originalIntegral);
                            // std::cout<< "Scaled plot " << theCurrentDataDataset <<std::endl;
                            // std::cout<< "Original integral = " << originalIntegral <<std::endl;
                            // std::cout<< "Integral from Background Plot = " << integralBackgroundPlot <<std::endl;
                            // std::cout<< "New Integral = " << the1Dplot->Integral() <<std::endl;
                        // }
                    }
                    the1Dplot->Write(the1Dplot->GetName(), TObject::kOverwrite);
                    delete theRebinnedPlot;
                    delete the1Dplot;

                }

            }
        }
        theOutputFile.Close();
    }

    theInputFile.Close();
    std::cout<<"File closed"<<std::endl;

}
