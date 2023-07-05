#include "RooAbsArg.h"
#include "RooConstVar.h"
#include "RooDataHist.h"
#include "RooDataSet.h"
#include "RooFit.h"
#include "RooGaussian.h"
#include "RooHistPdf.h"
#include "RooIntegralMorph.h"
#include "RooMomentMorphND.h"
#include "RooMyPdf.cxx"
#include "RooNLLVar.h"
#include "RooPlot.h"
#include "RooPolynomial.h"
#include "RooRealVar.h"
#include "RooWorkspace.h"
#include "TAxis.h"
#include "TCanvas.h"
#include "TH1.h"
#include "TRandom3.h"
#include <RooRealVar.h>

using namespace RooFit;



void morphing() {

  TString file_input[] = {"./FitParameterM4l_2e2m.txt",
                          "./FitParameterAvgMll_2e2m.txt"};
  TString tmps;
  ifstream fin_mS(file_input[0]);
  ifstream fin_mZd(file_input[1]);
  int Npoints = 33;
  double Param_mS[7][Npoints];
  double Param_mZd[7][Npoints];
  double PmS[33];
  double PmZd[33];
  fin_mS >> tmps;
  fin_mS >> tmps;
  fin_mS >> tmps;
  fin_mS >> tmps;
  fin_mS >> tmps;
  fin_mS >> tmps;
  fin_mS >> tmps;
  fin_mS >> tmps;
  fin_mS >> tmps; // read first line.

  for (Int_t i = 0; i < Npoints; i++) {

    fin_mS >> tmps;
    PmS[i] = tmps.IsFloat() ? tmps.Atof() : 0;
    fin_mS >> tmps;
    PmZd[i] = tmps.IsFloat() ? tmps.Atof() : 0;
    fin_mS >> tmps;
    Param_mS[0][i] = tmps.IsFloat() ? tmps.Atof() : 0;
    fin_mS >> tmps;
    Param_mS[1][i] = tmps.IsFloat() ? tmps.Atof() : 0;
    fin_mS >> tmps;
    Param_mS[2][i] = tmps.IsFloat() ? tmps.Atof() : 0;
    fin_mS >> tmps;
    Param_mS[3][i] = tmps.IsFloat() ? tmps.Atof() : 0;
    fin_mS >> tmps;
    Param_mS[4][i] = tmps.IsFloat() ? tmps.Atof() : 0;
    fin_mS >> tmps;
    Param_mS[5][i] = tmps.IsFloat() ? tmps.Atof() : 0;
    fin_mS >> tmps;
    Param_mS[6][i] = tmps.IsFloat() ? tmps.Atof() : 0;
  }

  fin_mZd >> tmps;
  fin_mZd >> tmps;
  fin_mZd >> tmps;
  fin_mZd >> tmps;
  fin_mZd >> tmps;
  fin_mZd >> tmps;
  fin_mZd >> tmps;
  fin_mZd >> tmps;
  fin_mZd >> tmps; // read first line.
  for (Int_t i = 0; i < Npoints; i++) {

    fin_mZd >> tmps;
    PmS[i] = tmps.IsFloat() ? tmps.Atof() : 0;
    fin_mZd >> tmps;
    PmZd[i] = tmps.IsFloat() ? tmps.Atof() : 0;
    fin_mZd >> tmps;
    Param_mZd[0][i] = tmps.IsFloat() ? tmps.Atof() : 0;
    fin_mZd >> tmps;
    Param_mZd[1][i] = tmps.IsFloat() ? tmps.Atof() : 0;
    fin_mZd >> tmps;
    Param_mZd[2][i] = tmps.IsFloat() ? tmps.Atof() : 0;
    fin_mZd >> tmps;
    Param_mZd[3][i] = tmps.IsFloat() ? tmps.Atof() : 0;
    fin_mZd >> tmps;
    Param_mZd[4][i] = tmps.IsFloat() ? tmps.Atof() : 0;
    fin_mZd >> tmps;
    Param_mZd[5][i] = tmps.IsFloat() ? tmps.Atof() : 0;
    fin_mZd >> tmps;
    Param_mZd[6][i] = tmps.IsFloat() ? tmps.Atof() : 0;
  }

  RooRealVar mll("mll", "mll", 0, 300);
  RooRealVar mS("mS", "mS", 120, 900);


  RooArgList pdfs;

  TVectorD paramVec = TVectorD(33);

  RooWorkspace w("w", 2);
  RooAbsPdf *pdf;

  TH1 *hmZdmS[33];
  TH1 *hmZdmS_morph[10];

  RooBinning dim1(1, 0.0, 1.0);
  RooBinning dim2(1, 0.0, 1.0);
  RooMomentMorphND::Grid referenceGrid(dim1, dim2);

  for (int i = 0; i < 33; ++i) {
    w.factory(TString::Format(
        "RooMyPdf::myPdf_mZd_%d(mll[0,300], %f, %f,%f, %f,%f,%f, %f)", i,
        Param_mZd[0][i], Param_mZd[1][i], Param_mZd[2][i], Param_mZd[3][i],
        Param_mZd[4][i], Param_mZd[5][i], Param_mZd[6][i]));
    w.factory(TString::Format(
        "RooMyPdf::myPdf_mS_%d(mS[120,900], %f, %f,%f, %f,%f,%f, %f)", i,
        Param_mS[0][i], Param_mS[1][i], Param_mS[2][i], Param_mS[3][i],
        Param_mS[4][i], Param_mS[5][i], Param_mS[6][i]));
    w.factory(TString::Format("PROD::myPdf_mZdmS_%d(myPdf_mZd_%d,myPdf_mS_%d)",
                              i, i, i));

    pdf = w.pdf(TString::Format("myPdf_mZdmS_%d", i));

    pdfs.add(*pdf);
    paramVec[i] = i;
    w.Print();

    hmZdmS[i] =
        pdf->createHistogram(TString::Format("hmZdmS_%d", i), mS,
                             Binning(460, 120, 1500), YVar(mll, Binning(100)));
  }

  pdfs.Print();

  RooPlot *mZdFrame = w.var("mll")->frame();
  RooPlot *mSFrame = w.var("mS")->frame();

  RooRealVar alpha1("alpha1", "alpha1", 0.5, 0, 1);
  RooRealVar alpha2("alpha2", "alpha2", 0.5, 0, 1);

  RooArgList varlist;
  varlist.add(mS);
  varlist.add(mll);
  referenceGrid.addPdf(*w.pdf("myPdf_mZdmS_0"), 0, 0);
  referenceGrid.addPdf(*w.pdf("myPdf_mZdmS_1"), 1, 0);
  referenceGrid.addPdf(*w.pdf("myPdf_mZdmS_2"), 0, 1);
  referenceGrid.addPdf(*w.pdf("myPdf_mZdmS_3"), 1, 1);
  TFile f("outputHist.root", "recreate");

  RooMomentMorphND morphpdfND("morphpdfND", "2D morph",
                              RooArgList(alpha1, alpha2), RooArgList(mS, mll),
                              referenceGrid, RooMomentMorphND::Linear);

  alpha1.setVal(0.0);
  alpha2.setVal(0.0);
  hmZdmS_morph[0] = morphpdfND.createHistogram(
      TString::Format("hmZdmS_morph_alpha%d", 0), mS, Binning(460, 120, 1500),
      YVar(mll, Binning(100)));
  hmZdmS_morph[0]->Write();

  alpha1.setVal(1.0);
  alpha2.setVal(1.0);
  hmZdmS_morph[1] = morphpdfND.createHistogram(
      TString::Format("hmZdmS_morph_alpha%d", 0), mS, Binning(460, 120, 1500),
      YVar(mll, Binning(100)));
  hmZdmS_morph[1]->Write();

  hmZdmS[0]->Draw("cont");
  for (int i = 1; i < 33; i++) {
    hmZdmS[i]->Draw("cont same");
    hmZdmS[i]->Write();
  }
  for (int i = 0; i < 2; i++) {
    hmZdmS_morph[i]->Draw("cont1 same");
  }
  f.Close();
}
