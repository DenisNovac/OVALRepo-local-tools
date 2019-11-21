import os, sys, shutil, re, time
from datetime import datetime
sys.path.insert(1, os.path.relpath('./ScriptsEnvironment/scripts'))
import ScriptsEnvironment.scripts.oval_decomposition as oval_decomposition

def decompose_definition(args):
    # removing 1 and 2 arguments of command line because
    # oval_decomposition will use them with own parser
    sys.argv.pop(0)
    sys.argv.pop(0)

    # check if there is auto_remove_decomposed flag
    #if ''

    # check if input path is a folder
    input_path = None
    try:
        input_path = re.search(r'-f (?P<input_path>(\S*))', ' '.join(args))['input_path']
    except TypeError as e:
        sys.argv.clear()
        sys.argv.append('-h')
        oval_decomposition.main()

    #auto_remove_decomposed = vars(args)['remove_decomposed']

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
        is_verbose = False
        if '-v' in sys.argv:
            is_verbose = True
        sys.argv.clear()
        sys.argv.append('')
        sys.argv.append('-f')
        sys.argv.append(config)
        if is_verbose:
            sys.argv.append('-v')
            # This is because you want to see when it switches to another file on decomposing
            time.sleep(1)
        oval_decomposition.main()


        # replaces decomposed configs in .decomposed folder
        #if auto_remove_decomposed:
        #    config_name=config.split(os.sep)[len(config.split(os.sep))-1]
        #    path = os.path.abspath(sys.argv[2])
        #    try:
        #        os.mkdir(os.path.abspath('./.decomposed'))
        #        os.system("attrib +h " + os.path.abspath('./.decomposed'))
        #    except:
        #        pass
        #    time=datetime.now()
        #    ts=str(datetime.timestamp(time))
        #    shutil.move(path,os.path.abspath('./.decomposed/'+ts+' '+config_name))

        sys.stdout.write(" Success\n")
        sys.stdout.flush()

