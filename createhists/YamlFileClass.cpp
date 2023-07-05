#include "YamlFileClass.h"
using namespace std;

YamlFile::YamlFile(TString configFile)
{
    //std::cout << "yaml construnctor called" << std::endl;
    node = YAML::LoadFile( configFile.Data() );
}

//Destructor
YamlFile::~YamlFile(){
    //std::cout << "yaml destructor called" << std::endl;
}

vector<string> YamlFile::getFiles () {
    vector<string> files = node["filesIn"]["files"].as<vector<string>>();
    return files;
}

