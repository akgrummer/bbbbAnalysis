#include "HistFileClass.h"
using namespace std;

//Default constructor
HistFile::HistFile(TString itreename, string idir, vector<string> ifiles, TString odir, TString ofilename )
{
    nselected= 0;
    std::cout << "### Making ROOT Histograms with HistFileClass ###\n\n";
    ofile = new TFile(odir+ofilename, "RECREATE");
    chain=new TChain(itreename.Data(), "chainname");
    std::cout << "Will create file: " << odir+ofilename << std::endl;
    std::cout<< "input directory: " << idir <<"\n";
    std::cout << "loading input root files..." << std::endl;
    for (const auto & file : ifiles)
    {
        ipath = idir+file;
        chain->Add(ipath.data());
    }
    //itree = (TTree*)ifile->Get("bbbbTree");
    htitle= "";
    hname= "";
    hweight= "";
    hweightName= "";
    hcut= "";
    hregionName = "";
}

//Destructor
HistFile::~HistFile(){
    std::cout << "\n ### success ###" << std::endl;
    ofile->Close();
}

//void SaveHist(TString branchName, TString hname, TString htitle, TCut hcut, const Int_t nbins, Double_t xbins[])
void HistFile::SaveHist(TString varname)
{
    if (histcnt==0) {std::cout << "writing histograms ..." << std::endl; histcnt++;}
    else { histcnt++; cout<<std::flush<<"\r"<<histcnt+1;}
    hname = hname.Format("%s%s%s", varname.Data(), hweightName.Data(), hregionName.Data());
    htitle = htitle.Format("%s, %s, %s", varname.Data(), hweightName.Data(), hregionName.Data());

    TH1D* hist = new TH1D(hname, htitle, bins.size()-1, bins.data());
    hist->Reset();
    hist->Sumw2();
    nselected=0;
    TempString = branchName+">>+"+hname;
    nselected = chain->Draw(TempString.Data(), hcut*hweight, "egoff");
    //std::cout << " event survived the cut(s): " << nselected << std::endl;
    hist->Write();
}

void HistFile::SetBranch( TString bname)
{ branchName = bname; }

void HistFile::SetBins( ranges::span<Double_t> ibins)
{ bins = ibins; }

void HistFile::SetCutData(TCut regionCut, TString region="")
{
    hcut = regionCut;
    if(!region.EqualTo("")) hregionName = region;
}

void HistFile::SetWeightData(TString weight, TString weightName = "")
{
    hweight = weight.Data();
    if(!weightName.EqualTo("")) hweightName = weightName;
}

