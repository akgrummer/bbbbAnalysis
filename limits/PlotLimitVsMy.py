from ROOT import TH2D, TCanvas, TFile, TGraphAsymmErrors, TGraph, TLegend, TPad, gPad, TLatex, gStyle
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
parser.add_argument('--year'    , dest = 'year'    , help = 'year to run over: 201{6-8},RunII' , required = True)
parser.add_argument('--systematics'   , dest='systematics'   , help='systematics'   , action="store_true", default = False, required = False)
parser.add_argument('--freezeBKGnorm'   , dest='freezeBKGnorm'   , help='freezeBKGnorm'   , action="store_true", default = False, required = False)

args = parser.parse_args()

append = "statOnly"
if args.systematics : append = "syst"
if args.freezeBKGnorm : append = "freezeBKGnorm"
color     = ROOT.kBlue
#  year = "RunII"
#  year = "2016"
year = ""
year = args.year

xMassList = [300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1400, 1600, 1800, 2000]
#  xMassList = [300]

inputFile = TFile(args.input)

for xMass in xMassList:
    theCanvas = TCanvas("limitMapCentral", "limitMapCentral", 800, 600)
    gStyle.SetOptStat(0) # remove the stats box
    gStyle.SetOptTitle(0) # remove the title
    theLegend  = TLegend(0.65,0.7,0.9,0.88)
    theLegend.SetTextSize(0.04)
    gPad.SetTicks(1,1)
    # theLegend.SetNColumns(2);
    gPad.SetMargin(0.12,0.05,0.12,0.09) #left,right,bottom,top

    theCanvas.SetLogy()

    inputGraph2sigmaName = "Limits_%s/Option_%s/2SigmaLimit_%s_%s_massX_%i" % (year, append,year, append, xMass)
    print(inputGraph2sigmaName)
    theGraph2sigma = inputFile.Get(inputGraph2sigmaName)
    theGraph2sigma.SetTitle("")
    theGraph2sigma.GetXaxis().SetTitle("m_{Y} [GeV]")
    theGraph2sigma.GetXaxis().SetLabelFont(42)
    theGraph2sigma.GetXaxis().SetLabelSize(0.045)
    theGraph2sigma.GetXaxis().SetTitleFont(42)
    theGraph2sigma.GetXaxis().SetTitleSize(0.045)
    theGraph2sigma.GetXaxis().SetTitleOffset(1.2)
    theGraph2sigma.GetYaxis().SetLabelFont(42)
    theGraph2sigma.GetYaxis().SetLabelSize(0.045)
    theGraph2sigma.GetYaxis().SetTitleFont(42)
    theGraph2sigma.GetYaxis().SetTitleSize(0.045)
    theGraph2sigma.GetYaxis().SetTitle("#sigma(pp #rightarrow X) #times BR(Y(b#bar{b}) H(b#bar{b})) [fb]")
    theGraph2sigma.GetYaxis().SetTitleOffset(1.2)
    theGraph2sigma.GetYaxis().SetRangeUser(1.,1.e5)
    #  theGraph2sigma.GetYaxis().SetRangeUser(0.,2000)
    theGraph2sigma.GetXaxis().SetRangeUser(50.,1900.)
    #  theGraph2sigma.SetTitle("m_{X} = %i GeV"%(xMass))
    theGraph2sigma.Draw("a3")

    inputGraph1sigmaName = "Limits_%s/Option_%s/1SigmaLimit_%s_%s_massX_%i" % (year, append,year, append, xMass)
    theGraph1sigma = inputFile.Get(inputGraph1sigmaName)
    theGraph1sigma.Draw("same 3")

    inputGraphName = "Limits_%s/Option_%s/CentralLimit_%s_%s_massX_%i" % (year, append,year, append, xMass)
    theGraph = inputFile.Get(inputGraphName)
    theGraph.SetLineColor(color)
    theGraph.SetLineStyle(7)
    # theGraph.SetMarkerColor(color)
    theGraph.SetLineWidth(2)
    # theGraph.SetMarkerStyle(20)
    # theGraph.SetMarkerSize(0.7)
    theGraph.Draw("same pl")


    inputGraphName = "Limits_%s/Option_%s/ObservedLimit_%s_%s_massX_%i" % (year, append,year, append, xMass)
    theGraphObserved = inputFile.Get(inputGraphName)
    theGraphObserved.SetLineColor(ROOT.kBlack)
    theGraphObserved.SetLineStyle(7)
    theGraphObserved.SetMarkerColor(ROOT.kBlack)
    theGraphObserved.SetLineWidth(2)
    theGraphObserved.SetMarkerStyle(20)
    theGraphObserved.SetMarkerSize(0.7)
    theGraphObserved.Draw("same pl")

    theLegend.SetBorderSize(0) # remove the border
    theLegend.SetLineColor(0)
    theLegend.SetFillColor(0)
    theLegend.SetTextSize(0.035)
    theLegend.SetFillStyle(0) # make the legend background transparent
    theLegend.AddEntry(theGraph, "Median expected", "lp")
    theLegend.AddEntry(theGraph1sigma, "68% expected"                             , "f" )
    theLegend.AddEntry(theGraph2sigma, "95% expected"                             , "f" )
    theLegend.AddEntry(theGraphObserved, "Observed", "lp")
    CMSlabel = TLatex()
    CMSlabel.SetTextFont(63)
    CMSlabel.SetTextSize(30)
    CMSlabel.DrawLatexNDC(0.15, 0.92, "CMS #scale[0.8]{#it{#bf{Work In Progress}}}")
    myLabels = TLatex()
    myLabels.SetTextFont(63)
    myLabels.SetTextSize( 22 )
    myLabels.DrawLatexNDC(0.75, 0.93, "m_{X} = %i GeV"%(xMass))
    myLabels.SetTextFont(53)
    myLabels.SetTextSize( 22 )
    if(args.year == "RunII"): myLabels.DrawTextNDC(0.2, 0.8, "2016, 2017, 2018")
    else: myLabels.DrawTextNDC(0.2, 0.8, args.year)
    myLabels.SetTextFont(63)
    myLabels.SetTextSize( 22 )
    if "VR" in args.input:    myLabels.DrawLatexNDC(0.2, 0.84, "Validation Region")
    if "CR" in args.input:    myLabels.DrawLatexNDC(0.2, 0.84, "Control Region")

    theLegend.Draw("same")
    lastSlash = args.input.rfind("/")
    theDir = args.input[:lastSlash]
    #  path = "%s/%sLinear/"%(theDir, args.year)
    path = "%s/%s/"%(theDir, args.year)
    if not (os.path.exists(path)): os.makedirs(path) 
    theCanvas.SaveAs(path + "Limits" + year + "_Limits_" + append +  "_mX_" + str(xMass) + ".pdf")
    # theCanvas.SaveAs(path + "Limits" + year + "_Limits_" + append +  "_mX_" + str(xMass) + ".png")
    del theCanvas

inputFile.Close()
