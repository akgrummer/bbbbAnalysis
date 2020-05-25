import ROOT
import argparse
ROOT.gROOT.SetBatch(True)
# import statistics
import math

def stupidPythonMean(valueList):
    sum = 0
    for value in valueList:
        sum += value
    return sum/len(valueList)


def stupidPythonStdDev(valueList):
    sum = 0
    sumSquare = 0
    for value in valueList:
        sum += value
        sumSquare += (value*value)
    meanOfSquares = sumSquare/len(valueList)
    mean = sum/len(valueList)
    return math.sqrt(meanOfSquares - mean*mean)


def GetLimit(fname):
    fIn = ROOT.TFile.Open(fname)
    print fname
    tIn = fIn.Get('limit')
    if tIn.GetEntries() != 5:
        print "*** WARNING: cannot parse file", fname, "because nentries != 5"
        raise RuntimeError('cannot parse file')
    vals = []
    for i in range(0, tIn.GetEntries()):
        tIn.GetEntry(i)
        qe = tIn.quantileExpected
        lim = tIn.limit
        vals.append((qe,lim))
    return vals

#Prepare fit graph
def PrepareFitGraph(injlist,fIn_proto):
    gr1 = ROOT.TGraphAsymmErrors()
    gr2 = ROOT.TGraphAsymmErrors()
    for inj in injlist:
        #Get the information
        fInname = fIn_proto.format(inj=inj)
        fIn = ROOT.TFile(fInname)
        tIn = fIn.Get('limit')
        ntoys = tIn.GetEntries()
        #Fill best fit measurements from toys
        vals = []
        i=0
        for i in range(ntoys):
            tIn.GetEntry(i)
            if tIn.quantileExpected==-1: 
                vals.append(tIn.r) 
        mean      = stupidPythonMean(vals)
        meanerror = stupidPythonStdDev(vals)/math.sqrt(i)
        stvd      = stupidPythonStdDev(vals)  
        #One with the stvd bar        
        gr1.SetPoint(gr1.GetN(), inj,mean)
        gr1.SetPointError(gr1.GetN()-1, 0, 0, stvd, stvd)  
        #One with the meanerror bar
        gr2.SetPoint(gr2.GetN(), inj,mean)
        gr2.SetPointError(gr2.GetN()-1, 0, 0, meanerror, meanerror)
    return gr1,gr2
#Prepare pull graph
def PreparePullGraph(injlist,fIn_proto):
    gr = ROOT.TGraphAsymmErrors()
    for inj in injlist:
        #Get the information
        fInname = fIn_proto.format(inj=inj)
        fIn = ROOT.TFile(fInname)
        tIn = fIn.Get('limit')
        ntoys = tIn.GetEntries()
        #Fill best fit measurements from toys
        vals = []
        for i in range(ntoys):
            tIn.GetEntry(i)
            if tIn.quantileExpected==-1: vals.append(tIn.r) 
        mean = stupidPythonMean(vals)
        stvd = stupidPythonStdDev(vals)
        pull = (mean-inj)/stvd 
        gr.SetPoint(gr.GetN(), inj, pull)
        gr.SetPointError(gr.GetN()-1, 0, 0, 1, 1)
    return gr
