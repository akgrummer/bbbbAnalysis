import os
import sys
import argparse
import getpass
import subprocess

year="2016"
configFile = 'config/Resonant_NMSSM_bbbb/plotter_{0}Resonant_NMSSM_XYH_bbbb_systBDT_2022Apr.cfg'
selectionFile='config/Resonant_NMSSM_bbbb/selectionCfg_{0}Resonant_NMSSM_XYH_bbbb_all.cfg'
commandSED = "sed -i 's/2022Apr25_seed2025/2022Apr25_seed{0}/g' {1}"
commandSEDback = "sed -i 's/2022Apr25_seed{0}/2022Apr25_seed2025/g' {1}"
commandFill = 'fill_histograms.exe config/Resonant_NMSSM_bbbb/plotter_{0}Resonant_NMSSM_XYH_bbbb_systBDT_2022Apr.cfg >> BDTfill/out.txt 2>> BDTfill/err.txt'
for seed in range(2029,2312):
#  for seed in range(2028,2029):
    if os.system(commandSED.format(seed,configFile.format(year))) != 0:
        print "... Error Not able to execute command \"", commandSED.format(seed,configFile.format(year)), "\", exit"
        sys.exit()
    if os.system(commandSED.format(seed,selectionFile.format(year))) != 0:
        print "... Error Not able to execute command \"", commandSED.format(seed,selectionFile.format(year)), "\", exit"
        sys.exit()
    if os.system(commandFill.format(year)) != 0:
        print "... Error Not able to execute command \"", commandFill.format(year), "\", exit"
        sys.exit()
    if os.system(commandSEDback.format(seed,configFile.format(year))) != 0:
        print "... Error Not able to execute command \"", commandSEDback.format(seed,configFile.format(year)), "\", exit"
        sys.exit()
    if os.system(commandSEDback.format(seed,selectionFile.format(year))) != 0:
        print "... Error Not able to execute command \"", commandSEDback.format(seed,selectionFile.format(year)), "\", exit"


