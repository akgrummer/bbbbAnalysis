from ROOT import TH2D, TCanvas, TH1D, TFile, TGraphAsymmErrors, TGraph, TLegend, TPad, gPad, TLatex, gStyle
import ROOT
import subprocess
from array import array
import os
import argparse
import os.path
from array import array


ROOT.gROOT.SetBatch(True)

parser = argparse.ArgumentParser(description='Command line parser of skim options')
parser.add_argument('--tag'    , dest = 'tag'    , help = 'tag file' , required = True)
parser.add_argument('--year'    , dest = 'year'    , help = 'year to run over: 201{6-8},RunII' , required = True)

args = parser.parse_args()

# append = "statOnly"
append = "syst"
color     = ROOT.kBlue
#  year = "RunII"
#  year = "2016"
year = ""
year = args.year

# massList = xMassList
# massXY="X"
# othermassXY="Y"

ifile="Significance/{0}/sig_{1}.root".format(args.tag, args.year)
inputFile = TFile(ifile)
myTree = inputFile.Get("limit")
h1 = ROOT.TH1D('h1','h1' ,10 ,0.,5.)
myTree.Draw("limit>>h1", "limit>0", "goff")


theCanvas = TCanvas("limitsMean", "limitsMean", 800, 600)
# theCanvas.SetLogy()
gStyle.SetOptStat(0) # remove the stats box
gStyle.SetOptTitle(0) # remove the title
gPad.SetTicks(1,1)
gPad.SetMargin(0.12,0.05,0.12,0.09) #left,right,bottom,top
h1.SetMarkerStyle(8)
h1.SetMarkerSize(0.8)
h1.SetLineWidth(2)
h1.GetXaxis().SetTitle("#sigma")
h1.GetYaxis().SetTitle("Entries/bin")
h1.Draw("hist")
h1.GetYaxis().SetRangeUser(0,h1.GetMaximum()*1.3)

CMSlabel = TLatex()
CMSlabel.SetTextFont(63)
CMSlabel.SetTextSize( 30 )
CMSlabel.DrawLatexNDC(0.12, 0.93, "CMS #scale[0.8]{#it{#bf{Work In Progress}}}")

plotlabels = TLatex()
plotlabels.SetTextFont(53)
plotlabels.SetTextSize(20)
if("RunII" in args.year): yearLabel="Full Run II Data"
else: yearLabel = args.year
plotlabels.DrawTextNDC(0.72, 0.93, yearLabel)

# plotlabels.DrawTextNDC(0.2, 0.76, "Mean: {:0.4f}".format(h1.GetMean()))
# plotlabels.DrawTextNDC(0.2, 0.72, "Std. Dev.: {:.4f}".format(h1.GetStdDev()))


labelText = ""
if "VR" in args.tag:      labelText = labelText + "Validation Region"
if "CR" in args.tag:      labelText = labelText + "Control Region"
if "SR" in args.tag:      labelText = labelText + "Signal Region"
plotlabels.SetTextFont(63)
plotlabels.SetTextSize(20)
plotlabels.DrawTextNDC(0.6, 0.82, labelText)
plotlabels.SetTextFont(43)
plotlabels.DrawTextNDC(0.6, 0.77, "Significance")
plotlabels.DrawLatexNDC(0.6, 0.73, "Cut: #sigma>0")

odir = "results/{}/".format("Significance")
if not os.path.isdir(odir):
    os.mkdir(odir)
odir = "{0}Limits_{1}/".format(odir,args.tag)
if not os.path.isdir(odir):
    os.mkdir(odir)

ofile = "Signif_{0}_{1}_{2}".format(args.year, append, args.tag)
ofile = "{0}{1}".format(ofile,".pdf")
theCanvas.SaveAs(odir+ofile)

inputFile.Close()

