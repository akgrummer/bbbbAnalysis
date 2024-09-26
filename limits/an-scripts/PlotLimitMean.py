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
parser.add_argument('--systematics'   , dest='systematics'   , help='systematics'   , action="store_true", default = False, required = False)
parser.add_argument('--freezeBKGnorm'   , dest='freezeBKGnorm'   , help='freezeBKGnorm'   , action="store_true", default = False, required = False)
parser.add_argument('--listX', dest='listX', default=False, action='store_true', required=False)
parser.add_argument('--use2sig', dest='use2sig', default=False, action='store_true', required=False)

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
# yMassList = [60, 70, 80, 90, 100, 125, 150, 200, 250, 300, 400, 500,600, 700, 800, 900, 1000, 1200, 1400]
yMassList = [60, 70, 80, 90, 100, 125, 150, 190, 200, 250, 300, 350, 400, 450, 500,600, 700, 800, 900, 1000, 1200, 1400]
xMassList = [400, 500, 600, 650, 700, 800, 900, 1000, 1100, 1200, 1400, 1600]
massList = yMassList
massXY="Y"
othermassXY="X"

if args.listX:
    massList = xMassList
    massXY = "X"
    othermassXY="Y"
else:
    massList = yMassList
    massXY = "Y"
    othermassXY="X"
# massList = xMassList
# massXY="X"
# othermassXY="Y"

ifile="hists/Limits_{0}.root".format(args.tag)
inputFile = TFile(ifile)
hMean = TH1D( 'hMean', 'hMean', 10, -5., 5. )
for theMass in massList:
    inputGraph2sigmaName = "Limits_{0}/Option_{1}/2SigmaLimit_{0}_{1}_mass{2}_{3}".format(args.year, append, massXY, theMass)
    theGraph2sigma = inputFile.Get(inputGraph2sigmaName)

    inputGraph1sigmaName = "Limits_{0}/Option_{1}/1SigmaLimit_{0}_{1}_mass{2}_{3}".format(args.year, append, massXY, theMass)
    theGraph1sigma = inputFile.Get(inputGraph1sigmaName)

    inputGraphName = "Limits_{0}/Option_{1}/CentralLimit_{0}_{1}_mass{2}_{3}".format(args.year, append, massXY, theMass)
    theGraphExp = inputFile.Get(inputGraphName)

    inputGraphName = "Limits_{0}/Option_{1}/ObservedLimit_{0}_{1}_mass{2}_{3}".format(args.year, append, massXY, theMass)
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
        if(args.use2sig):
            if diff>=0: ySig = theGraph2sigma.GetErrorYhigh(i)/2
            else: ySig= theGraph2sigma.GetErrorYlow(i)/2
        else:
            if diff>=0: ySig = theGraph1sigma.GetErrorYhigh(i)
            else: ySig= theGraph1sigma.GetErrorYlow(i)
        # print("sigma: {}".format(ySig))
        pull =  diff/ySig
        # if (pull>2.5): print( "m{0}=({1},{2}), m{3}={4}, yObs={5}, yExp={6}, pull={7}".format(massXY, xObs, xExp, othermassXY, theMass, yObs, yExp, pull ))
        # if (pull>3.4): print( "m{0}={1}, m{3}={4}, yObs={5:.4f}, yExp={6:.4f}, pull={7:.4f}".format(massXY, xObs, xExp, othermassXY, theMass, yObs, yExp, pull ))
        if (pull>4. and not args.listX and not args.use2sig): print( "m{0}={1}, m{3}={4}, yObs={5:.4f}, yExp={6:.4f}, pull={7:.4f}".format(massXY, xObs, xExp, othermassXY, theMass, yObs, yExp, pull ))
        if (pull<-2.0 and not args.listX and not args.use2sig): print( "m{0}={1}, m{3}={4}, yObs={5:.4f}, yExp={6:.4f}, pull={7:.4f}".format(massXY, xObs, xExp, othermassXY, theMass, yObs, yExp, pull ))
        hMean.Fill(pull)

theCanvas = TCanvas("limitsMean", "limitsMean", 800, 600)
# theCanvas.SetLogy()
gStyle.SetOptStat(0) # remove the stats box
gStyle.SetOptTitle(0) # remove the title
gPad.SetTicks(1,1)
gPad.SetMargin(0.12,0.05,0.12,0.09) #left,right,bottom,top
hMean.SetMarkerStyle(8)
hMean.SetMarkerSize(0.8)
hMean.SetLineWidth(2)
hMean.GetXaxis().SetTitle("(Obs-Exp)/#sigma")
hMean.GetYaxis().SetTitle("Entries")
hMean.Draw("hist")
hMean.GetXaxis().SetRangeUser(-5.2, 5.2)
hMean.GetYaxis().SetRangeUser(0,hMean.GetMaximum()*1.3)

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

plotlabels.DrawTextNDC(0.2, 0.76, "Mean: {:0.4f}".format(hMean.GetMean()))
plotlabels.DrawTextNDC(0.2, 0.72, "Std. Dev.: {:.4f}".format(hMean.GetStdDev()))

labelText = ""
if "VR" in args.tag:      labelText = labelText + "Validation Region"
if "CR" in args.tag:      labelText = labelText + "Control Region"
if "SR" in args.tag:      labelText = labelText + "Signal Region"
plotlabels.SetTextFont(63)
plotlabels.SetTextSize(20)
plotlabels.DrawTextNDC(0.6, 0.82, labelText)

odir = "results/Limits_{0}/".format(args.tag)
if not os.path.isdir(odir):
    os.mkdir(odir)
odir = "{0}{1}/".format(odir,"unblinded")
if not os.path.isdir(odir):
    os.mkdir(odir)
odir = "{0}{1}/".format(odir,"mean")
if not os.path.isdir(odir):
    os.mkdir(odir)

ofile = "Limits{0}_{1}_{2}".format(args.year, append, args.tag)
if(args.listX): ofile = "{0}_{1}".format(ofile,massXY)
if (args.use2sig): ofile = "{0}_{1}".format(ofile,"2sigma")
ofile = "{0}{1}".format(ofile,".pdf")
theCanvas.SaveAs(odir+ofile)

inputFile.Close()

