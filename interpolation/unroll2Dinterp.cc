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
            // if(!isBkg)
            // {
            //     value*=0.9;
            //     error*=0.9;
            // }
            the1Dplot->SetBinContent(newBinNumber, value);
            the1Dplot->SetBinError(newBinNumber++, error);
        }
    }
    return the1Dplot;
}

TH1F *rebinAndUnroll(TH2F *the2Dplot){

    uint nXbin = the2Dplot->GetNbinsX();
    uint nYbin = the2Dplot->GetNbinsY();
    const double* xBinArray = the2Dplot->GetXaxis()->GetXbins()->GetArray();
    const double* yBinArray = the2Dplot->GetYaxis()->GetXbins()->GetArray();

    TH2F *theRebinnedPlot = new TH2F(theRebinnedPlotName.data(),theRebinnedPlotName.data(),nXbin,xBinArray,nYbin,yBinArray);
    FillRebinnedPlot(theCurrent2Dplot,theRebinnedPlot);
    TH1F* the1Dplot = UnrollPlot(theRebinnedPlot, isBkg);
    the1Dplot->Write(the1Dplot->GetName(), TObject::kOverwrite);
    return the1Dplot;

}

int main(){

    TH1F* the1Dplot = rebinAndUnroll();

}

