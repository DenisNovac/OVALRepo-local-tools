import os, sys, shutil, re
from datetime import datetime
sys.path.insert(1, os.path.relpath('./ScriptsEnvironment/scripts'))
import ScriptsEnvironment.scripts.oval_decomposition as oval_decomposition

def decompose_definition( args ):
    # removing 1, 2 and 3 arguments of command line because
    # oval_decomposition will use them with own parser
    verbose_output = False
    input_path=''
    # take path from arguments: -f <path> and check for -v flag
    try:
        if re.search('(^-v)|(-v$)', vars(args)['o'].strip()):
            verbose_output=True
        input_path = vars(args)['o'].split('-f ')[1]
        input_path = input_path.split(' ')[0]
    except Exception:
        # call help from oval_decomposition if no path specified
        sys.argv.clear()
        sys.argv.append('')
        sys.argv.append('')
        oval_decomposition.main()

    auto_remove_decomposed = vars(args)['r']

    configs = [ ]    
    if os.path.isdir(input_path):
        configs_root = os.path.relpath(input_path)
        file_list=os.listdir(os.path.relpath(input_path))
        for file in file_list:
            configs.append(configs_root+os.sep+file)
    else:
        configs.append(os.path.relpath(input_path))


    for config in configs:
        sys.stdout.write("Decomposing "+config+" ...")
        sys.stdout.flush()
        
        # new console arguments for every config because
        # oval_decomposition uses it's own argument parser
        sys.argv.clear()
        sys.argv.append('')
        sys.argv.append('-f')
        sys.argv.append(config)
        if verbose_output:
            sys.argv.append('-v')
        oval_decomposition.main()

        # replaces decomposed configs in .decomposed folder
        if auto_remove_decomposed:
            config_name=config.split(os.sep)[len(config.split(os.sep))-1]
            path = os.path.abspath(sys.argv[2])
            try:
                os.mkdir(os.path.abspath('./.decomposed'))
                os.system("attrib +h " + os.path.abspath('./.decomposed'))
            except:
                pass
            time=datetime.now()
            ts=str(datetime.timestamp(time))
            shutil.move(path,os.path.abspath('./.decomposed/'+ts+' '+config_name))

        sys.stdout.write(" Success\n")
        sys.stdout.flush()