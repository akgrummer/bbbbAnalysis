import ROOT
from ROOT import TFile, TH1F, TH2F, TCanvas, gStyle, gPad, gDirectory, TLatex, gROOT, PyConfig, TMath, kBlue, TLine, TPad, TLegend, TGraph, TBox, kThermometer, THStack, TGraphAsymmErrors
from ROOT import kRed, kGreen
# PyConfig.IgnoreCommandLineOptions = False
import numpy as np
import re
import os
from VariableDicts import varInfo
import sys
import math
import argparse
import csv

def rootplot_1Dhist(h1, h2, h3, year, idir, tag1, tag2, tag3):
    c1 = TCanvas('c1', 'c1',800,600)
    gStyle.SetOptStat(0) # remove the stats box
    gStyle.SetOptTitle(0) # remove the title
    c1.SetTicks(1,1)


    if(args.monitor != "mean"):
        h1.GetYaxis().SetRangeUser(-0.2, 1.4)
        h1.GetYaxis().SetTitle("Fraction of bins")
        h2.GetYaxis().SetRangeUser(-0.2, 1.4)
        h2.GetYaxis().SetTitle("Fraction of bins")
        h3.GetYaxis().SetRangeUser(-0.2, 1.4)
        h3.GetYaxis().SetTitle("Fraction of bins")
    else:
        h1.GetYaxis().SetRangeUser(0, h3.GetBinContent(h3.GetMaximumBin())*1.2 )
        h1.GetYaxis().SetTitle("Events per bin")
        h2.GetYaxis().SetRangeUser(0, h3.GetBinContent(h3.GetMaximumBin())*1.2 )
        h2.GetYaxis().SetTitle("Events per bin")
        h3.GetYaxis().SetRangeUser(0, h3.GetBinContent(h3.GetMaximumBin())*1.2 )
        h3.GetYaxis().SetTitle("Events per bin")
    h1.GetXaxis().SetTitle("Mass Group")
    h1.GetXaxis().SetNdivisions(-505);
    # h1.GetXaxis().ChangeLabel(1,-1,-1,-1,-1,-1,"-#pi");
    h1.SetLineColor(kRed+2)
    h1.SetLineWidth(2)
    h2.GetXaxis().SetTitle("Mass Group")
    h2.GetXaxis().SetNdivisions(-505);
    # h2.GetXaxis().ChangeLabel(1,-1,-1,-1,-1,-1,"-#pi");
    h2.SetLineColor(kBlue+2)
    h2.SetLineWidth(2)
    h3.GetXaxis().SetTitle("Mass Group")
    h3.GetXaxis().SetNdivisions(-505);
    # h2.GetXaxis().ChangeLabel(1,-1,-1,-1,-1,-1,"-#pi");
    h3.SetLineColor(ROOT.kGreen+2)
    h3.SetLineWidth(2)
    h3.Draw("hist")
    h2.Draw("hist same")
    h1.Draw("hist same")

    # LineAtOne = TLine(-0.5,.05,4.5,0.05) #x1,y1,x2,y2
    # LineAtOne.SetLineWidth(2)
    # LineAtOne.SetLineColor(1)
    # LineAtOne.SetLineStyle(9)
    # LineAtOne.Draw()

    # Decorations
    CMSlabel = TLatex()
    #  CMSlabel.SetTextSize( 0.08 )
    #  CMSlabel.DrawTextNDC(0.7, 0.85, "CMS Internal")
    CMSlabel.SetTextFont(63)
    CMSlabel.SetTextSize( 30 )
    CMSlabel.DrawLatexNDC(0.12, 0.93, "CMS #scale[0.8]{#it{#bf{Work In Progress}}}")

    plotlabels = TLatex()

    plotlabels.SetTextFont(53)
    plotlabels.SetTextSize(20)
    plotlabels.DrawLatexNDC(0.55, 0.93, args.year)

    plotlabels.SetTextFont(63)
    plotlabels.SetTextSize(20)
    #  labelText = "mX = %.0f GeV, mY = %.0f GeV"%(mXval,mYval)
    labelText = ""
    if "VR" in tag1:    labelText = labelText + "Validation Region"
    if "CR" in tag1:    labelText = labelText + "Control Region"
    if "SR" in tag1:    labelText = labelText + "Signal Region"
    plotlabels.DrawLatexNDC(0.65, 0.93, labelText)
    plotlabels.SetTextFont(63)
    plotlabels.SetTextSize(16)
    if (args.monitor == "lt1"): labelText = "Bins with less than 1 event"
    if (args.monitor == "lt5"): labelText = "Bins with less than 5 events"
    if (args.monitor == "lt10"): labelText = "Bins with less than 10 events"
    if (args.monitor == "mean"): labelText = "Average number of events per bin"
    plotlabels.DrawLatexNDC(0.2, 0.85,labelText)
    plotlabels.DrawLatexNDC(0.2, 0.81, "Background Model, before fit")
    #### define legend
    leg = TLegend(0.55,0.75,0.70,0.86)
    h1Label="nominal binning"
    h2Label="mY bins x2"
    h3Label="mY bins x2, mX bins x2"
    leg.AddEntry(h1, h1Label, "l")
    leg.AddEntry(h2, h2Label, "l")
    leg.AddEntry(h3, h3Label, "l")
    leg.SetBorderSize(0) # remove the border
    leg.SetLineColor(0)
    leg.SetFillColor(0)
    leg.SetTextSize(0.03)
    leg.SetFillStyle(0) # make the legend background transparent
    leg.Draw()

    c1.SaveAs("{0}/{1}vs{2}vs{3}_{4}_{5}.pdf".format( odir, tag1, tag2, tag3, year, args.monitor))

