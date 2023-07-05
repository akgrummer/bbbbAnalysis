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
parser.add_argument('--input'    , dest = 'input'    , help = 'input file' , required = True)
parser.add_argument('--systematics'   , dest='systematics'   , help='systematics'   , action="store_true", default = False, required = False)
parser.add_argument('--year'   , dest='year'   , help='run year, 2016,2017,2018,RunII', default = "RunII", required = False)

args = parser.parse_args()

append = "statOnly"
if args.systematics : append = "syst"
color     = ROOT.kBlue

#  xMassList = [300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1400, 1600, 1800, 2000]
xMassList = [400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1400, 1600]

inputFile = TFile(args.input)

for xMass in xMassList:
    theCanvas = TCanvas("limitMapCentral", "limitMapCentral", 1200, 800)
    theLegend  = TLegend(0.17,0.65,0.5,0.88)
    theLegend.SetTextSize(0.04)
    # theLegend.SetNColumns(2);

    theCanvas.SetLogy()

    inputGraph2sigmaName = "Limits_{0}/Option_{1}/2SigmaLimit_{0}_{1}_massX_{2}".format(args.year, append, xMass)
    print("here", inputGraph2sigmaName)
    theGraph2sigma = inputFile.Get(inputGraph2sigmaName)
    theGraph2sigma.SetTitle("")
    theGraph2sigma.GetXaxis().SetTitle("m_{Y} [GeV]")
    theGraph2sigma.GetXaxis().SetLabelFont(62)
    theGraph2sigma.GetXaxis().SetLabelSize(0.045)
    theGraph2sigma.GetXaxis().SetTitleFont(62)
    theGraph2sigma.GetXaxis().SetTitleSize(0.045)
    theGraph2sigma.GetYaxis().SetLabelFont(62)
    theGraph2sigma.GetYaxis().SetLabelSize(0.045)
    theGraph2sigma.GetYaxis().SetTitleFont(62)
    theGraph2sigma.GetYaxis().SetTitleSize(0.045)
    theGraph2sigma.GetYaxis().SetTitle("#sigma(pp #rightarrow X) #times BR(Y(b#bar{b}) H(b#bar{b})) [fb]")
    theGraph2sigma.GetYaxis().SetRangeUser(1.,1.e5)
    theGraph2sigma.GetXaxis().SetRangeUser(50.,1900.)
    theGraph2sigma.SetTitle("m_{X} = %i GeV"%(xMass))
    theGraph2sigma.Draw("a3")

    inputGraph1sigmaName = "Limits_{0}/Option_{1}/1SigmaLimit_{0}_{1}_massX_{2}".format(args.year, append, xMass)
    theGraph1sigma = inputFile.Get(inputGraph1sigmaName)
    theGraph1sigma.Draw("same 3")

    inputGraphName = "Limits_{0}/Option_{1}/CentralLimit_{0}_{1}_massX_{2}".format(args.year, append, xMass)
    theGraph = inputFile.Get(inputGraphName)

    theGraph.SetLineColor(color)
    theGraph.SetLineStyle(7)
    # theGraph.SetMarkerColor(color)
    theGraph.SetLineWidth(2)
    # theGraph.SetMarkerStyle(20)
    # theGraph.SetMarkerSize(0.7)
    theGraph.Draw("same pl")

    N_points = theGraph.GetN()
    x, y = ROOT.Double(0), ROOT.Double(0)
    multiplier = ROOT.Double(1)
    # print(N_points)
    with open('limitValues.txt', mode='a') as f:
        f.write("{}\n".format(args.year))
        for i in xrange(N_points):
            theGraph.GetPoint(i, x, y)
            if xMass<600: multiplier = 100
            elif xMass<1600: multiplier = 10
            else: multiplier = 1
            r = y/multiplier
            f.write("MX = {0} MY = {1}: Cent Exp. r val = {2:.2f}\n".format(xMass,x,r))



    inputGraphName = "Limits_{0}/Option_{1}/ObservedLimit_{0}_{1}_massX_{2}".format(args.year, append, xMass)
    theGraphObserved = inputFile.Get(inputGraphName)
    theGraphObserved.SetLineColor(ROOT.kBlack)
    theGraphObserved.SetLineStyle(7)
    theGraphObserved.SetMarkerColor(ROOT.kBlack)
    theGraphObserved.SetLineWidth(2)
    theGraphObserved.SetMarkerStyle(20)
    theGraphObserved.SetMarkerSize(0.7)
    #  theGraphObserved.Draw("same pl")

    theLegend.AddEntry(theGraph, "Median expected", "lp")
    theLegend.AddEntry(theGraph1sigma, "68% expected"                             , "f" )
    theLegend.AddEntry(theGraph2sigma, "95% expected"                             , "f" )
    #  theLegend.AddEntry(theGraphObserved, "Observed", "lp")


    theLegend.Draw("same")
    theCanvas.SaveAs("Limits{0}_Limits_{1}_mX_{2}.png".format(args.year, append, xMass))
    del theCanvas

inputFile.Close()