#Make fit plot
def MakeFitPlot(injlist,fIn_proto,fLimit,title,outputname):
    gr1,gr2 = PrepareFitGraph(injlist,fIn_proto)
    limit   = GetLimit(fLimit)  
    c1 = ROOT.TCanvas('c1', 'c1', 1000, 1000)
    p1 = ROOT.TPad("p_2", "p_2", 0, 0, 1, 1)
    ROOT.gStyle.SetEndErrorSize(6)
    p1.SetFillStyle(4000)
    p1.SetFrameLineWidth(3)
    p1.SetFrameFillColor(0)
    p1.SetTopMargin(0.10)
    p1.SetBottomMargin(0.10)
    p1.SetLeftMargin(0.15)
    p1.SetRightMargin(0.10) 
    p1.Draw()  
    p1.cd()
    gr1.SetMinimum(min(injlist)-(min(injlist)*10))
    gr1.SetMaximum(max(injlist)+(min(injlist)*10))
    gr1.SetTitle(';#mu_{inj};<#hat{#mu}>')
    gr1.SetMarkerColor(ROOT.kBlack)
    gr1.SetLineColor(ROOT.kBlack)
    gr1.SetMarkerSize(0.8)
    gr1.SetMarkerStyle(8)
    gr1.SetLineWidth(2)
    gr1.SetLineStyle(9)
    gr2.SetMarkerColor(ROOT.kBlack)
    gr2.SetLineColor(ROOT.kRed)
    gr2.SetLineWidth(5)
    gr2.SetMarkerSize(0.8)
    gr2.SetMarkerStyle(8)
    gr1.Draw('AP')
    ll = ROOT.TLine(min(injlist)-(min(injlist)/10),min(injlist)-(min(injlist)/10), max(injlist)+(min(injlist)/10), max(injlist)+(min(injlist)/10))
    ll.SetLineStyle(7)
    ll.SetLineColor(ROOT.kGray+1)
    ll.SetLineWidth(3)
    ll.Draw()
    ul = ROOT.TLine(limit[2][1],min(injlist)-(min(injlist)*10), limit[2][1], max(injlist)+(min(injlist)*5))
    ul.SetLineStyle(7)
    ul.SetLineColor(ROOT.kGreen+1)
    ul.SetLineWidth(3)
    ul.Draw()
    gr2.Draw('P')
    #Legend
    leg_0 = ROOT.TLegend(0.01,0.92,0.40,0.97,"%s"%(title))
    leg_0.SetNColumns(1)
    leg_0.SetBorderSize(0)
    leg_0.SetTextSize(0.035)
    leg_0.SetTextFont(42)
    leg_0.SetLineColor(1)
    leg_0.SetLineWidth(10)
    leg_0.SetFillColor(0)
    leg_0.SetFillStyle(0)
    leg_0.Draw() 
    leg_1 = ROOT.TLegend(0.20,0.75,0.60,0.89)
    leg_1.SetNColumns(1)
    leg_1.SetBorderSize(0)
    leg_1.SetTextSize(0.035)
    leg_1.SetTextFont(42)
    leg_1.SetLineColor(ROOT.kWhite)
    leg_1.SetFillStyle(1001)
    leg_1.SetFillColor(ROOT.kWhite)   
    leg_1.AddEntry(ll, "Expected", "l") 
    leg_1.AddEntry(gr2,"Fitted", "PE") 
    leg_1.AddEntry(gr1,"1 s.d. of #hat{#mu} distribution", "E") 
    leg_1.AddEntry(ul,"95% CL Median U.L.", "l")
    leg_1.Draw() 
    c1.SaveAs('%s.png'%outputname)
    c1.Print('%s.pdf'%outputname, 'pdf')
#Make fit plot
def MakePullPlot(injlist,fIn_proto,fLimit,title,outputname):
    gr = PreparePullGraph(injlist,fIn_proto)
    limit   = GetLimit(fLimit) 
    c1 = ROOT.TCanvas('c1', 'c1', 1000, 1000)
    ROOT.gStyle.SetEndErrorSize(8)
    p1 = ROOT.TPad("p_2", "p_2", 0, 0, 1, 1)
    p1.SetFillStyle(4000)
    p1.SetFrameLineWidth(3)
    p1.SetFrameFillColor(0)
    p1.SetTopMargin(0.10)
    p1.SetBottomMargin(0.10)
    p1.SetLeftMargin(0.15)
    p1.SetRightMargin(0.10)  
    p1.Draw()  
    p1.cd()
    gr.SetMarkerSize(2)
    gr.SetLineWidth(2)
    gr.SetLineStyle(9)
    gr.SetMarkerStyle(8)
    gr.SetMinimum(-2.5)
    gr.SetMaximum(2.5)    
    gr.SetMarkerColor(ROOT.kRed)
    gr.SetLineColor(ROOT.kBlack)
    gr.SetTitle(';#mu_{inj};Pull = ( <#hat{#mu}> - #mu_{inj} ) / #sigma_{<#hat{#mu}>}')
    gr.Draw('AP')
    ll = ROOT.TLine(min(injlist), 0, max(injlist), 0)
    ll.SetLineStyle(7)
    ll.SetLineColor(ROOT.kGray+1)
    ll.SetLineWidth(3)
    ll.Draw()
    ul = ROOT.TLine(limit[2][1],-2.5, limit[2][1], 2.5)
    ul.SetLineStyle(7)
    ul.SetLineColor(ROOT.kOrange+1)
    ul.SetLineWidth(3)
    ul.Draw()
    #Legend
    leg_0 = ROOT.TLegend(0.01,0.92,0.40,0.97,"%s"%(title))
    leg_0.SetNColumns(1)
    leg_0.SetBorderSize(0)
    leg_0.SetTextSize(0.035)
    leg_0.SetTextFont(42)
    leg_0.SetLineColor(1)
    leg_0.SetLineWidth(10)
    leg_0.SetFillColor(0)
    leg_0.SetFillStyle(0)
    leg_0.Draw() 
    leg_1 = ROOT.TLegend(0.20,0.79,0.60,0.89)
    leg_1.SetNColumns(1)
    leg_1.SetBorderSize(0)
    leg_1.SetTextSize(0.035)
    leg_1.SetTextFont(42)
    leg_1.SetLineColor(ROOT.kWhite)
    leg_1.SetFillStyle(1001)
    leg_1.SetFillColor(ROOT.kWhite) 
    leg_1.AddEntry(ll, "Expected", "l") 
    leg_1.AddEntry(gr, "Fitted", "pe") 
    leg_1.AddEntry(ul,"95% CL Median U.L.", "l")
    leg_1.Draw() 
    c1.SaveAs('%s.png'%outputname)
    c1.Print('%s.pdf'%outputname, 'pdf')

