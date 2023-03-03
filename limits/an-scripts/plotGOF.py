#!/usr/bin/env python
'''
DESCRIPTION:
Plots goodness-of-fit plots by looking inside the current working directory
to find GOF_FitAlgo-<fitAlgo>_Created<DDMonthYear> directories. These are created by running the doGOF.csh script first.

The following algorithms are supported:

saturated: Compute a goodness-of-fit measure for binned fits based on the saturated model method, as prescribed by the StatisticsCommittee (note). 
This quantity is similar to a chi-square, but can be computed for an arbitrary combination of binned channels with arbitrary constraints.

Kolmogorov-Smirnov (KS): Compute a goodness-of-fit measure for binned fits using the Kolmogorov-Smirnov test. 
It is based on the highest difference between the cumulative distribution function and the empirical distribution function of any bin.

Anderson-Darling (AD): Compute a goodness-of-fit measure for binned fits using the Anderson-Darling test. 
It is based on the integral of the difference between the cumulative distribution function and the empirical distribution function over all bins. 
It also gives the tail ends of the distribution a higher weighting.


PREREQUISITES:
Run the doGOF.csh to produce the GoF ROOT files. These are used as input for this script


USAGE:
cd <datacards_dir>
python ../../../plotGOF.py [opts]


EXAMPLES:
cd LimitsMore_Created30Jul2021_v1/datacards_multicategory_LTau_Created30Jul2021
python plotGOF.py --analysisType HToHW --mass 300


LAST USED:
python ../../plotGOF.py --analysisType HToHW --mass 300,400,500,700


LINKS:
http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/part3/commonstatsmethods.html#goodness-of-fit-tests
https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideHiggsAnalysisCombinedLimit#Goodness_of_fit_tests

'''

#================================================================================================ 
# Imports
#================================================================================================ 
import ROOT
import sys
import os
import glob
import shutil
import getpass
from subprocess import call, check_output
from optparse import OptionParser

import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles


#================================================================================================ 
# Shell Types 
#================================================================================================ 
ss = ShellStyles.SuccessStyle()
ns = ShellStyles.NormalStyle()
ts = ShellStyles.NoteStyle()
hs = ShellStyles.HighlightAltStyle()
qs = ShellStyles.AltStyle()
ls = ShellStyles.HighlightStyle()
es = ShellStyles.ErrorStyle()
cs = ShellStyles.CaptionStyle()
ws = ShellStyles.WarningStyle()

#================================================================================================ 
# Custom colours (https://www.color-hex.com)
#================================================================================================ 
kDarkBlue = ROOT.TColor.GetColor("#001ee2")
kBlue     = ROOT.TColor.GetColor("#8097cc")
kLightBlue= ROOT.TColor.GetColor("#a6b6db")
kRed      = ROOT.TColor.GetColor("#e23222")
kLightRed = ROOT.TColor.GetColor("#FCD0D1")

#================================================================================================ 
# Function definition
#================================================================================================ 
def Verbose(msg, printHeader=False):
    '''
    Calls Print() only if verbose options is set to true
    '''
    if not opts.verbose:
        return
    Print(msg, printHeader)
    return

def Print(msg, printHeader=True):
    '''
    Simple print function. If verbose option is enabled prints, otherwise does nothing.
    '''
    fName = __file__.split("/")[-1]
    if printHeader:
        print "=== ", fName
    print "\t", msg
    return


def CleanFiles(opts):
    if not opts.clean:
        return
        
    dirName  = "lxbatch"
    fullPath = os.path.join(os.getcwd(), dirName)
    if not os.path.exists("%s" % (fullPath)):
        os.mkdir(fullPath)
        
    bMatchJob  = False
    bMatchRoot = False
    for fname in os.listdir('.'):
        if fname.startswith('job_'):
            bMatchJob = True
            break
        if fname.startswith('higgsCombineToys') and fname.endswith(".root"):
            bMatchRoot = True
            break

    if bMatchJob:
        Print("Cleaning auxiliary \"job\" files (lxbatch job) by moving them to a dedicated directory \"%s\"" % (dirName), True)
        srcFiles = "job_*.*"
        call("mv %s %s" % (srcFiles, fullPath), shell=True)

    if bMatchRoot:
        Print("Cleaning auxiliary \"ROOT\" files (lxbatch job) by moving them to a dedicated directory \"%s\"" % (dirName), True)
        call("mv %s %s" % (opts.inputToyFiles, fullPath), shell=True )
    return


