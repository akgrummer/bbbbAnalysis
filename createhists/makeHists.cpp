#include "HistFileClass.h"
#include "YamlFileClass.h"
#include "makeHists.h"

int main(int argc, char **argv ){

    YamlFile cfile("config.yaml");
    idir = cfile.node["filesIn"]["dir"].as<std::string>();
    ofilename = (TString) cfile.node["ofile"].as<std::string>();
    // YamlFile cfile2("config2.yaml");
    //ifiles = cfile.getFiles();
    auto start = chrono::high_resolution_clock::now();
    HistFile myfile( itreename, idir, cfile.getFiles(), odir, ofilename );
    auto stop = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::milliseconds>(stop - start);
    cout << "Time taken loading files: "
        << duration.count() << " ms" << endl;


    start = chrono::high_resolution_clock::now();
    myfile.SetCutData(VRB, "VR");

    myfile.SetBranch("H2_m");
    myfile.SetBins(binEdges_H2_m);

    for(const auto &train : trainings) {
        myfile.SetWeightData(weight+train, train);
        myfile.SaveHist("mY");
    }
    myfile.SetWeightData(Form("%s%s+%s%s", weight.Data(), "mean", weight.Data(), "std"), "stdup");
    myfile.SaveHist("mY");

    myfile.SetWeightData(Form("%s%s-%s%s", weight.Data(), "mean", weight.Data(), "std"), "stddown");
    myfile.SaveHist("mY");

    for(int i = 0; i<10; i++){
        myfile.SetWeightData(  weight + Form("%d",i), Form("%d",i));
            myfile.SaveHist("mY");
    }
    std::cout << " -- event after cut(s) for mY: " << myfile.nselected << std::endl;

    myfile.SetBranch("HH_kinFit_m");
    myfile.SetBins(binEdges_HH_kinFit_m);

    for(const auto &train : trainings) {
        myfile.SetWeightData(weight + train, train);
        myfile.SaveHist("mX");
    }
    for(int i = 0; i<10; i++){
        myfile.SetWeightData( weight + Form("%d",i), Form("%d",i));
        myfile.SaveHist("mX");
    }
    std::cout << " -- events after cut(s) for mX: " << myfile.nselected << std::endl;
    stop = chrono::high_resolution_clock::now();
    auto duration2 = chrono::duration_cast<chrono::seconds>(stop - start);
    cout << "Time taken filling and writing hists files: "
        << duration2.count() << " s" << endl;

    return 0;
}
