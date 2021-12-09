from ROOT import TCanvas, THist
from ROOT import TFile, TNtuple, TH1F
from ROOT import gROOT, gBenchmark, gRandom, gSystem
from ROOT import gPad

def Draw1DHistosComparison(original, target, variables, original_weights, norm, outputDirectory, tag):
    c1 = TCanvas( 'c1', 'c1', 0., 0., 800, 600 )
    gPad.SetTickx(1)
    gPad.SetTicky(1)
    gPad.SetMargin(0.16,0.05,0.16,0.05)

