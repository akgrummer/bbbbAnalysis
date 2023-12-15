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
parser.add_argument('--tag'    , dest = 'tag'    , help = 'tag file' , required = True)
parser.add_argument('--systematics'   , dest='systematics'   , help='systematics'   , action="store_true", default = False, required = False)
parser.add_argument('--year'   , dest='year'   , help='run year, 2016,2017,2018,RunII', default = "RunII", required = False)
parser.add_argument('--vsMY', dest='vsMY', default=False, action='store_true', required=False)
parser.add_argument('--unblind'   , dest='unblind'   , help='plot the observed graph also', action='store_true', default = False, required = False)

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
    othermassXY="X"
else:
    massList = xMassList
    massXY = "X"
    othermassXY="Y"

ifile="hists/Limits_{0}.root".format(args.tag)
inputFile = TFile(ifile)

for theMass in massList:
    theCanvas = TCanvas("limitMapCentral", "limitMapCentral", 800, 600)
    ROOT.gStyle.SetOptStat(0) # remove the stats box
    ROOT.gStyle.SetOptTitle(0) # remove the title
    theLegend  = TLegend(0.17,0.65,0.5,0.88)
    theLegend.SetTextSize(0.04)
    theCanvas.SetLogy()
    theCanvas.SetTicks(1,1)
    # theLegend.SetNColumns(2);


    inputGraph2sigmaName = "Limits_{0}/Option_{1}/2SigmaLimit_{0}_{1}_mass{2}_{3}".format(args.year, append, massXY, theMass)
    # print("here", inputGraph2sigmaName)
    theGraph2sigma = inputFile.Get(inputGraph2sigmaName)
    theGraph2sigma.SetTitle("")
    theGraph2sigma.GetXaxis().SetTitle("m_{%s} [GeV]"%(othermassXY))
    theGraph2sigma.GetXaxis().SetLabelFont(62)
    theGraph2sigma.GetXaxis().SetLabelSize(0.045)
    theGraph2sigma.GetXaxis().SetTitleFont(62)
    theGraph2sigma.GetXaxis().SetTitleSize(0.045)
    theGraph2sigma.GetYaxis().SetLabelFont(62)
    theGraph2sigma.GetYaxis().SetLabelSize(0.045)
    theGraph2sigma.GetYaxis().SetTitleFont(62)
    theGraph2sigma.GetYaxis().SetTitleSize(0.045)
    theGraph2sigma.GetYaxis().SetTitle("#sigma(pp #rightarrow X) #times BR(Y(b#bar{b}) H(b#bar{b})) [fb]")
    theGraph2sigma.GetYaxis().SetRangeUser(5e-1,1.e5)
    theGraph2sigma.GetXaxis().SetRangeUser(50.,1900.)
    theGraph2sigma.SetTitle("m_{%s} = %i GeV"%(massXY,theMass))
    theGraph2sigma.Draw("a3")

    inputGraph1sigmaName = "Limits_{0}/Option_{1}/1SigmaLimit_{0}_{1}_mass{2}_{3}".format(args.year, append, massXY, theMass)
    theGraph1sigma = inputFile.Get(inputGraph1sigmaName)
    theGraph1sigma.Draw("same 3")

    inputGraphName = "Limits_{0}/Option_{1}/CentralLimit_{0}_{1}_mass{2}_{3}".format(args.year, append, massXY, theMass)
    theGraph = inputFile.Get(inputGraphName)

    theGraph.SetLineColor(color)
    theGraph.SetLineStyle(7)
    theGraph.SetMarkerColor(color)
    theGraph.SetLineWidth(2)
    theGraph.SetMarkerStyle(22)
    theGraph.SetMarkerSize(0.7)
    theGraph.Draw("same pl")





    inputGraphName = "Limits_{0}/Option_{1}/ObservedLimit_{0}_{1}_mass{2}_{3}".format(args.year, append, massXY, theMass)
    theGraphObserved = inputFile.Get(inputGraphName)
    theGraphObserved.SetLineColor(ROOT.kBlack)
    theGraphObserved.SetLineStyle(1)
    theGraphObserved.SetMarkerColor(ROOT.kBlack)
    theGraphObserved.SetLineWidth(2)
    theGraphObserved.SetMarkerStyle(20)
    theGraphObserved.SetMarkerSize(0.7)
    if (args.unblind): theGraphObserved.Draw("same pl")

    theGraph2sigma.GetYaxis().SetTitleOffset(1.1)

    CMSlabel = TLatex()
    CMSlabel.SetTextFont(63)
    CMSlabel.SetTextSize( 30 )
    CMSlabel.DrawLatexNDC(0.12, 0.93, "CMS #scale[0.8]{#it{#bf{Work In Progress}}}")

    plotlabels = TLatex()
    plotlabels.SetTextFont(43)
    plotlabels.SetTextSize(20)
    plotlabels.DrawLatexNDC(0.60, 0.75, "m{0} = {1} GeV".format(massXY, theMass))
    plotlabels.SetTextFont(53)
    plotlabels.SetTextSize(20)
    if("RunII" in args.year): yearLabel="Full Run II Data"
    else: yearLabel = args.year
    plotlabels.DrawTextNDC(0.72, 0.93, yearLabel)

    labelText = ""
    if "VR" in args.tag:      labelText = labelText + "Validation Region"
    if "CR" in args.tag:      labelText = labelText + "Control Region"
    if "SR" in args.tag:      labelText = labelText + "Signal Region"
    plotlabels.SetTextFont(63)
    plotlabels.SetTextSize(20)
    plotlabels.DrawTextNDC(0.6, 0.82, labelText)

    theLegend.AddEntry(theGraph, "Median expected", "lp")
    theLegend.AddEntry(theGraph1sigma, "68% expected"                             , "f" )
    theLegend.AddEntry(theGraph2sigma, "95% expected"                             , "f" )
    if (args.unblind): theLegend.AddEntry(theGraphObserved, "Observed", "lp")
    theLegend.SetBorderSize(0) # remove the border
    theLegend.SetLineColor(0)
    theLegend.SetFillColor(0)
    theLegend.SetTextSize(0.035)
    theLegend.SetFillStyle(0) # make the legend background transparent
    theLegend.Draw("same")


    odir = "results/Limits_{0}/".format(args.tag)
    if not os.path.isdir(odir):
        os.mkdir(odir)
    if (args.unblind): odir = "{0}{1}/".format(odir,"unblinded")
    else: odir = "{0}{1}/".format(odir,"blinded")
    if not os.path.isdir(odir):
        os.mkdir(odir)
    odir = "{0}{1}/".format(odir,"vsm{0}".format(massXY))
    if not os.path.isdir(odir):
        os.mkdir(odir)
    odir = "{0}{1}/".format(odir,args.year)
    if not os.path.isdir(odir):
        os.mkdir(odir)

    # N_points = theGraph.GetN()
    # x, y = ROOT.Double(0), ROOT.Double(0)
    # multiplier = ROOT.Double(1)
    # print(N_points)
    # with open(odir+'limitValues.txt', mode='a') as f:
    #     f.write("{}\n".format(args.year))
    #     for i in xrange(N_points):
    #         theGraph.GetPoint(i, x, y)
    #         if theMass<600: multiplier = 100
    #         elif theMass<1600: multiplier = 10
    #         else: multiplier = 1
    #         r = y/multiplier
    #         f.write("MX = {0} MY = {1}: Cent Exp. r val = {2:.2f}\n".format(theMass,x,r))


    theCanvas.SaveAs(odir+"Limits{0}_Limits_{1}_m{2}_{3}.pdf".format(args.year, append, massXY, theMass))
    del theCanvas

inputFile.Close()
