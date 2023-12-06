import ROOT
from ROOT import TFile, TH1F, TH2F, TCanvas, gStyle, gPad, gDirectory, TLatex, gROOT, PyConfig, TMath, kBlue, TLine, TPad, TLegend, TGraph, TBox, kThermometer, THStack, TGraphAsymmErrors
from ROOT import kRed
# PyConfig.IgnoreCommandLineOptions = False
import numpy as np
import re
import os
from VariableDicts import varInfo
import sys
import math
import argparse
import csv

def rootplot_1Dhist(h1, year, iodir, tag):
    c1 = TCanvas('c1', 'c1',800,600)
    gStyle.SetOptStat(0) # remove the stats box
    gStyle.SetOptTitle(0) # remove the title
    c1.SetTicks(1,1)


    h1.GetYaxis().SetRangeUser(-0.2, 1.2)
    h1.GetXaxis().SetTitle("Mass Group")
    h1.GetYaxis().SetTitle("P-Value")
    h1.GetXaxis().SetNdivisions(-505);
    # h1.GetXaxis().ChangeLabel(1,-1,-1,-1,-1,-1,"-#pi");
    h1.SetLineColor(kRed+2)
    h1.SetLineWidth(2)
    # h2.SetLineColor(kBlue+2)
    # h2.SetLineWidth(2)
    h1.Draw("hist")

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
    if "VR" in tag:    labelText = labelText + "Validation Region"
    if "CR" in tag:    labelText = labelText + "Control Region"
    if "SR" in tag:    labelText = labelText + "Signal Region"
    plotlabels.DrawLatexNDC(0.65, 0.93, labelText)
    plotlabels.SetTextFont(63)
    plotlabels.SetTextSize(16)
    plotlabels.DrawLatexNDC(0.2, 0.8, "1000 Toys")
    plotlabels.DrawLatexNDC(0.2, 0.76, "Background Only Fits")
    #### define legend
    leg = TLegend(0.6,0.75,0.75,0.89)
    leg.AddEntry(h1, "GoF", "l")
    #  leg.AddEntry(h1, "3b ttbar", "l")
    #  leg.AddEntry(h2, "4b ttbar", "l")
    # leg.AddEntry(h1, "3b Signal MC", "l")
    # leg.AddEntry(h2, "4b Signal MC", "l")
    leg.SetBorderSize(0) # remove the border
    leg.SetLineColor(0)
    leg.SetFillColor(0)
    leg.SetTextSize(0.035)
    leg.SetFillStyle(0) # make the legend background transparent
    leg.Draw()

    c1.SaveAs("{}/sig0{}_{}.pdf".format( iodir, tag, year))

def makePlotsPerYear(year, pvalFile):
  # odir = "VarPlots/2023Jun26_GOF_2D/"
  hGOF = ROOT.TH1D( "GOF", "GoF hist", 5, -0.5, 4.5);
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

  # rootplot_2Dhist(h2dCR,year, "CR", odir, tag)
  rootplot_1Dhist(hGOF, year, iodir, args.tag + "_"+args.algo + args.zoom)
  # rootplot_2Dhist(h2dSR,year, "SR", odir, tag)
  # del h2dCR, h2dVR, h2dSR
  del hGOF

##################################################
gROOT.SetBatch(True)
parser = argparse.ArgumentParser(description='Command line parser of skim options')
parser.add_argument('--tag'       ,  dest = 'tag'       ,  help = 'production tag'           ,  required = True        )
parser.add_argument('--algo'       ,  dest = 'algo'       ,  help = 'production tag'           ,  required = True        )
parser.add_argument('--year'       ,  dest = 'year'       ,  help = 'production tag'           ,  required = True        )
parser.add_argument('--zoom'       ,  dest = 'zoom'       ,  help = 'production tag', default=""           ,  required = False        )

args = parser.parse_args()

iodir = "GOFfiles/GOFfiles_sig0/GOFPlots_" + args.tag
ifile = iodir + "/PVALS_{0}_{1}_sig0.csv".format(args.year,args.algo)
makePlotsPerYear("{}".format(args.year), ifile)

