from ROOT import TH2D, TCanvas, TFile, TGraphAsymmErrors, TGraph, TLegend, TBox, TMarker
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

args = parser.parse_args()

append = "statOnly"
if args.systematics : append = "syst"
colorList = [ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kCyan]

yMassList = [60, 70, 80, 90, 100, 125, 150, 200, 250, 300, 400, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800]

massGroupRange = {0 : [280, 620], 1 : [680, 820], 2 : [880, 1020], 3 : [1080, 1420], 4 : [1580, 2020]}

for yMass in yMassList:
    inputFile = TFile("Limits_fullSubmission_v44.root")
    theCanvas = TCanvas("limitMapCentral", "limitMapCentral", 1200, 800)
    theLegend  = TLegend(0.47,0.6,0.88,0.88)
    theLegend.SetTextSize(0.04)
    # theLegend.SetNColumns(2);

    theCanvas.SetLogy()

    inputGraphName = "Limits_RunII/Option_%s/CentralLimit_RunII_%s_massY_%i" % (append, append, yMass)
    theGraph = inputFile.Get(inputGraphName)
    theGraph.SetLineColor(ROOT.kBlack)
    # theGraph.SetLineStyle(7)
    # theGraph.SetMarkerColor(color)
    theGraph.SetLineWidth(3)
    # theGraph.SetMarkerStyle(20)
    # theGraph.SetMarkerSize(0.7)
    theGraph.Draw("apl")

    theLegend.AddEntry(theGraph, "Full plane", "lp")

    theMarkerList = []
    marketCounter = 0

    for massGroup in range(0, 5):
        inputFileGroup = TFile("Limits_" + args.tag + "_massGroup" + str(massGroup) + ".root")
        inputGraphNameGroup = "Limits_RunII/Option_%s/CentralLimit_RunII_%s_massY_%i" % (append, append, yMass)
        theGraphGroup = inputFileGroup.Get(inputGraphNameGroup)
        theGraphGroup.SetLineColor(colorList[massGroup])
        theGraphGroup.SetLineStyle(7)
        theGraphGroup.SetMarkerColor(colorList[massGroup])
        theGraphGroup.SetLineWidth(2)
        theGraphGroup.SetMarkerStyle(20)
        theGraphGroup.SetMarkerSize(0.)
        theGraphGroup.Draw("pl same")
        theLegend.AddEntry(theGraphGroup, "Mass Group " + str(massGroup) , "lp")

        for point in range (0, theGraphGroup.GetN()):
            pointX  = array('d',[0])
            pointY = array('d',[0])
            theGraphGroup.GetPoint(point, pointX, pointY)
            if pointX[0] > massGroupRange[massGroup][0] and pointX[0] < massGroupRange[massGroup][1]:
                print massGroup, pointX[0]
                theMarkerList.append(TMarker(pointX[0], pointY[0], 20))
                theMarkerList[marketCounter].SetMarkerStyle(20)
                theMarkerList[marketCounter].SetMarkerColor(colorList[massGroup])
                theMarkerList[marketCounter].Draw("same")
                marketCounter += 1

        # theBox = TBox(massGroupRange[massGroup][0], theGraph.GetYaxis().GetXmin(), massGroupRange[massGroup][1], theGraph.GetYaxis().GetXmax())
        # theBox.SetLineColor(colorList[massGroup])
        # theBox.SetLineWidth(2)
        # theBox.SetFillStyle(0)
        # theBox.Draw("same")



    theLegend.Draw("same")
    theCanvas.SaveAs("LimitsRunII_Limits_" + append +  "_mY_" + str(yMass) + ".png")

inputFile.Close()