def makePlotsPerYear(year, eventDistFile1, eventDistFile2, eventDistFile3):
  # odir = "VarPlots/2023Jun26_GOF_2D/"
  h1 = ROOT.TH1D( "h1", "h1 hist", 5, -0.5, 4.5);
  h2 = ROOT.TH1D( "h2", "h2 hist", 5, -0.5, 4.5);
  h3 = ROOT.TH1D( "h3", "h3 hist", 5, -0.5, 4.5);
  # varname = "HH_kinFit_m"
  with open(eventDistFile1) as csvfile:
      eventPer = csv.reader(csvfile, delimiter=',')
      cnt=1
      for x,y,p in eventPer:
          h1.SetBinContent(cnt ,float(p))
          cnt+=1

  with open(eventDistFile2) as csvfile:
      eventPer = csv.reader(csvfile, delimiter=',')
      cnt=1
      for x,y,p in eventPer:
          h2.SetBinContent(cnt ,float(p))
          cnt+=1

  with open(eventDistFile3) as csvfile:
      eventPer = csv.reader(csvfile, delimiter=',')
      cnt=1
      for x,y,p in eventPer:
          h3.SetBinContent(cnt ,float(p))
          cnt+=1


  # rootplot_2Dhist(h2dCR,year, "CR", odir, tag)
  rootplot_1Dhist(h1, h2, h3, year, idir, tag1, tag2, tag3)
  # rootplot_2Dhist(h2dSR,year, "SR", odir, tag)
  # del h2dCR, h2dVR, h2dSR
  del h1
  del h2
  del h3

##################################################
gROOT.SetBatch(True)
parser = argparse.ArgumentParser(description='Command line parser of skim options')
parser.add_argument('--year'       ,  dest = 'year'       ,  help = 'production tag'           ,  required = True        )
parser.add_argument('--monitor'       ,  dest = 'monitor'       ,  help = 'production tag', default="lt1"           ,  required = False        ) # "lt1", "lt5", "lt10"

args = parser.parse_args()
tag1 = "2023Jul5_nonClosureMCStats2_SR"
tag2 = "2023Jul5_binMYx2_ncMCStats_SR"
tag3 = "2023Jul5_binMYx2_MXx2_SR"
limitDir="/uscms/homes/a/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/limits"
idir = limitDir + "/FitDiagnostics/EventDist_2023Sep/"
odir = idir+"compare/"
ifile = idir + "{0}_{1}_{2}.txt".format(args.monitor, tag1, args.year)
ifile2 = idir + "{0}_{1}_{2}.txt".format(args.monitor, tag2, args.year)
ifile3 = idir + "{0}_{1}_{2}.txt".format(args.monitor, tag3, args.year)
makePlotsPerYear("{}".format(args.year), ifile, ifile2, ifile3)

