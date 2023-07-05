from ROOT import TFile, TCanvas, TPad, TLegend

ifile = TFile.Open("2016/root/gofs__2016__MX700__MY60.root")
for obj in ifile.GetListOfKeys():
    c1 = ifile.Get(obj.GetName())
    print(obj.GetName())