def doPlots(i, opts):

    msg = "Processing %s%s%s algorithm" % (ts, opts.algorithm, ns )
    Print(msg, True)

    # Settings
    aDict = {}
    aDict["HToToTauNu"] = "H^{+}#rightarrow#tau_{h}#nu fully hadronic"
    aDict["HToTB"]      = "H^{+}#rightarrow tb fully hadronic"
    aDict["HToHW"]      = "H^{#pm} #rightarrow H W^{#pm}, H#rightarrow #tau^{+}#tau^{-}"

    # Hadd ROOT files
    rootFiles = glob.glob1(opts.inputDir, "higgsCombineToys*.root")
    Print("Found %d ROOT files" % (len(rootFiles)), True)
    
    Verbose("Attempting to merge all toy ROOT files", True)
    if len(rootFiles) > 0:
        if os.path.isfile(opts.outputfile):
            os.remove(opts.outputfile)
        Verbose("Merging '%s' ROOT files into '%s;" % (opts.inputToyFiles, opts.inputToyFiles), False)
        call("hadd -k %s %s > mergeROOT.txt" % (opts.outputfile, opts.inputToyFiles), shell=True)  # -k option to skip problematic files
    else:
        msg = "%sFound %d toy ROOT files to merge%s" % (ts, len(rootFiles), ns )
        Print(msg, True)
        sys.exit()
    
    # Clean auxiliary jobs files?
    CleanFiles(opts)
        
    # Perform GoF calculations
    if not os.path.isfile(opts.outputfile):
        raise Exception("The output ROOT file \"%s\" does not exist!" % (opts.outputfile) )
    else:
        Print("Opening merged ROOT file \"%s\" to read results (toys)" % (opts.outputfile), True)

    if not os.path.isfile(opts.inputDataFile):
        raise Exception("The output ROOT file '%s' does not exist!" % (opts.inputDataFile) )
    else:
        Print("Opening ROOT file '%s' to read results (data)" % (opts.inputDataFile), True)
    fToys = ROOT.TFile(opts.outputfile)
    fData = ROOT.TFile(opts.inputDataFile)
    tToys = fToys.Get("limit")
    tData = fData.Get("limit")
    nToys = tToys.GetEntries()

    if opts.verbose:
        aux.PrintTH1Info(tData)

    if opts.verbose:
        tData.Print()

    # Store the goodness-of-fit value observed in data
    Verbose("NData = %.1f, NToys = %.1f" % (tData.GetEntries(), tToys.GetEntries()), False)
    tData.GetEntry(0)
    GoF_DATA = tData.limit
    Verbose(GoF_DATA, True)

    # Setting (Toys)
    nToysTotal = 0
    pValueCum  = 0
    toys       = []
    minToy     = +99999999
    maxToy     = -99999999

    # For-loop: All toys
    for i in range(0, tToys.GetEntries()):
        tToys.GetEntry(i)

        # Toys counter
        nToysTotal += tToys.limit
        toys.append(tToys.limit)
        
        # Accumulate p-Value if GoF_toy > GoF_data
        if tToys.limit > GoF_DATA: 
            Verbose("GoF (toy) = %.3f, GoF (data) = %.3f, p-Value += %d (%d)" % (tToys.limit, GoF_DATA, tToys.limit, pValueCum), i==1)
            pValueCum += tToys.limit
        
    # Finalise p-value calculation by dividing by number of toys total
    pval = pValueCum / nToysTotal
    msg = "%sp-Value = %.3f%s (%.2f/%.2f)" % (ss, pval, ns, pValueCum, nToysTotal)
    Print(msg, False)

    # xMin will be automatically re-adjusted 
    xMin  = {}
    xMin["saturated"] = 0
    xMin["KS"] = 0.0
    xMin["AD"] = 0.0

    # xMax will be automatically re-adjusted 
    xMax  = {}
    xMax["saturated"] = 2000
    xMax["KS"] = 2000.0
    xMax["AD"] = 200.00
    binWidth = {}
    binWidth["saturated"] = 5 #10
    binWidth["KS"] = 0.002 #0.002 #0.004
    binWidth["AD"] = 0.2   # 0.10 0.25 #0.5
    nBins = (xMax[opts.algorithm]-xMin[opts.algorithm])/binWidth[opts.algorithm]

    # Create histogram to plot the test statistic for toys and data [ TH1D::TH1D(const char* name, const char* title, int nbinsx, double xlow, double xup) ]
    Verbose("algo = %s, nBins = %d, xMin= %s, xMax = %s" % (opts.algorithm, nBins, xMin[opts.algorithm], xMax[opts.algorithm]), True)
    Verbose("algo = %s, nBins = %s, xMin= %s, xMax = %s" % (type(opts.algorithm), type(nBins), type(xMin[opts.algorithm]), type(xMax[opts.algorithm])), False)
    hist = ROOT.TH1D("GoF-%s" % (opts.algorithm), "", int(nBins), xMin[opts.algorithm], xMax[opts.algorithm])

    # For-loop: Toys
    for k in toys: 
        hist.Fill(k)

    # Set range for x-axis and y-axis range
    xMin  = hist.GetBinLowEdge(hist.FindFirstBinAbove(0.0))*0.25 # hist.GetBinCenter(hist.FindFirstBinAbove(0.0))*0.8
    xMax  = hist.GetBinLowEdge(hist.FindLastBinAbove(0.0))*1.75  # hist.GetBinCenter(hist.FindLastBinAbove(0.0))*1.2
    yMin  = 0.0
    yMax  = hist.GetMaximum()*1.05
    Verbose("xMin = %s, xMax = %s, yMin = %s, yMax = %s, binWidth = %s, nBins = %s" % (xMin, xMax, yMin, yMax, binWidth[opts.algorithm], nBins), True)

    # Customise canvas & histogram
    c  = ROOT.TCanvas("canvas", "canvas")
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
    hist.SetLineColor(kRed)
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
    left.SetTextSize(22)
    left.SetTextAlign(11)
    #left.DrawLatex(GoF_DATA*1.01, (hist.GetMaximum())*0.03, "#color[4]{data}")
    #left.DrawLatex(GoF_DATA*1.02, (hist.GetMaximum())*0.03, "#color[4]{t_{0}}")
    if GoF_DATA < 1.0:
        left.DrawLatex(tZeroX, tZeroY*1.1, "#color[4]{t_{0}= %.2f}" % (GoF_DATA))
    elif GoF_DATA < 10.0:
        left.DrawLatex(tZeroX, tZeroY*1.1, "#color[4]{t_{0}= %.1f}" % (GoF_DATA))
    else:
        left.DrawLatex(tZeroX, tZeroY*1.1, "#color[4]{t_{0}= %.0f}" % (GoF_DATA))

    # Analysis text
    anaText = ROOT.TLatex()
    anaText.SetNDC()
    anaText.SetTextFont(43)
    anaText.SetTextSize(22)
    anaText.SetTextAlign(31) 
    if 0:
        anaText.DrawLatex(0.92-0.6, 0.86, aDict[opts.analysisType])
    else:
        #anaText.DrawLatex(0.92, 0.86, "\"%s\" GoF test" % (opts.algorithm) )
        anaText.DrawLatex(0.92, 0.86, "%s model" % (opts.algorithm) )

    # Add text with details of the GoF test (nToys, p-value, signal mass)
    pvalText = ROOT.TLatex()
    pvalText.SetNDC()
    pvalText.SetTextFont(43)
    pvalText.SetTextSize(22)
    pvalText.SetTextAlign(31) #11
    pvalText.DrawLatex(0.92, 0.80, "toys = %d" % nToys)
    #pvalText.DrawLatex(0.92, 0.74, "p-value = %.2f" % pval)
    pvalText.DrawLatex(0.92, 0.74, "p-value = %.3f" % pval)
    pvalText.DrawLatex(0.92, 0.68, "m_{H^{+}} = %s GeV" % opts.mass)

    # Print some info
    Verbose("Toys = %.0f" % (nToys), True)
    Verbose("nToysTotal = %.0f" % (nToysTotal), True)
    Verbose("p-value = %.2f" % (pval), False)

    # Add default texts
    histograms.addStandardTexts(lumi=opts.lumi, sqrts="13 TeV", addCmsText=True, cmsTextPosition=None, cmsExtraTextPosition=None, cmsText="CMS", cmsExtraText="Internal   ")

    # Save the plot (not needed - drawPlot saves the canvas already)
    saveName = "GoF_m%s_%s" % (opts.mass, opts.algorithm)
    SavePlot(c, saveName, opts.saveDir, saveFormats = [".C", ".png", ".pdf"])

    return

