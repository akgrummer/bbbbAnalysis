from  ConfigParser import *
import ast

class ConfigurationReader:
    def __init__(self, configFileName): 
        ###########Read Config file
        print "[INFO] Reading skim configuration file from file", configFileName
        cfgparser = ConfigParser()
        cfgparser.read('%s'%configFileName)
        ##########Get skim variables
        print "[INFO] Getting configuration parameters . . ."
        self.backgroundWeightName         = ast.literal_eval(cfgparser.get("configuration","backgroundWeightName"))
        print "    -The backgroundWeightName:"
        print "      *",self.backgroundWeightName[0]
        self.minpt                        = ast.literal_eval(cfgparser.get("configuration","minbjetpt"))
        print "    -The min b-jet pt:"
        print "      *",self.minpt 
        self.minRegressedPt               = ast.literal_eval(cfgparser.get("configuration","minbjetregressedpt"))
        print "    -The min b-jet regressed pt"
        print "      *",self.minRegressedPt 
        self.minEta                       = ast.literal_eval(cfgparser.get("configuration","minbjeteta"))
        print "    -The min b-jet eta"
        print "      *",self.minEta 
        self.maxEta                       = ast.literal_eval(cfgparser.get("configuration","maxbjeteta"))
        print "    -The max b-jet eta"
        print "      *",self.maxEta 
        self.preSelection                 = ast.literal_eval(cfgparser.get("configuration","preSelection"))
        print "    -The preSelection:"
        print "      *",self.preSelection
        self.controlRegionSelection       = ast.literal_eval(cfgparser.get("configuration","controlRegionSelection"))
        print "    -The controlRegionSelection:"
        print "      *",self.controlRegionSelection

        self.controlRegionSelectionRightSide       = ast.literal_eval(cfgparser.get("configuration","controlRegionSelectionRightSide"))
        print "    -The controlRegionSelectionRightSide:"
        print "      *",self.controlRegionSelectionRightSide

        self.controlRegionSelectionLeftSide       = ast.literal_eval(cfgparser.get("configuration","controlRegionSelectionLeftSide"))
        print "    -The controlRegionSelectionLeftSide:"
        print "      *",self.controlRegionSelectionLeftSide

        self.controlRegionSelectionOutHalf       = ast.literal_eval(cfgparser.get("configuration","controlRegionSelectionOutHalf"))
        print "    -The controlRegionSelectionOutHalf:"
        print "      *",self.controlRegionSelectionOutHalf

        self.controlRegionSelectionInHalf       = ast.literal_eval(cfgparser.get("configuration","controlRegionSelectionInHalf"))
        print "    -The controlRegionSelectionInHalf:"
        print "      *",self.controlRegionSelectionInHalf

        self.controlRegionSelectionInQtr       = ast.literal_eval(cfgparser.get("configuration","controlRegionSelectionInQtr"))
        print "    -The controlRegionSelectionInQtr:"
        print "      *",self.controlRegionSelectionInQtr

        self.controlRegionSelectionOutQtr       = ast.literal_eval(cfgparser.get("configuration","controlRegionSelectionOutQtr"))
        print "    -The controlRegionSelectionOutQtr:"
        print "      *",self.controlRegionSelectionOutQtr

        self.controlRegionSelectionExcRightOut = ast.literal_eval(cfgparser.get("configuration","controlRegionSelectionExcRightOut"))
        print "    -The controlRegionSelectionExcRightOut:"
        print "      *",self.controlRegionSelectionExcRightOut

        self.controlRegionSelectionExcLeftOut = ast.literal_eval(cfgparser.get("configuration","controlRegionSelectionExcLeftOut"))
        print "    -The controlRegionSelectionExcLeftOut:"
        print "      *",self.controlRegionSelectionExcLeftOut

        self.bTagScoreSelection = ast.literal_eval(cfgparser.get("configuration","bTagScoreSelection"))
        print "    -The bTagScoreSelection:"
        print "      *",self.bTagScoreSelection

        self.skimFolder                   = ast.literal_eval(cfgparser.get("configuration","skimFolder"))
        print "    -The skimFolder:"
        print "      *",self.skimFolder
        self.skimFolderMW                   = ast.literal_eval(cfgparser.get("configuration","skimFolderMW"))
        print "    -The Mass Window skimFolder:"
        print "      *",self.skimFolderMW
        self.variables                    = ast.literal_eval(cfgparser.get("configuration","variables"))
        print "    -The list of variables:"
        for x in range(len(self.variables)):
            print "      *",self.variables[x]
        self.trainingVariables            = ast.literal_eval(cfgparser.get("configuration","trainingVariables"))
        print "    -The list of training variables:"
        for x in range(len(self.trainingVariables)):
            print "      *",self.trainingVariables[x]
        self.bTagSelection                = ast.literal_eval(cfgparser.get("configuration","bTagSelection"))
        print "    -The bTagSelection:"
        print "      *",self.bTagSelection
        self.antiBTagSelection            = ast.literal_eval(cfgparser.get("configuration","antiBTagSelection"))
        print "    -The antiBTagSelection:"
        print "      *",self.antiBTagSelection
        self.threadNumber       = ast.literal_eval(cfgparser.get("configuration","threadNumber"))
        print "    -The thread number for applying weights:"
        print "      *",self.threadNumber

        self.analysisBackgroundArgument       = ast.literal_eval(cfgparser.get("configuration","analysisBackgroundArgument"))
        print "    -The analysis background arguments:"
        print "      *",self.analysisBackgroundArgument

        self.analysisClassifierArgument       = ast.literal_eval(cfgparser.get("configuration","analysisClassifierArgument"))
        print "    -The analysis classifier arguments:"
        print "      *",self.analysisClassifierArgument

        self.addSelection                     = ast.literal_eval(cfgparser.get("configuration","addSelection"))
        print "    - Additional cuts, Mass window selections: "
        print "      *",self.addSelection

        self.year                     = ast.literal_eval(cfgparser.get("configuration","year"))
        print " year for the configuration file"
        print "      *Year: ",self.year