#Make fit plot
def MakeDoubleFitPlot(injlist,fIn1,fIn2,fLimit,title,outputname):
    gr1_1,gr2_1 = PrepareFitGraph(injlist,fIn1)
    gr1_2,gr2_2 = PrepareFitGraph(injlist,fIn2)
    limit   = GetLimit(fLimit)  
    c1 = ROOT.TCanvas('c1', 'c1', 1000, 1000)
    p1 = ROOT.TPad("p_2", "p_2", 0, 0, 1, 1)
    ROOT.gStyle.SetEndErrorSize(6)
    p1.SetFillStyle(4000)
    p1.SetFrameLineWidth(3)
    p1.SetFrameFillColor(0)
    p1.SetTopMargin(0.10)
    p1.SetBottomMargin(0.10)
    p1.SetLeftMargin(0.15)
    p1.SetRightMargin(0.10) 
    p1.Draw()  
    p1.cd()
    gr1_1.SetMinimum(min(injlist)-(min(injlist)*5))
    gr1_1.SetMaximum(max(injlist)+(min(injlist)*10))
    gr1_1.SetTitle(';#mu_{inj};<#hat{#mu}>')
    gr1_1.SetMarkerColor(ROOT.kBlack)
    gr1_1.SetLineColor(ROOT.kBlack)
    gr1_1.SetMarkerSize(0.8)
    gr1_1.SetMarkerStyle(8)
    gr1_1.SetLineWidth(2)
    gr2_1.SetMarkerColor(ROOT.kBlack)
    gr2_1.SetLineColor(ROOT.kRed)
    gr2_1.SetLineWidth(5)
    gr2_1.SetMarkerSize(0.8)
    gr2_1.SetMarkerStyle(8)
    gr1_2.SetMarkerColor(ROOT.kBlue)
    gr1_2.SetLineColor(ROOT.kBlue)
    gr1_2.SetMarkerSize(0.8)
    gr1_2.SetMarkerStyle(8)
    gr1_2.SetLineWidth(2)
    gr2_2.SetMarkerColor(ROOT.kBlue)
    gr2_2.SetLineColor(ROOT.kGreen+1)
    gr2_2.SetLineWidth(5)
    gr2_2.SetMarkerSize(0.8)
    gr2_2.SetMarkerStyle(8)
    gr1_1.Draw('AP')
    ll = ROOT.TLine(min(injlist)-(min(injlist)/10),min(injlist)-(min(injlist)/10), max(injlist)+(min(injlist)/10), max(injlist)+(min(injlist)/10))
    ll.SetLineStyle(7)
    ll.SetLineColor(ROOT.kGray+1)
    ll.SetLineWidth(3)
    ll.Draw()
    ul = ROOT.TLine(limit[2][1],min(injlist)-(min(injlist)*5), limit[2][1], max(injlist)+(min(injlist)*10))
    ul.SetLineStyle(7)
    ul.SetLineColor(ROOT.kOrange+1)
    ul.SetLineWidth(3)
    ul.Draw()
    gr2_1.Draw('P')
    gr1_2.Draw('P')
    gr2_2.Draw('P')
    #Legend
    leg_0 = ROOT.TLegend(0.01,0.92,0.40,0.97,"%s"%(title))
    leg_0.SetNColumns(1)
    leg_0.SetBorderSize(0)
    leg_0.SetTextSize(0.035)
    leg_0.SetTextFont(42)
    leg_0.SetLineColor(1)
    leg_0.SetLineWidth(10)
    leg_0.SetFillColor(0)
    leg_0.SetFillStyle(0)
    leg_0.Draw() 
    leg_1 = ROOT.TLegend(0.17,0.65,0.85,0.89)
    leg_1.SetNColumns(1)
    leg_1.SetBorderSize(0)
    leg_1.SetTextSize(0.030)
    leg_1.SetTextFont(42)
    leg_1.SetLineColor(ROOT.kWhite)
    leg_1.SetFillStyle(1001)
    leg_1.SetFillColor(ROOT.kWhite)   
    leg_1.AddEntry(ll, "Expected", "l") 
    leg_1.AddEntry(gr2_1,"Fit (#mu#upoints + b_{true})","PE") 
    leg_1.AddEntry(gr1_1,"1 s.d. of #hat{#mu} distribution (#mu#upoints + b_{true})", "E") 
    leg_1.AddEntry(gr2_2,"Fit (#mu#upoints + #mu_{inj}#upointb_{sig} + b_{true})", "PE") 
    leg_1.AddEntry(gr1_2,"1 s.d. of #hat{#mu} distribution (#mu#upoints + #mu_{inj}#upointb_{sig} + b_{true})", "E") 
    leg_1.AddEntry(ul,"95% CL Median U.L.", "l")
    leg_1.Draw() 
    c1.SaveAs('%s.png'%outputname)
    c1.Print('%s.pdf'%outputname, 'pdf')

