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

#  xMassList = [300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1400, 1600, 1800, 2000]
xMassList = [400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1400, 1600]

inputFile = TFile(args.input)
hMean = TH1D( 'hMean', 'hMean', 50, -4.1, 4.1 )
for xMass in xMassList:
    inputGraph2sigmaName = "Limits_%s/Option_%s/2SigmaLimit_%s_%s_massX_%i" % (year, append,year, append, xMass)
    theGraph2sigma = inputFile.Get(inputGraph2sigmaName)

    inputGraph1sigmaName = "Limits_%s/Option_%s/1SigmaLimit_%s_%s_massX_%i" % (year, append,year, append, xMass)
    theGraph1sigma = inputFile.Get(inputGraph1sigmaName)

    inputGraphName = "Limits_%s/Option_%s/CentralLimit_%s_%s_massX_%i" % (year, append,year, append, xMass)
    theGraphExp = inputFile.Get(inputGraphName)

    inputGraphName = "Limits_%s/Option_%s/ObservedLimit_%s_%s_massX_%i" % (year, append,year, append, xMass)
    theGraphObs = inputFile.Get(inputGraphName)

    N_points = theGraphObs.GetN()
    xObs, yObs = ROOT.Double(0), ROOT.Double(0)
    xExp, yExp = ROOT.Double(0), ROOT.Double(0)
    # xSig, ySig = ROOT.Double(0), ROOT.Double(0)
    for i in range(N_points):
        theGraphObs.GetPoint(i, xObs, yObs)
        theGraphExp.GetPoint(i, xExp, yExp)
        diff = yObs-yExp
        #  print ("diff {}".format(diff))
        if diff>=0: ySig = theGraph1sigma.GetErrorYhigh(i)
        else: ySig= theGraph1sigma.GetErrorYlow(i)
        # print("sigma: {}".format(ySig))
        hMean.Fill( diff/ySig )

theCanvas = TCanvas("limitsMean", "limitsMean", 800, 600)
# theCanvas.SetLogy()
gStyle.SetOptStat(0) # remove the stats box
gStyle.SetOptTitle(0) # remove the title
gPad.SetTicks(1,1)
gPad.SetMargin(0.12,0.05,0.12,0.09) #left,right,bottom,top
# theLegend.SetNColumns(2);

#  theLegend  = TLegend(0.65,0.7,0.9,0.88)
#  theLegend.SetTextSize(0.04)
#  theLegend.SetBorderSize(0) # remove the border
#  theLegend.SetLineColor(0)
#  theLegend.SetFillColor(0)
#  theLegend.SetTextSize(0.035)
#  theLegend.SetFillStyle(0) # make the legend background transparent
#  theLegend.AddEntry(theGraph, "Median expected", "lp")
#  theLegend.AddEntry(theGraph1sigma, "68% expected", "f" )
#  theLegend.AddEntry(theGraph2sigma, "95% expected", "f" )
#  theLegend.AddEntry(theGraphObserved, "Observed", "lp")
#  theLegend.AddEntry(hMean, "(Obs-Exp)/sigma", "p")
hMean.SetMarkerStyle(8)
hMean.SetMarkerSize(0.8)
hMean.SetLineWidth(2)
hMean.GetXaxis().SetTitle("(Obs-Exp)/sigma")
hMean.GetYaxis().SetTitle("Entries")
hMean.Draw("hist")
hMean.GetXaxis().SetRangeUser(-4.5, 4.5)
hMean.GetYaxis().SetRangeUser(0,15)
CMSlabel = TLatex()
CMSlabel.SetTextFont(63)
CMSlabel.SetTextSize(30)
CMSlabel.DrawLatexNDC(0.15, 0.92, "CMS #scale[0.8]{#it{#bf{Work In Progress}}}")
myLabels = TLatex()
myLabels.SetTextFont(63)
myLabels.SetTextSize( 22 )
#  myLabels.DrawLatexNDC(0.75, 0.93, "m_{X} = %i GeV"%(xMass))
#  myLabels.SetTextFont(53)
#  myLabels.SetTextSize( 22 )
myLabels.SetTextFont(53)
myLabels.SetTextSize(20)
if(args.year == "RunII"): myLabels.DrawTextNDC(0.7, 0.93, "2016, 2017, 2018")
else: myLabels.DrawTextNDC(0.83, 0.93, args.year)
myLabels.SetTextFont(63)
myLabels.SetTextSize( 22 )
if "VR" in args.input:
    myLabels.DrawLatexNDC(0.2, 0.84, "Validation Region")
    print("{2}: {0} for {1}".format(hMean.GetMean(),"VR", args.year))
if "CR" in args.input:  
    myLabels.DrawLatexNDC(0.2, 0.84, "Control Region")
    print("{2}: {0} for {1}".format(hMean.GetMean(),"CR", args.year))

# theLegend.Draw("same")
lastSlash = args.input.rfind("/")
theDir = args.input[:lastSlash]
path = "%s/%sMean/"%(theDir, args.year)
if not (os.path.exists(path)): os.makedirs(path) 
#  tag= "allMassPoints"
tag= ""
theCanvas.SaveAs(path + "Limits" + year + "_Limits_" + append + tag + ".pdf")
#  theCanvas.SaveAs(path + "Limits" + year + "_Limits_" + append + ".png")
# del theCanvas

inputFile.Close()
