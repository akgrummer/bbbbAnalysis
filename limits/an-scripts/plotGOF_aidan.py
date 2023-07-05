import ROOT
from ROOT import TLatex
import sys
import os
import glob
import shutil
import getpass
import argparse
from subprocess import call, check_output
from optparse import OptionParser

# import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
# import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
# import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
# import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles

#================================================================================================
# Custom colours (https://www.color-hex.com)
#================================================================================================
kDarkBlue = ROOT.TColor.GetColor("#001ee2")
kBlue     = ROOT.TColor.GetColor("#8097cc")
kLightBlue= ROOT.TColor.GetColor("#a6b6db")
kRed      = ROOT.TColor.GetColor("#e23222")
kLightRed = ROOT.TColor.GetColor("#FCD0D1")

parser = argparse.ArgumentParser(description='Command line parser of GOF plotting options')
parser.add_argument('--year'       ,  dest = 'year'       ,  help = 'year to plot'           ,  required = True        )
# parser.add_argument('--masspoint'       ,  dest = 'masspoint'       ,  help = 'mass point to plot'           ,  required = True        )
parser.add_argument('--algo'       ,  dest = 'algo'       ,  help = 'GoF algorithm', default=""  ,  required = False        )
parser.add_argument('--tag'       ,  dest = 'tag'       ,  help = 'production tag'           ,  required = True        )
parser.add_argument('--samplelist'    , dest = 'samplelist'    , help = 'production tag' , required = True)

args = parser.parse_args()
# year = "2018"
# group = "1"
# year = "2016"
# year = args.year
# algo = args.algo
# if (algo == ""):
    # suffix="TF"
# else:
    # suffix="toys"
