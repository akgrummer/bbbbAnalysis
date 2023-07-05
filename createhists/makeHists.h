#ifndef MAKEHIST_H
#define MAKEHIST_H
#include <iostream>
#include <range/v3/all.hpp>
#include <yaml-cpp/yaml.h>

#include <TStyle.h>
#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>
#include <TChain.h>
#include <TCut.h>
#include <TString.h>
#include <TH1F.h>
#include <TH2F.h>
#include <TF1.h>
#include <TLatex.h>
#include <TCanvas.h>
#include <TPad.h>
#include <Rtypes.h>
#include <RtypesCore.h>
#include <TLegend.h>
#include <TH1.h>

using namespace std;
using namespace ranges;

Double_t binEdges_H2_m[] = { 36., 45., 51., 57., 62., 66., 70., 74., 78., 82., 86., 90., 94., 98., 102., 106., 110., 114., 122., 132., 140., 148., 156., 164., 172., 180., 188., 196., 204., 212., 228., 244., 260., 276., 292., 308., 324., 340., 356., 372., 388., 412., 444., 476., 508., 540., 572., 604., 636., 668., 700., 732., 764., 828., 892., 956., 1020., 1084., 1148., 1212., 1276., 1340., 1404., 1468., 1564., 1692., 1820., 1948., 2076., 2204. };

Double_t binEdges_HH_kinFit_m[] = { 212., 228., 244., 260., 276., 292., 308., 324., 340., 360., 392., 424., 456., 488., 520., 552., 584., 616., 648., 704., 768., 832., 896., 960., 1024., 1088., 1152., 1216., 1296., 1424., 1552., 1680., 1808., 1936., 2064., 2192., 2320. };

TCut Blinded      = "H2_m > 125+20 || H2_m < 125-20";
TCut SR           = "H1_m > 125-20 && H1_m < 125+20";
TCut VR           = "(H1_m > 125-30 && H1_m < 125-20) || (H1_m > 125+20 && H1_m < 125+30)";
TCut CR           = "(H1_m > 125-60 && H1_m < 125-30) || (H1_m > 125+30 && H1_m < 125+60)";
TCut VRB          = (VR) && (Blinded);
TCut CRB          = (CR) && (Blinded);

TString weight = "Weight_forBackground_BDTweights_2023Apr10_10folds_";
TString training_elems[] = {"mean", "max", "min"};
ranges::span trainings{ training_elems, std::size(training_elems) };

TString itreename = "bbbbTree";
//TString ifiles[] = { "bbbbNtuple_94.root", "bbbbNtuple_95.root" };
vector<string> ifiles;
vector<string> ifiles2;
string idir;
TString odir = "./hists/";
TString ofilename;
// TString ofilename = "hists_94.root";

#endif
