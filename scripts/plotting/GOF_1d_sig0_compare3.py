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

def rootplot_1Dhist(h1, h2, h3, year, idir, tag):
    c1 = TCanvas('c1', 'c1',800,600)
    gStyle.SetOptStat(0) # remove the stats box
    gStyle.SetOptTitle(0) # remove the title
    c1.SetTicks(1,1)


    h1.GetYaxis().SetRangeUser(-0.2, 1.4)
    h1.GetXaxis().SetTitle("Mass Group")
    h1.GetYaxis().SetTitle("P-Value")
    h1.GetXaxis().SetNdivisions(-505);
    # h1.GetXaxis().ChangeLabel(1,-1,-1,-1,-1,-1,"-#pi");
    h1.SetLineColor(kRed+2)
    h1.SetLineWidth(2)
    h2.GetYaxis().SetRangeUser(-0.2, 1.2)
    h2.GetXaxis().SetTitle("Mass Group")
    h2.GetYaxis().SetTitle("P-Value")
    h2.GetXaxis().SetNdivisions(-505);
    # h2.GetXaxis().ChangeLabel(1,-1,-1,-1,-1,-1,"-#pi");
    h2.SetLineColor(kBlue+2)
    h2.SetLineWidth(2)
    # h2.SetLineColor(kBlue+2)
    # h2.SetLineWidth(2)
    h3.GetYaxis().SetRangeUser(-0.2, 1.2)
    h3.GetXaxis().SetTitle("Mass Group")
    h3.GetYaxis().SetTitle("P-Value")
    h3.GetXaxis().SetNdivisions(-505);
    # h3.GetXaxis().ChangeLabel(1,-1,-1,-1,-1,-1,"-#pi");
    h3.SetLineColor(kGreen+2)
    h3.SetLineWidth(2)
    # h3.SetLineColor(kBlue+2)
    # h3.SetLineWidth(2)
    h1.Draw("hist")
    h2.Draw("hist same")
    h3.Draw("hist same")

    LineAtOne = TLine(-0.5,.05,4.5,0.05) #x1,y1,x2,y2
    LineAtOne.SetLineWidth(2)
    LineAtOne.SetLineColor(1)
    LineAtOne.SetLineStyle(9)
    LineAtOne.Draw()

    # Decorations
    CMSlabel = TLatex()
    #  CMSlabel.SetTextSize( 0.08 )
    #  CMSlabel.DrawTextNDC(0.7, 0.85, "CMS Internal")
    CMSlabel.SetTextFont(63)
    CMSlabel.SetTextSize( 30 )
    CMSlabel.DrawLatexNDC(0.12, 0.93, "CMS #scale[0.8]{#it{#bf{Work In Progress}}}")

    plotlabels = TLatex()
    plotlabels.SetTextFont(63)
    plotlabels.SetTextSize(20)
    #  labelText = "mX = %.0f GeV, mY = %.0f GeV"%(mXval,mYval)
    labelText = ""
    if "VR" in tag and "VR" in args.tag2:    labelText = labelText + "Validation Region"
    if "CR" in tag and "CR" in args.tag2:    labelText = labelText + "Control Region"
    if "SR" in tag and "SR" in args.tag2:    labelText = labelText + "Signal Region"
    plotlabels.DrawLatexNDC(0.65, 0.93, labelText)
    plotlabels.SetTextFont(63)
    plotlabels.SetTextSize(16)
    plotlabels.DrawLatexNDC(0.2, 0.85, "1000 Toys")
    plotlabels.DrawLatexNDC(0.2, 0.81, "Background Only Fits")
    #### define legend
    leg = TLegend(0.55,0.75,0.70,0.86)
    h1Label=""
    h2Label=""
    h3Label=""
    # h1Label = "bad Hourglass Unc."
    h1Label = "new non-closure Unc."
    # if "binX4" in args.tag2:
    #     h2Label = "Merged Bins (x4)"
    # elif "doubleMCStats" in args.tag2:
    #     h2Label = "Doubled MC Stats."
    # elif "1p5MCStats" in args.tag2:
    #     h2Label = "x 1.5 MC Stats."
    # elif "newMinimizer" in args.tag2:
    #     h2Label = "analytic Minimizer"
    # elif "nonClosureMCStats" in args.tag2:
    #     h2Label = "new Hourglass Unc."
    # if "binMYx2" in args.tag2 and "ncMCStats" in args.tag2:
    h2Label = "new non-closure and mY bins x2"
    # if "binMYx2" in args.tag3 and "ncMCStats" in args.tag3:
    h3Label = "AND cut HARD low stats bins"
    leg.AddEntry(h1, h1Label, "l")
    leg.AddEntry(h2, h2Label, "l")
    leg.AddEntry(h3, h3Label, "l")
    #  leg.AddEntry(h1, "3b ttbar", "l")
    #  leg.AddEntry(h2, "4b ttbar", "l")
    # leg.AddEntry(h1, "3b Signal MC", "l")
    # leg.AddEntry(h2, "4b Signal MC", "l")
    leg.SetBorderSize(0) # remove the border
    leg.SetLineColor(0)
    leg.SetFillColor(0)
    leg.SetTextSize(0.03)
    leg.SetFillStyle(0) # make the legend background transparent
    leg.Draw()

    c1.SaveAs("{}/sig0{}_{}.pdf".format( odir, tag, year))