# algo = "_"+algo
# group = "0"
# masspoint="MX_900_MY_600"
# masspoint = args.masspoint
# config = {
#     # "Dir": "localCombineRuns/CombineGoF_2022Oct24_Group{1}/{0}/".format(year, group),
#     # "Dir": "localCombineRuns/CombineGoF_2023May9/{0}/".format(masspoint),
#     "Dir": "localCombineRuns/CombineGoF_2023May9/{0}/".format(masspoint),
#     # "Dir": "localCombineRuns/CombineGoF_2023May9_MX_800_MY_600_normX2/{0}/".format(masspoint),
#     # "fData": "higgsCombine{0}Group{1}data.GoodnessOfFit.mH120.root".format(year,group),
#     # "fData": "higgsCombine{0}Group{1}ADdata.GoodnessOfFit.mH120.root".format(year,group),
#     "fData": "higgsCombine_{0}{1}_{2}.GoodnessOfFit.mH120.root".format(year,algo, masspoint),
#     # "fToy": "higgsCombine{0}Group{1}.GoodnessOfFit.mH120.12345.root".format(year, group),
#     "fToy": "higgsCombine_{0}{1}_{2}_{3}.GoodnessOfFit.mH120.12345.root".format(year,algo,masspoint, suffix),
#     # "PlotLabel": "Mass Group {0}".format(group),
#     "PlotLabel": "{0}".format(masspoint),
#     "year": "{0}".format(year)
#     }
def doPlots(config):
    saveDir = config["Dir"]
    # algorithm = "AD"
    # algorithm = "saturated"
    # algorithm = "KS"
    algorithm = args.algo
    fData = ROOT.TFile(config["Dir"] + config["fData"])
    fToys = ROOT.TFile(config["Dir"] + config["fToy"])
    tToys = fToys.Get("limit")
    tData = fData.Get("limit")
    nToys = tToys.GetEntries()

    tData.GetEntry(0)
    GoF_DATA = tData.limit

    nToysTotal = 0
    pValueCum  = 0
    toys       = []
    minToy     = +99999999
    maxToy     = -99999999

    # xMin will be automatically re-adjusted
    xMin  = {}
    xMin["saturated"] = 0
    xMin["KS"] = 0.0
    xMin["AD"] = 0.0

    # xMax will be automatically re-adjusted
    xMax  = {}
    xMax["saturated"] = 2000
    xMax["KS"] = 20.0
    xMax["AD"] = 200.00
    binWidth = {}
    binWidth["saturated"] = 5 #10
    binWidth["KS"] = 0.0002 #0.002 #0.004
    binWidth["AD"] = 0.2   # 0.10 0.25 #0.5
    nBins = (xMax[algorithm]-xMin[algorithm])/binWidth[algorithm]

    hist = ROOT.TH1D("GoF-%s" % (algorithm), "", int(nBins), xMin[algorithm], xMax[algorithm])

    for i in range(0, tToys.GetEntries()):
        tToys.GetEntry(i)

        # Toys counter
        nToysTotal += tToys.limit
        toys.append(tToys.limit)
        hist.Fill(tToys.limit)

        # Accumulate p-Value if GoF_toy > GoF_data
        if tToys.limit > GoF_DATA:
            pValueCum += tToys.limit


    # Finalise p-value calculation by dividing by number of toys total
    pval = pValueCum / nToysTotal
    msg = "p-Value = %.3f (%.2f/%.2f)" % (pval, pValueCum, nToysTotal)
    print(msg)
    pvalsFile.write("{0},{1},{2:.4f}\n".format(config["MX"],config["MY"],pval))

    # Set range for x-axis and y-axis range
    xMin  = hist.GetBinLowEdge(hist.FindFirstBinAbove(0.0))*0.25 # hist.GetBinCenter(hist.FindFirstBinAbove(0.0))*0.8
    xMax  = hist.GetBinLowEdge(hist.FindLastBinAbove(0.0))*1.75  # hist.GetBinCenter(hist.FindLastBinAbove(0.0))*1.2
    yMin  = 0.0
    yMax  = hist.GetMaximum()*1.05

    # Customise canvas & histogram
    c1 = ROOT.TCanvas('c1', 'c1',800,600)
    ROOT.gStyle.SetOptStat(0) # remove the stats box
    ROOT.gStyle.SetOptTitle(0) # remove the title
    ROOT.gPad.SetTicks(1,1)
    ROOT.gPad.SetMargin(0.12,0.05,0.12,0.09) #left,right,bottom,top
    binW   = hist.GetBinWidth(0)
    yTitle = "Entries / %.2f" % (binW)
    if binW >= 5.0:
        yTitle = "Entries / %.1f" % (binW)
    elif binW >= 0.1:
        yTitle = "Entries / %.2f" % (binW)
    elif binW >= 0.01:
        yTitle = "Entries / %.3f" % (binW)
    else:
        yTitle = "Entries / %.4f" % (binW)

    hist.GetYaxis().SetTitle(yTitle ) # bin width does not change
    hist.GetXaxis().SetTitle("test-statistic t")
    hist.GetXaxis().SetTitle("test-statistic t")
    hist.SetLineColor(ROOT.kRed)
    hist.SetLineWidth(3)
    if 0:
        hist.SetFillColor(kLightRed)
    hist.GetXaxis().SetRangeUser(xMin, xMax)
    hist.GetYaxis().SetRangeUser(yMin, yMax)
    hist.GetYaxis().SetTitleOffset(1.30)
    hist.Draw()

    # Duplicate histogram for filling only part which is above GoF_DATA
    hCum = hist.Clone("Cumulative")
    for b in range(0, hCum.GetNbinsX()):
        if b < hCum.FindBin(GoF_DATA):
            hCum.SetBinContent(b, 0)
    hCum.SetLineWidth(0)
    if 1:
        hCum.SetFillColor(kLightBlue) #kLightRed)
        hCum.SetFillStyle(1001)
    else:
        hCum.SetLineWidth(3)
        hCum.SetLineColor(kLightBlue)
        hCum.SetLineStyle(ROOT.kDashed) #ROOT.kDotted)
        hCum.SetFillColor(kDarkBlue)
        hCum.SetFillStyle(3356) #3444)
    hCum.Draw("same")
    hist.Draw("same") # re-draw to get line

    # Customise arrow indicating data-observed
    tZeroX = hist.GetBinLowEdge(hist.FindBin(GoF_DATA)) # GoF_DATA
    if hist.GetBinContent(hist.FindBin(GoF_DATA)) > 0.0:
        tZeroY = hist.GetBinContent(hist.FindBin(GoF_DATA))*0.25
    else:
        tZeroY = hist.GetMaximum()/5
    arr = ROOT.TArrow(tZeroX, 0.0001, tZeroX, tZeroY, 0.02, "<|")
    arr.SetLineColor(kDarkBlue) #ROOT.kBlue)
    arr.SetFillColor(kDarkBlue) #ROOT.kBlue)
    arr.SetFillStyle(1001)
    arr.SetLineWidth(3)
    arr.SetLineStyle(1)
    arr.SetAngle(60)
    arr.Draw("<|same")

    # Add data observed value1
    left = ROOT.TLatex()
    #left.SetNDC()
    left.SetTextFont(43)
    left.SetTextSize(20)
    left.SetTextAlign(11)
    #left.DrawLatex(GoF_DATA*1.01, (hist.GetMaximum())*0.03, "#color[4]{data}")
    #left.DrawLatex(GoF_DATA*1.02, (hist.GetMaximum())*0.03, "#color[4]{t_{0}}")
    if GoF_DATA < 1.0:
        left.DrawLatex(tZeroX, tZeroY*1.1, "#color[4]{t_{0}= %.4f}" % (GoF_DATA))
    elif GoF_DATA < 10.0:
        left.DrawLatex(tZeroX, tZeroY*1.1, "#color[4]{t_{0}= %.1f}" % (GoF_DATA))
    else:
        left.DrawLatex(tZeroX, tZeroY*1.1, "#color[4]{t_{0}= %.0f}" % (GoF_DATA))

    #cms label
    CMSlabel = TLatex()
    #  CMSlabel.SetTextSize( 0.08 )
    #  CMSlabel.DrawTextNDC(0.7, 0.85, "CMS Internal")
    CMSlabel.SetTextFont(63)
    CMSlabel.SetTextSize( 30 )
    CMSlabel.DrawLatexNDC(0.12, 0.93, "CMS #scale[0.8]{#it{#bf{Work In Progress}}}")
    # Analysis text
    anaText = ROOT.TLatex()
    anaText.SetNDC()
    anaText.SetTextFont(43)
    anaText.SetTextSize(20)
    anaText.SetTextAlign(31)
    anaText.DrawLatex(0.92, 0.84, "%s model" % (algorithm) )
    anaText.SetTextFont(43)
    anaText.SetTextSize(16)
    anaText.DrawLatex(0.92, 0.80, "%s" % (msg) )
    anaText.SetTextFont(53)
    anaText.SetTextSize(20)
    anaText.DrawLatex(0.92, 0.93, "%s" % (config["year"]) )
    masses = config["PlotLabel"].split("_")
    anaText.DrawLatex(0.8, 0.93, "m_{X} = %s, m_{Y} = %s GeV" % (masses[1], masses[3] ) )

    # Add text with details of the GoF test (nToys, p-value, signal mass)
    pvalText = ROOT.TLatex()
    pvalText.SetNDC()
    pvalText.SetTextFont(43)
    pvalText.SetTextSize(16)
    pvalText.SetTextAlign(31) #11
    pvalText.DrawLatex(0.92, 0.77, "toys = %d" % nToys)
    #pvalText.DrawLatex(0.92, 0.74, "p-value = %.2f" % pval)
    # pvalText.DrawLatex(0.92, 0.74, "p-value = %.3f" % pval)
    # pvalText.DrawLatex(0.92, 0.68, "m_{H^{+}} = %s GeV" % opts.mass)
    anaText.SetTextFont(63)
    anaText.SetTextSize(18)
    if ("VR" in config["Dir"]): anaText.DrawLatex(0.92, 0.73, "Validation Region" )
    else: anaText.DrawLatex(0.92, 0.73, "Signal Region" )
    anaText.SetTextSize(16)
    if ("trim" in config["Dir"]): anaText.DrawLatex(0.92, 0.69, "new group ranges" )

    # Print some info
    print("Toys = %.0f" % (nToys))
    print("nToysTotal = %.0f" % (nToysTotal))
    print("p-value = %.2f" % (pval))

    # Add default texts
    # histograms.addStandardTexts(lumi=opts.lumi, sqrts="13 TeV", addCmsText=True, cmsTextPosition=None, cmsExtraTextPosition=None, cmsText="CMS", cmsExtraText="Internal   ")
    # histograms.addStandardTexts(sqrts="13 TeV", addCmsText=True, cmsTextPosition=None, cmsExtraTextPosition=None, cmsText="CMS", cmsExtraText="Internal   ")

    # Save the plot (not needed - drawPlot saves the canvas already)
    saveName = "GoF_{0}_{1}_{2}".format(algorithm, masspoint, config["year"])
    # SavePlot(c, saveName, saveDir, saveFormats = [".C", ".png", ".pdf"])
    SavePlot(c1, saveName, saveDir, saveFormats = [".pdf"])

    return