def SavePlot(plot, plotName, saveDir, saveFormats = [".C", ".png", ".pdf"]):
    Verbose("Saving canvas in %s formats: %s" % (len(saveFormats), ", ".join(saveFormats) ) )

     # Check that path exists
    if not os.path.exists(saveDir):
        Verbose("Creating directory \"%s\"" % (saveDir), True)
        os.makedirs(saveDir)
    else:
        pass
    Print("Results will be saved under directory %s" % (ss + saveDir + ns), True)
        
    # Create the name under which plot will be saved
    saveName = os.path.join(saveDir, plotName.replace("/", "_"))

    # For-loop: All save formats
    for i, ext in enumerate(saveFormats):
        saveNameURL = saveName + ext
        saveNameURL = aux.convertToURL(saveNameURL, opts.url)
        Verbose(saveNameURL, False)
        plot.SaveAs(saveName + ext)
    return


def main(opts):

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    ROOT.gErrorIgnoreLevel = ROOT.kFatal # [Options: Print, kInfo, kWarning, kError, kBreak, kSysError, kFatal]
    ROOT.gROOT.SetBatch()
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)
    #ROOT.gStyle.SetNdivisions(5, "X")
    ROOT.gStyle.SetNdivisions(6, "X")

    myDirs = []

    # For-loop: All GoF directories (generated by doGOF.csh script)
    for d in os.listdir('.'):
        if not os.path.isdir(d):
            continue    
        if "GOF_" in d: # crude but works
            myDirs.append(d)

    if len(myDirs) < 1:
        raise Exception("No goodness-of-fit directories found. Did your run the doGOF.csh script to create them?" )
    else:
        Verbose("Found %d GoF directories: %s" % (len(myDirs), ", ".join(myDirs)), True)


    myAlgos = []
    allowedAlgos = ["saturated", "KS", "AD"] # KS = Kolmogorov-Smirnov, AD = Anderson-Darling

    # For-loop: All GoF directories
    for i, d in enumerate(myDirs, 1):
        Print("%d/%d) %s" % (i, len(myDirs), d), i==1)
        algo = d.split("-")[1].split("_")[0]
        if algo not in allowedAlgos:
            raise Exception("The algorithm \"%s\" is invalid. Expected one of the following: %s" % (algo, ", ".join(allowedAlgos)))

        Verbose("Found %d GoF algorithm result(s): %s" % (len(myDirs), ", ".join(myAlgos)), True)

        # Definitions
        opts.inputDir   = d
        opts.algorithm  = algo
        opts.inputToyFiles  = "%s/higgsCombineToys*.GoodnessOfFit.mH%s.*.root" % (opts.inputDir, opts.mass)
        opts.inputDataFile  = "%s/higgsCombineData.GoodnessOfFit.mH120.root" % (opts.inputDir) # FIXME: why mH120? Where can I fix that? (i.e. remove completely)
        #opts.inputDataFile  = "%s/higgsCombineData.GoodnessOfFit.mH%s.root" % (opts.inputDir, opts.mass)
        opts.outputfile     = "%s/GoF_%s_mH%s.root" % (opts.inputDir, algo, opts.mass)
        
        # Update integrated luminosity based on directory name
        doPlots(i, opts)

    Verbose("All plots saved under directory %s" % (ts + aux.convertToURL(opts.saveDir, opts.url) + ns), True)

    return