def makePlotsPerYear(year, pvalFile, pvalFile2, pvalFile3):
  # odir = "VarPlots/2023Jun26_GOF_2D/"
  hGOF = ROOT.TH1D( "GOF", "GoF hist", 5, -0.5, 4.5);
  hGOF2 = ROOT.TH1D( "GOF2", "GoF2 hist", 5, -0.5, 4.5);
  hGOF3 = ROOT.TH1D( "GOF3", "GoF3 hist", 5, -0.5, 4.5);
  # varname = "HH_kinFit_m"
  with open(pvalFile) as csvfile:
      pvals = csv.reader(csvfile, delimiter=',')
      next(pvals)
      cnt=1
      for x,y,p in pvals:
          hGOF.SetBinContent(cnt ,float(p))
          cnt+=1
      # h2dVR.Fill(ro, yval, val)
      # h2dSR.Fill(xval, yval, val)
  with open(pvalFile2) as csvfile:
      pvals = csv.reader(csvfile, delimiter=',')
      next(pvals)
      cnt=1
      for x,y,p in pvals:
          hGOF2.SetBinContent(cnt ,float(p))
          cnt+=1

  with open(pvalFile3) as csvfile:
      pvals = csv.reader(csvfile, delimiter=',')
      next(pvals)
      cnt=1
      for x,y,p in pvals:
          hGOF3.SetBinContent(cnt ,float(p))
          cnt+=1

  # rootplot_2Dhist(h2dCR,year, "CR", odir, tag)
  rootplot_1Dhist(hGOF, hGOF2, hGOF3, year, idir, args.tag  + "_"+args.tag2 + "_" +args.tag3 + "_"+args.algo + args.zoom)
  # rootplot_2Dhist(h2dSR,year, "SR", odir, tag)
  # del h2dCR, h2dVR, h2dSR
  del hGOF
  del hGOF2
  del hGOF3

##################################################
gROOT.SetBatch(True)
parser = argparse.ArgumentParser(description='Command line parser of skim options')
parser.add_argument('--tag'       ,  dest = 'tag'       ,  help = 'production tag'           ,  required = True        )
parser.add_argument('--tag2'       ,  dest = 'tag2'       ,  help = 'production tag'           ,  required = True        )
parser.add_argument('--tag3'       ,  dest = 'tag3'       ,  help = 'production tag'           ,  required = True        )
parser.add_argument('--algo'       ,  dest = 'algo'       ,  help = 'production tag'           ,  required = True        )
parser.add_argument('--year'       ,  dest = 'year'       ,  help = 'production tag'           ,  required = True        )
parser.add_argument('--zoom'       ,  dest = 'zoom'       ,  help = 'production tag', default=""           ,  required = False        )

args = parser.parse_args()

idir = "GOFfiles/GOFfiles_sig0/GOFPlots_" + args.tag
idir2 = "GOFfiles/GOFfiles_sig0/GOFPlots_" + args.tag2
idir3 = "GOFfiles/GOFfiles_sig0/GOFPlots_" + args.tag3
odir = "GOFfiles/GOFfiles_sig0/compare"
ifile = idir + "/PVALS_{0}_{1}_sig0.csv".format(args.year,args.algo)
ifile2 = idir2 + "/PVALS_{0}_{1}_sig0.csv".format(args.year,args.algo)
ifile3 = idir3 + "/PVALS_{0}_{1}_sig0.csv".format(args.year,args.algo)
makePlotsPerYear("{}".format(args.year), ifile, ifile2, ifile3)