def SavePlot(plot, plotName, saveDir, saveFormats = [".C", ".png", ".pdf"]):
    print("Saving canvas in %s formats: %s" % (len(saveFormats), ", ".join(saveFormats) ) )

     # Check that path exists
    if not os.path.exists(saveDir):
        print("Creating directory \"%s\"" % (saveDir))
        os.makedirs(saveDir)
    else:
        pass
    print("Results will be saved under directory %s" % (saveDir))

    # Create the name under which plot will be saved
    saveName = os.path.join(saveDir, plotName.replace("/", "_"))

    # For-loop: All save formats
    for i, ext in enumerate(saveFormats):
        # saveNameURL = saveName + ext
        # saveNameURL = aux.convertToURL(saveNameURL, opts.url)
        # Verbose(saveNameURL, False)
        plot.SaveAs(saveName + ext)
    return

if __name__ == "__main__":
    ROOT.gROOT.SetBatch(True)
    limitWorkDir = os.getcwd()
    odir = "GOFfiles/GOFPlots_{0}/"
    with open("{0}PVALS_{1}_{2}.csv".format(odir.format(args.tag),args.year,args.algo), "w") as pvalsFile:
        pvalsFile.write("MX,MY,PVAL\n")
        for signalRaw in open(limitWorkDir+"/"+args.samplelist, 'rb').readlines():
            if '#' in signalRaw: continue
            sig = signalRaw[:-1]
            masspoint = sig[15:]
            config = {
                "Dir": odir.format(args.tag),
                "fData": "GOF_{0}_{1}_{2}_DATA.root".format(args.year, sig, args.algo),
                "fToy": "GOF_{0}_{1}_{2}_TOYS.root".format(args.year, sig, args.algo),
                "PlotLabel": "{0}".format(masspoint),
                "year": "{0}".format(args.year),
                "pvalsFile": pvalsFile,
                "MX": masspoint.split("MX_")[1].split("_MY")[0],
                "MY": masspoint.split("_MY_")[1]
                }
            doPlots(config)

