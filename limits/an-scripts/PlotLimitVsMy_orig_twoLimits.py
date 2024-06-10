from ROOT import TH2D, TCanvas, TFile, TGraphAsymmErrors, TGraph, TLegend, TLatex
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
parser.add_argument('--limitType', dest='limitType',  help = 'obs to run the Observed limit comparison' , required=False)


args = parser.parse_args()

append = "statOnly"
if args.systematics : append = "syst"
color     = ROOT.kBlue

#  xMassList = [300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1400, 1600, 1800, 2000]
xMassList = [400, 500, 600, 650, 700, 800, 900, 1000, 1100, 1200, 1400, 1600]
yMassList = [60, 70, 80, 90, 100, 125, 150, 200, 250, 300, 400, 500,600, 700, 800, 900, 1000, 1200, 1400]
if args.vsMY:
    massList = yMassList
    massXY = "Y"
else:
    massList = xMassList
    massXY = "X"

inputFile1 = TFile(args.input, "READ")
inputFile2 = TFile(args.input2, "READ")

if args.limitType=="obs":
    limitType1 = "Observed"
    limitType2 = "Observed"
else:
    limitType1 = "Central"
    limitType2 = "Expected"

for theMass in massList:
    theCanvas = TCanvas("limitMap{0}".format(limitType1), "limitMap{0}".format(limitType1), 1200, 800)
    theLegend  = TLegend(0.17,0.7,0.5,0.8)
    theLegend.SetBorderSize(0) # remove the border
    theLegend.SetLineColor(0)
    theLegend.SetFillColor(0)
    theLegend.SetTextSize(0.025)
    theLegend.SetFillStyle(0) # make the legend background transparent
    # theLegend.SetNColumns(2);

    theCanvas.SetLogy()

    # inputGraph1 = "Limits_{0}/Option_{1}/CentralLimit_{0}_{1}_mass{2}_{3}".format(args.year, append, massXY, theMass)
    inputGraph1 = "Limits_{0}/Option_{1}/{4}Limit_{0}_{1}_mass{2}_{3}".format(args.year, append, massXY, theMass, limitType1)
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
    # if not args.vsMY:
    #     if (theMass<500):
    #         theGraph1.SetMinimum(90.)
    #         theGraph1.SetMaximum(500.)
    #     elif (theMass<600):
    #         theGraph1.SetMinimum(20.)
    #         theGraph1.SetMaximum(200.)
    #     elif (theMass<700):
    #         theGraph1.SetMinimum(10.)
    #         theGraph1.SetMaximum(100.)
    #     elif (theMass<800):
    #         theGraph1.SetMinimum(10.)
    #         theGraph1.SetMaximum(90.)
    #     elif (theMass<1000):
    #         theGraph1.SetMinimum(5.)
    #         theGraph1.SetMaximum(100)
    #     else:
    #         theGraph1.SetMinimum(1.)
    #         theGraph1.SetMaximum(40)
    theGraph1.GetXaxis().SetRangeUser(50.,1900.)
    theGraph1.GetYaxis().SetRangeUser(5e-1,1.e5)
    theGraph1.SetTitle("")
    theGraph1.SetLineColor(color)
    theGraph1.SetLineWidth(1)
    theGraph1.Draw("apl")

    inputGraph2 = "Limits_{0}/Option_{1}/{4}Limit_{0}_{1}_mass{2}_{3}".format(args.year, append, massXY, theMass,limitType1)
    theGraph2 = inputFile2.Get(inputGraph2)
    theGraph2.SetLineColor(ROOT.kRed+2)
    theGraph2.SetLineWidth(1)


    theGraph2.Draw("plsame")

    x, y = ROOT.Double(0), ROOT.Double(0)
    multiplier = ROOT.Double(1)

    CMSlabel = TLatex()
    CMSlabel.SetTextFont(63)
    CMSlabel.SetTextSize(30)
    CMSlabel.DrawLatexNDC(0.15, 0.92, "CMS #scale[0.8]{#it{#bf{Work In Progress}}}")
    myLabels = TLatex()
    myLabels.SetTextFont(53)
    myLabels.SetTextSize( 22 )
    if(args.year == "RunII"): myLabels.DrawTextNDC(0.7, 0.92, "2016, 2017, 2018")
    else: myLabels.DrawTextNDC(0.7, 0.92, args.year)
    myLabels.SetTextFont(43)
    myLabels.SetTextSize( 22 )
    myLabels.DrawLatexNDC(0.5, 0.92, "m_{%s} = %i GeV"%(massXY,theMass))
    myLabels.SetTextFont(63)
    myLabels.SetTextSize( 22 )
    if "SR" in args.input:    myLabels.DrawLatexNDC(0.2, 0.84, "Signal Region")
    if "VR" in args.input:    myLabels.DrawLatexNDC(0.2, 0.84, "Validation Region")
    if "CR" in args.input:    myLabels.DrawLatexNDC(0.2, 0.84, "Control Region")
    myLabels.SetTextFont(43)
    myLabels.SetTextSize( 20 )
    myLabels.DrawLatexNDC(0.2, 0.8, "{0} limit".format(limitType2))

    # theLegend.AddEntry(theGraph1, "Median expected limit w/o extra unc.", "lp")
    # theLegend.AddEntry(theGraph1, "Median expected limit old non-closure", "lp")
    # theLegend.AddEntry(theGraph2, "Median expected limit new non-closure, new bins", "lp")
    #
    # theLegend.AddEntry(theGraph1, "before adding signal", "lp")
    # theLegend.AddEntry(theGraph2, "after adding 2017 MC mX=1000,mY=150 GeV", "lp")
    theLegend.AddEntry(theGraph1, "with mass groups", "lp")
    theLegend.AddEntry(theGraph2, "without mass groups", "lp")

    theLegend.Draw("same")
    theCanvas.SaveAs("results/TwoLimits/temp/{4}/TwoLimits{0}_{1}_m{2}_{3}.pdf".format(args.year, append,massXY, theMass, limitType2))


    del theCanvas

inputFile1.Close()
inputFile2.Close()