#================================================================================================ 
# Function definition
#================================================================================================ 
if __name__ == "__main__":

    # Default Values
    HELP          = False
    #SAVEDIR         = "/afs/cern.ch/user/%s/%s/public/html/FitDiagnostics" % (getpass.getuser()[0], getpass.getuser())
    SAVEDIR       = "/publicweb/%s/%s/FitDiagnostics/%s" % (getpass.getuser()[0], getpass.getuser(), os.path.basename(os.getcwd()))
    VERBOSE       = False
    ANALYSISTYPE  = "HToTauNu"
    MASS          = 300
    INPUTTOYFILES = None
    INPUTDATAFILE = None
    OUTPUTFILE    = None
    URL           = False
    LUMI          = 138000 #pb-1
    SAVEFORMATS   = "pdf,png,C"
    ALGORITHM     = "saturated"
    CLEAN         = False

    # Object for selecting data eras, search modes, and optimization modes
    parser = OptionParser(usage="Usage: %prog [options]", add_help_option=False, conflict_handler="resolve")

    parser.add_option("-h", "--help", dest="help", action="store_true", default=HELP, 
                      help="Show this help message and exit [default: %s]" % HELP)

    parser.add_option("--saveDir", dest="saveDir", type="string", default=SAVEDIR,
                      help="Directory where all plots will be saved [default: %s]" % SAVEDIR)

    parser.add_option("--url", dest="url", action="store_true", default=URL,
                      help="Don't print the actual save path the plots are saved, but print the URL instead [default: %s]" % URL)

    parser.add_option("--clean", dest="clean", action="store_true", default=CLEAN, 
                      help="Move all GoF.sh output (lxbatch) to a dedicated directory [default: %s]" % CLEAN)

    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE,
                      help="Print more information [default: %s]" % (VERBOSE) )

    parser.add_option("--analysisType", dest="analysisType", default=ANALYSISTYPE,
                      help="Flag to indicate the analysis type (e.g. %s [default: %s]" % (", ".join(aux.getAnalysisAliasList()), ANALYSISTYPE))

    parser.add_option("--inputToyFiles", dest="inputToyFiles", default=INPUTTOYFILES,
                      help="Name of ROOT file to use as input for toy test statistic(of hadd command) [default: %s]" % (INPUTTOYFILES) )

    parser.add_option("--inputDataFile", dest="inputDataFile", default=INPUTDATAFILE,
                      help="Name of ROOT file to use as input for data test statistic [default: %s]" % (INPUTDATAFILE) )

    parser.add_option("--outputfile", dest="outputfile", default=OUTPUTFILE,
                      help="Name of ROOT file to use as output (of hadd command)  [default: %s]" % (OUTPUTFILE) )

    parser.add_option("-m", "--mass", dest="mass", default=MASS,
                      help="Mass point to use [default: %s]" % (MASS) )

    parser.add_option("--lumi", dest="lumi", default=LUMI,
                      help="Integrated luminosity [default: %s]" % (LUMI) )

    parser.add_option("-s", "--saveFormats", dest="saveFormats", default = SAVEFORMATS,
                      help="Save formats for all plots [default: %s]" % SAVEFORMATS)

    #parser.add_option("-a", "--algorithm", dest="algorithm", default=ALGORITHM,
    #                  help="Name of algorithm used in the goodness-of-fit test [default: %s]" % (ALGORITHM) )


    (opts, args) = parser.parse_args()

    # All the formats for saving plots
    if "," in opts.saveFormats:
        opts.saveFormats = opts.saveFormats.replace(" ", "").split(",")
    else:
        opts.saveFormats = [opts.saveFormats]
    opts.saveFormats = ["." + s for s in opts.saveFormats]

    # All the formats for saving plots
    if "," in opts.mass:
        opts.massList = opts.mass.split(",")
    else:
        opts.massList = [opts.mass]

    # Sanity check
    opts.massList = [m for m in opts.massList if m in ["300", "400", "500", "700"]]
    if len(opts.massList) < 1:
        msg = "No supported mass points found in option provided (--mass %s)" % (opts.mass)
        raise Exception(es + msg + ns)


    if opts.saveDir == None:
        opts.saveDir = aux.getSaveDirPath(os.path.basename(os.getcwd()), prefix="", postfix="Test")

        
    # Automatically detect analysis?
    aux.ensureAnalysisTypeIsValid(opts.analysisType)
    msg = "Analysis type %s" % (hs + opts.analysisType + ns)
    Print(msg, True)


    Verbose("Using ROOT files '%s' ('%s') as input for toys (data)" % (opts.inputToyFiles, opts.inputDataFile), True)

    for m in opts.massList:
        opts.mass = m
        main(opts)
