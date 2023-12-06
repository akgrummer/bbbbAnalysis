from ROOT import TH2D, TCanvas, TFile, TGraphAsymmErrors, TGraph, TLegend
import ROOT
import subprocess
from array import array
import os
import argparse
import os.path
from array import array


ROOT.gROOT.SetBatch(True)

parser = argparse.ArgumentParser(description='Command line parser of skim options')
parser.add_argument('--input1'    , dest = 'input'    , help = 'input file' , required = True)
parser.add_argument('--input2'    , dest = 'input2'    , help = 'input file' , required = True)
parser.add_argument('--systematics'   , dest='systematics'   , help='systematics'   , action="store_true", default = False, required = False)
parser.add_argument('--year'   , dest='year'   , help='run year, 2016,2017,2018,RunII', default = "RunII", required = False)
parser.add_argument('--vsMY', dest='vsMY', default=False, action='store_true', required=False)


args = parser.parse_args()

append = "statOnly"
if args.systematics : append = "syst"
color     = ROOT.kBlue

#  xMassList = [300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1400, 1600, 1800, 2000]
xMassList = [400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1400, 1600]
yMassList = [60, 70, 80, 90, 100, 125, 150, 200, 250, 300, 400, 500,600, 700, 800, 900, 1000, 1200, 1400]
if args.vsMY:
    massList = yMassList
    massXY = "Y"
else:
    massList = xMassList
    massXY = "X"

inputFile1 = TFile(args.input, "READ")
inputFile2 = TFile(args.input2, "READ")

for theMass in massList:
    theCanvas = TCanvas("limitMapCentral", "limitMapCentral", 1200, 800)
    theLegend  = TLegend(0.17,0.65,0.5,0.88)
    theLegend.SetBorderSize(0) # remove the border
    theLegend.SetLineColor(0)
    theLegend.SetFillColor(0)
    theLegend.SetTextSize(0.035)
    theLegend.SetFillStyle(0) # make the legend background transparent
    theLegend.SetTextSize(0.04)
    # theLegend.SetNColumns(2);

    theCanvas.SetLogy()

    inputGraph1 = "Limits_{0}/Option_{1}/CentralLimit_{0}_{1}_mass{2}_{3}".format(args.year, append, massXY, theMass)
    theGraph1 = inputFile1.Get(inputGraph1)
    theGraph1.SetTitle("")
    theGraph1.GetXaxis().SetTitle("m_{Y} [GeV]")
    theGraph1.GetXaxis().SetLabelFont(62)
    theGraph1.GetXaxis().SetLabelSize(0.045)
    theGraph1.GetXaxis().SetTitleFont(62)
    theGraph1.GetXaxis().SetTitleSize(0.045)
    theGraph1.GetYaxis().SetLabelFont(62)
    theGraph1.GetYaxis().SetLabelSize(0.045)
    theGraph1.GetYaxis().SetTitleFont(62)
    theGraph1.GetYaxis().SetTitleSize(0.045)
    theGraph1.GetYaxis().SetTitle("#sigma(pp #rightarrow X) #times BR(Y(b#bar{b}) H(b#bar{b})) [fb]")
    # theGraph1.GetYaxis().SetRangeUser(1.,1.e5)
    if not args.vsMY:
        if (theMass<500):
            theGraph1.SetMinimum(90.)
            theGraph1.SetMaximum(500.)
        elif (theMass<600):
            theGraph1.SetMinimum(20.)
            theGraph1.SetMaximum(200.)
        elif (theMass<700):
            theGraph1.SetMinimum(10.)
            theGraph1.SetMaximum(100.)
        elif (theMass<800):
            theGraph1.SetMinimum(10.)
            theGraph1.SetMaximum(90.)
        elif (theMass<1000):
            theGraph1.SetMinimum(5.)
            theGraph1.SetMaximum(100)
        else:
            theGraph1.SetMinimum(1.)
            theGraph1.SetMaximum(40)
    theGraph1.GetXaxis().SetRangeUser(50.,1900.)
    theGraph1.SetTitle("m_{%s} = %i GeV"%(massXY,theMass))
    theGraph1.SetLineColor(color)
    theGraph1.SetLineWidth(1)

    inputGraph2 = "Limits_{0}/Option_{1}/CentralLimit_{0}_{1}_mass{2}_{3}".format(args.year, append, massXY, theMass)
    theGraph2 = inputFile2.Get(inputGraph2)
    theGraph2.SetLineColor(ROOT.kRed+2)
    theGraph2.SetLineWidth(1)


    theGraph1.Draw("apl")
    theGraph2.Draw("plsame")

    x, y = ROOT.Double(0), ROOT.Double(0)
    multiplier = ROOT.Double(1)


    # theLegend.AddEntry(theGraph1, "Median expected limit w/o extra unc.", "lp")
    # theLegend.AddEntry(theGraph1, "Median expected limit old non-closure", "lp")
    # theLegend.AddEntry(theGraph2, "Median expected limit new non-closure, new bins", "lp")
    theLegend.AddEntry(theGraph1, "before adding signal", "lp")
    theLegend.AddEntry(theGraph2, "after adding 2017 MC mX=1000,mY=150 GeV", "lp")

    theLegend.Draw("same")
    theCanvas.SaveAs("TwoLimits{0}_{1}_m{2}_{3}.pdf".format(args.year, append,massXY, theMass))
    del theCanvas

inputFile1.Close()
inputFile2.Close()

