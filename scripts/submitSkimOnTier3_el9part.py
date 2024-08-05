import os
import sys
import argparse
import getpass

def parseInputFileList (fileName) :
    filelist = []
    with open (fileName) as fIn:
        for line in fIn:
            line = (line.split("#")[0]).strip()
            if line:
                filelist.append(line)
    return filelist

parser = argparse.ArgumentParser(description='Command line parser of skim options')
parser.add_argument('--input'     ,  dest = 'input'     ,  help = 'input filelist'           ,  required = True        )
parser.add_argument('--tag'       ,  dest = 'tag'       ,  help = 'production tag'           ,  required = True        )

parser.add_argument('--outputName', dest='oname',  help='the name of the output (if not given, auto from filelist)', default = None)
parser.add_argument('--njobs'     ,  dest = 'njobs'     ,  help = 'njobs'                    ,  type     = int         ,   default = 500    )

parser.add_argument('--append'    ,  dest = 'append'    ,  help = 'production tag'           ,  required = False, default=""        )
parser.add_argument('--verbose',        dest='verbose',    help='set verbose mode',                  action='store_true',  default=False)

#         --input=${inputFiles}   \
#         --tag=${submitTag} \
#         --cfg=${configFile}  \
#         --puWeight=${weightFile}  \
#         --xs=${crossSection}   \
#         --njobs=${numberOfJobs} \

args, unknown = parser.parse_known_args()

username = getpass.getuser()
print( "... Welcome", username)
oname = args.oname
if not oname:
    # print "A:" , args.input
    # print "B:" , args.input.rsplit(r'/', 1)[-1]
    # print "C:" , args.input.rsplit(r'/', 1)[0].rsplit('.', 1)
    oname = args.input.rsplit(r'/', 1)[-1].rsplit('.', 1)[0]
oname = 'SKIM_' + oname + args.append

jobsDir                = 'CondorJobs/skimming/jobs_' + args.tag + '/' + oname
outScriptNameBareProto = 'job_{0}.sh'

inputfiles = parseInputFileList (args.input)    ## parse input list
njobs      = args.njobs if args.njobs <= len (inputfiles) else len (inputfiles)

bbbbWorkDir  = os.getcwd()

## set directory to job directory, so that logs will be saved there
os.chdir(jobsDir)
for n in range(0, njobs):
    command = "%s/scripts/t3el7submit %s" % (bbbbWorkDir, outScriptNameBareProto.format(n))
    if args.verbose: print("** INFO: submit job with command", command)
    if os.system(command) != 0:
        print("... Not able to execute command \"", command, "\", exit")
        sys.exit()

