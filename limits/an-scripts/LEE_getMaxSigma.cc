#include "ROOT/TDataFrame.hxx"
#include "TFile.h"
#include "TTree.h"
#include "TPad.h"
#include <stdio.h>
using namespace ROOT::Experimental;

// g++  -std=c++17 -I `root-config --incdir`  -o an-scripts/exe/LEE_getMaxSigma an-scripts/LEE_getMaxSigma.cc `root-config --libs` -O3

int main(int argc, char** argv) {
    if(argc!=2)
    {
        std::cout<<"Usage: ./an-scripts/exe/LEE_getMaxSigma <ifile>"<<"\n";
        exit(EXIT_FAILURE);
    }

    TString iFileName = argv[1];
    std::unique_ptr<TFile> iFile( TFile::Open(iFileName, "read") );

    TTree *tree = (TTree*)iFile->Get("limit");
    tree->Draw("limit>>htempData(10000,0,5)","toyNum==-1");
    auto htempData = (TH1F*)gPad->GetPrimitive("htempData"); // 1D
    float maxDataVal = htempData->GetXaxis()->GetBinCenter(htempData->FindLastBinAbove(0));
    float maxValBinContentData = htempData->GetBinContent(htempData->FindLastBinAbove(0));

    tree->Draw("mX>>hmXData(10000,0,2000)",Form("toyNum==-1&&limit>=%f",maxDataVal-0.001));
    auto hmXData = (TH1F*)gPad->GetPrimitive("hmXData"); // 1D
    float maxmXData= hmXData->GetBinLowEdge(hmXData->FindLastBinAbove(0));

    tree->Draw("mY>>hmYData(10000,0,2000)",Form("toyNum==-1&&limit>=%f",maxDataVal-0.001));
    auto hmYData = (TH1F*)gPad->GetPrimitive("hmYData"); // 1D
    float maxmYData= hmYData->GetBinLowEdge(hmYData->FindLastBinAbove(0));

    std::cout<< "Data largest local sign: "<<"\n";
    std::cout<< maxValBinContentData<< " ";
    std::cout<< maxDataVal <<" ";
    std::cout<< maxmXData <<" ";
    std::cout<< maxmYData <<"\n";

    std::cout<< "MC toys above max local "<<"\n";
    std::cout<< ""<<"\r";

    for (int atoy=1; atoy<10001; atoy++){
        tree->Draw("limit>>htemp(10000,0,5)",Form("toyNum==%d",atoy));
        auto htemp = (TH1F*)gPad->GetPrimitive("htemp"); // 1D
        float maxVal = htemp->GetXaxis()->GetBinCenter(htemp->FindLastBinAbove(0));
        float maxValBinContent= htemp->GetBinContent(htemp->FindLastBinAbove(0));

        tree->Draw("mX>>hmX(10000,0,2000)",Form("toyNum==%d&&limit>=%f",atoy,maxVal-0.001));
        auto hmX = (TH1F*)gPad->GetPrimitive("hmX"); // 1D
        float maxmX= hmX->GetBinLowEdge(hmX->FindLastBinAbove(0));

        tree->Draw("mY>>hmY(10000,0,2000)",Form("toyNum==%d&&limit>=%f",atoy,maxVal-0.001));
        auto hmY = (TH1F*)gPad->GetPrimitive("hmY"); // 1D
        float maxmY= hmY->GetBinLowEdge(hmY->FindLastBinAbove(0));

        if (maxVal>maxDataVal){
            std::cout<< "\n";
            std::cout<< maxValBinContent << " ";
            std::cout<< maxVal << " ";
            std::cout<< maxmX << " ";
            std::cout<< maxmY <<"\n";
        }
        else{
            std::cout<< "\r" << Form("computing toy: %d",atoy) <<std::flush;
        }
    }
    std::cout<< ""<<"\n";

    return 0;
}