#Make pull plot
def MakeDoublePullPlot(injlist,fIn1,fIn2,fLimit,title,outputname):
    gr1 = PreparePullGraph(injlist,fIn1)
    gr2= PreparePullGraph(injlist,fIn2)
    limit   = GetLimit(fLimit)  
    c1 = ROOT.TCanvas('c1', 'c1', 1000, 1000)
    p1 = ROOT.TPad("p_2", "p_2", 0, 0, 1, 1)
    ROOT.gStyle.SetEndErrorSize(8)
    p1.SetFillStyle(4000)
    p1.SetFrameLineWidth(3)
    p1.SetFrameFillColor(0)
    p1.SetTopMargin(0.10)
    p1.SetBottomMargin(0.10)
    p1.SetLeftMargin(0.15)
    p1.SetRightMargin(0.10) 
    p1.Draw()  
    p1.cd()
    gr1.SetMinimum(-2.5)
    gr1.SetMaximum(2.5)
    gr1.SetTitle(';#mu_{inj};Pull = ( <#hat{#mu}> - #mu_{inj} ) / #sigma_{#hat{#mu} }')
    gr1.SetMarkerColor(ROOT.kRed)
    gr1.SetLineColor(ROOT.kBlack)
    gr1.SetMarkerSize(2)
    gr1.SetMarkerStyle(8)
    gr1.SetLineWidth(2)
    gr1.SetLineStyle(9)
    gr2.SetMarkerColor(ROOT.kGreen+1)
    gr2.SetLineColor(ROOT.kBlue)
    gr2.SetLineWidth(2)
    gr2.SetMarkerSize(2)
    gr2.SetMarkerStyle(8)
    gr2.SetLineStyle(9)
    gr1.Draw('AP')
    ll = ROOT.TLine(min(injlist), 0, max(injlist), 0)
    ll.SetLineStyle(7)
    ll.SetLineColor(ROOT.kGray+1)
    ll.SetLineWidth(3)
    ll.Draw()
    ul = ROOT.TLine(limit[2][1],-2.5, limit[2][1], 2.5)
    ul.SetLineStyle(7)
    ul.SetLineColor(ROOT.kOrange+1)
    ul.SetLineWidth(3)
    ul.Draw()
    gr2.Draw('P')
    #Legend
    leg_0 = ROOT.TLegend(0.01,0.92,0.40,0.97,"%s"%(title))
    leg_0.SetNColumns(1)
    leg_0.SetBorderSize(0)
    leg_0.SetTextSize(0.035)
    leg_0.SetTextFont(42)
    leg_0.SetLineColor(1)
    leg_0.SetLineWidth(10)
    leg_0.SetFillColor(0)
    leg_0.SetFillStyle(0)
    leg_0.Draw() 
    leg_1 = ROOT.TLegend(0.17,0.69,0.85,0.89)
    leg_1.SetNColumns(1)
    leg_1.SetBorderSize(0)
    leg_1.SetTextSize(0.035)
    leg_1.SetTextFont(42)
    leg_1.SetLineColor(ROOT.kWhite)
    leg_1.SetFillStyle(1001)
    leg_1.SetFillColor(ROOT.kWhite)   
    leg_1.AddEntry(ll, "Expected", "l") 
    leg_1.AddEntry(gr1,"Fit (#mu#upoints + b_{true})","PE") 
    leg_1.AddEntry(gr2,"Fit (#mu#upoints + #mu_{inj}#upointb_{sig} + b_{true})", "PE") 
    leg_1.AddEntry(ul,"95% CL Median U.L.", "l")
    leg_1.Draw() 
    c1.SaveAs('%s.png'%outputname)
    c1.Print('%s.pdf'%outputname, 'pdf')


