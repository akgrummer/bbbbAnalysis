#include "TFile.h"
#include "TTree.h"
#include "TPad.h"
#include "TH1F.h"
#include <stdio.h>
#include <iostream>
// using namespace ROOT::Experimental;

// g++  -std=c++17 -I `root-config --incdir`  -o an-scripts/exe/LEE_getMinSigma an-scripts/LEE_getMinSigma.cc `root-config --libs` -O3

// this is a copy of LEE_getMaxSigma BUT
// inverted the significance histograms (limit becomes -limit)
// and cut is less than the -limit
int main(int argc, char** argv) {
    if(argc!=4)
    {
        std::cout<<"Usage: ./an-scripts/exe/LEE_getMinSigma <ifile> <toymin> <toymax>"<<"\n";
        exit(EXIT_FAILURE);
    }


    TString iFileName = argv[1];
    // std::cout<< "File name: "<<iFileName <<"\n";
    std::unique_ptr<TFile> iFile( TFile::Open(iFileName, "read") );

    int toymin=atoi(argv[2]);
    int toymax=atoi(argv[3]);

    TTree *tree = (TTree*)iFile->Get("limit");
    tree->Draw("-limit>>htempData(10000,3.8,10)","toyNum==-1&&!(mX==400&&mY==250)");
    auto htempData = (TH1F*)gPad->GetPrimitive("htempData"); // 1D
    float minDataVal = htempData->GetXaxis()->GetBinCenter(htempData->FindLastBinAbove(0));
    float minValBinContentData = htempData->GetBinContent(htempData->FindLastBinAbove(0));

    minDataVal = -minDataVal;
    tree->Draw("mX>>hmXData(10000,0,2000)",Form("toyNum==-1&&limit<=%f&&!(mX==400&&mY==250)",minDataVal+0.001));
    auto hmXData = (TH1F*)gPad->GetPrimitive("hmXData"); // 1D
    float minmXData= hmXData->GetBinLowEdge(hmXData->FindLastBinAbove(0));

    tree->Draw("mY>>hmYData(10000,0,2000)",Form("toyNum==-1&&limit<=%f&&!(mX==400&&mY==250)",minDataVal+0.001));
    auto hmYData = (TH1F*)gPad->GetPrimitive("hmYData"); // 1D
    float minmYData= hmYData->GetBinLowEdge(hmYData->FindLastBinAbove(0));


    if (toymin==1){
    std::cout<< "Data largest local sign: "<<"\n";
    std::cout<< minValBinContentData<< " ";
    std::cout<< minDataVal <<" ";
    std::cout<< minmXData <<" ";
    std::cout<< minmYData <<"\n";
    }

    std::cout<< "MC toys below min local "<<"\n";
    std::cout<< ""<<"\r";

    float tempThreshold;
    tempThreshold=-3.5;

    for (int atoy=toymin; atoy<toymax; atoy++){
        // tree->Draw("-limit>>htemp(10000,3.8,10)",Form("toyNum==%d&&!(mX==400&&mY==250)&&!(mX==600&&mY==150)&&!(mX==600&&mY==125)",atoy));
        tree->Draw("-limit>>htemp(10000,3.8,10)",Form("toyNum==%d&&!(mX==400&&mY==250)",atoy));
        auto htemp = (TH1F*)gPad->GetPrimitive("htemp"); // 1D
        float minVal = htemp->GetXaxis()->GetBinCenter(htemp->FindLastBinAbove(0));
        float minValBinContent= htemp->GetBinContent(htemp->FindLastBinAbove(0));

        minVal = -minVal;
        // tree->Draw("mX>>hmX(10000,0,2000)",Form("toyNum==%d&&limit<=%f&&!(mX==400&&mY==250)&&!(mX==600&&mY==150)&&!(mX==600&&mY==125)",atoy,minVal+0.001));
        tree->Draw("mX>>hmX(10000,0,2000)",Form("toyNum==%d&&limit<=%f&&!(mX==400&&mY==250)",atoy,minVal+0.001));
        auto hmX = (TH1F*)gPad->GetPrimitive("hmX"); // 1D
        float minmX= hmX->GetBinLowEdge(hmX->FindLastBinAbove(0));

        // tree->Draw("mY>>hmY(10000,0,2000)",Form("toyNum==%d&&limit<=%f&&!(mX==400&&mY==250)&&!(mX==600&&mY==150)&&!(mX==600&&mY==125)",atoy,minVal+0.001));
        tree->Draw("mY>>hmY(10000,0,2000)",Form("toyNum==%d&&limit<=%f&&!(mX==400&&mY==250)",atoy,minVal+0.001));
        auto hmY = (TH1F*)gPad->GetPrimitive("hmY"); // 1D
        float minmY= hmY->GetBinLowEdge(hmY->FindLastBinAbove(0));

        if (minVal<minDataVal){
        // if (minVal<tempThreshold){
            std::cout<< "\n";
            std::cout<< minValBinContent << " ";
            std::cout<< minVal << " ";
            std::cout<< minmX << " ";
            std::cout<< minmY <<"\n";
        }
        else{
            std::cout<< "\r" << Form("computing toy: %d",atoy) <<std::flush;
        }
    }
    std::cout<< ""<<"\n";

    return 0;
}

