//
// Aidan Style, based on a style file from BaBar and ATLAS, orig @author M.Sutton
//

#include <iostream>

#include "AidanStyle.h"

#include "TROOT.h"

void SetAidanStyle ()
{
  static TStyle* aidanStyle = 0;
  std::cout << "\nApplying AIDAN style settings...\n" << std::endl ;
  if ( aidanStyle==0 ) aidanStyle = AidanStyle();
  gROOT->SetStyle("AIDAN");
  gROOT->ForceStyle();
}

TStyle* AidanStyle() 
{
  TStyle *aidanStyle = new TStyle("AIDAN","Aidan style");

  // use plain black on white colors
  Int_t icol=0; // WHITE
  aidanStyle->SetFrameBorderMode(icol);
  aidanStyle->SetFrameFillColor(icol);
  aidanStyle->SetCanvasBorderMode(icol);
  aidanStyle->SetCanvasColor(icol);
  aidanStyle->SetPadBorderMode(icol);
  aidanStyle->SetPadColor(icol);
  aidanStyle->SetStatColor(icol);
  aidanStyle->SetTitleFillColor(icol);
  //aidanStyle->SetFillColor(icol); // don't use: white fill color for *all* objects

  // set the paper & margin sizes
  aidanStyle->SetPaperSize(20,26);

  // set margin sizes
  aidanStyle->SetPadTopMargin(0.05);
  aidanStyle->SetPadRightMargin(0.05);
  // aidanStyle->SetPadRightMargin(0.16);
  aidanStyle->SetPadBottomMargin(0.16);
  aidanStyle->SetPadLeftMargin(0.16);

  // set title offsets (for axis label)
  aidanStyle->SetTitleXOffset(1.4);
  aidanStyle->SetTitleYOffset(1.4);

  // use large fonts
  //Int_t font=72; // Helvetica italics
  Int_t font=42; // Helvetica
  Double_t tsize=0.04;
  //aidanStyle->SetTextFont(font);

  //aidanStyle->SetTextSize(tsize);
  aidanStyle->SetLabelFont(font,"x");
  aidanStyle->SetTitleFont(font,"x");
  aidanStyle->SetLabelFont(font,"y");
  aidanStyle->SetTitleFont(font,"y");
  aidanStyle->SetLabelFont(font,"z");
  aidanStyle->SetTitleFont(font,"z");
  
  aidanStyle->SetLabelSize(tsize,"x");
  aidanStyle->SetTitleSize(tsize,"x");
  aidanStyle->SetLabelSize(tsize,"y");
  aidanStyle->SetTitleSize(tsize,"y");
  aidanStyle->SetLabelSize(tsize,"z");
  aidanStyle->SetTitleSize(tsize,"z");

  // use bold lines and markers
  aidanStyle->SetMarkerStyle(20);
  aidanStyle->SetMarkerSize(0.7);
  aidanStyle->SetHistLineWidth(2.);
  aidanStyle->SetLineStyleString(2,"[12 12]"); // postscript dashes

  // get rid of X error bars
  aidanStyle->SetErrorX(0.0001);
  // get rid of error bar caps
  aidanStyle->SetEndErrorSize(0.);

  ////////////////////////////////////////////////// 
  // added by aidan
  aidanStyle->SetTextSize(16);
  aidanStyle->SetOptTitle(1);
  aidanStyle->SetTitleStyle(0);
  aidanStyle->SetTitleBorderSize(0);
  ////////////////////////////////////////////////// 
  //
  //aidanStyle->SetOptTitle(0);
  //aidanStyle->SetOptStat(1111);
  aidanStyle->SetOptStat(0);
  //aidanStyle->SetOptFit(1111);
  aidanStyle->SetOptFit(0);

  // put tick marks on top and RHS of plots
  aidanStyle->SetPadTickX(1);
  aidanStyle->SetPadTickY(1);
  //aidanStyle->SetOptLogy(1);

  return aidanStyle;

}