#############COMMAND CODE IS BELOW ######################

###########OPTIONS
parser = argparse.ArgumentParser(description='Command line parser of skim options')
parser.add_argument('--study',  dest='study',      help='Name of model folder',   required = True)
parser.add_argument('--selsignal', dest='selsignal',  help='Name of the selection and signal',   required = True)
parser.add_argument('--dataset', dest='dataset',  help='Dataset',   required = True)
parser.add_argument('--injectionList',    dest='injectionList',      help='injection List', nargs='+',        required=True)
args = parser.parse_args()
studyname       = args.study
selsignalname   = args.selsignal
datasetname     = args.dataset

##Run everything
injlistString   = args.injectionList
injlist = []
for value in injlistString:
    injlist.append(float(value))
# injlist  = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]  
fLimit   = 'higgsCombineTest.AsymptoticLimits.mH120.root'
#First let's plot the best-fit without using the signal-induced background 
fIn1            = 'higgsCombine_inj_{inj}_myscale_0_fitresults.MultiDimFit.mH120.123456.root'
fitoutputname1  = '%s_%s_bestfit_nosigbkg'%(studyname,selsignalname)
pulloutputname1 = '%s_%s_pull_nosigbkg'%(studyname,selsignalname)
MakeFitPlot(injlist,fIn1,fLimit,"Fit w/o signal-induced bkg: %s"%selsignalname,fitoutputname1)
MakePullPlot(injlist,fIn1,fLimit,"Fit w/o signal-induced bkg: %s"%selsignalname,pulloutputname1)

#Second, let's plot the best-fit without using the signal-induced background 
fIn2            = 'higgsCombine_inj_{inj}_fitresults.MultiDimFit.mH120.123456.root'
fitoutputname2  = '%s_%s_bestfit'%(studyname,selsignalname)
pulloutputname2 = '%s_%s_pull'%(studyname,selsignalname)
MakeFitPlot(injlist,fIn2,fLimit,"Fit w/ signal-induced bkg: %s"%selsignalname,fitoutputname2)
MakePullPlot(injlist,fIn2,fLimit,"Fit w/o signal-induced bkg: %s"%selsignalname,pulloutputname2)

#Draw them together
fitoutputname   = '%s_%s_bestfit_both'%(studyname,selsignalname)
pulloutputname  = '%s_%s_pull_both'%(studyname,selsignalname)
MakeDoubleFitPlot(injlist,fIn1,fIn2,fLimit,"Case %s: %s"%(datasetname,selsignalname),fitoutputname)
MakeDoublePullPlot(injlist,fIn1,fIn2,fLimit,"Case %s: %s"%(datasetname,selsignalname),pulloutputname)