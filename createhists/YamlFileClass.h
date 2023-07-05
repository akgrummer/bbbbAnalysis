#ifndef YAMLFILECLASS_H
#define YAMLFILECLASS_H
#include <iostream>
#include <range/v3/all.hpp>
#include <yaml-cpp/yaml.h>

#include <TStyle.h>
#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>
#include <TChain.h>
#include <TCut.h>
#include <TString.h>
#include <TH1F.h>
#include <TH2F.h>
#include <TF1.h>
#include <TLatex.h>
#include <TCanvas.h>
#include <TPad.h>
#include <Rtypes.h>
#include <RtypesCore.h>
#include <TLegend.h>
#include <TH1.h>

class YamlFile{
    public:
    YamlFile( TString );
    ~YamlFile();
    YAML::Node node;

    std::vector<std::string> getFiles ();
};
#endif //YAMLFILECLASS_H

