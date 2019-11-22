import os, sys, shutil, re, time, datetime
sys.path.insert(1, os.path.relpath('./ScriptsEnvironment/scripts'))
import ScriptsEnvironment.scripts.oval_decomposition as oval_decomposition


def decompose_definition():
    # removing 1 and 2 arguments of command line because
    # oval_decomposition will use them with own parser
    sys.argv.pop(0)
    sys.argv.pop(0)

    # getting input path to a variable to check if it is a folder later
    input_path = None
    try:
        input_path = re.search(r'-f (?P<input_path>(\S*))', ' '.join(sys.argv))['input_path']
    except TypeError as e:
        sys.argv.clear()
        sys.argv.append('-h')

    if '-h' in sys.argv:
        print_own_help()
        oval_decomposition.main()
        return

    remove_decomposed = False
    if '-r' in sys.argv:
        remove_index = sys.argv.index('-r')
        sys.argv.pop(remove_index)
        remove_decomposed = True

    configs = []
    # if this is a dir - take all files for decomposing
    if os.path.isdir(input_path):
        configs_root = os.path.relpath(input_path)
        file_list = os.listdir(os.path.relpath(input_path))
        for file in file_list:
            configs.append(configs_root + os.sep + file)
    else:
        configs.append(os.path.relpath(input_path))

    for config in configs:
        sys.stdout.write("Decomposing " + config + " ...")
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
        if remove_decomposed:
            # last word after / is a name of file
            config_name = config.split(os.sep)[len(config.split(os.sep)) - 1]
            path = os.path.abspath(sys.argv[2])
            try:
                os.mkdir(os.path.abspath('./.decomposed'))
                os.system("attrib +h " + os.path.abspath('./.decomposed'))
            except FileExistsError:
                pass

            # timestamp for no replacing decomposed files with same names
            now = datetime.datetime.now()
            ts = str(datetime.datetime.timestamp(now))
            shutil.move(path, os.path.abspath('./.decomposed/' + ts + ' ' + config_name))

        sys.stdout.write(" Success\n")
        sys.stdout.flush()


def print_own_help():
    help_message = '''Additional info for decompose: 
    -f may also include a folder (no spaces in name allowed). All definitions in folder will be decomposed
    -v verbose output (print all created/replaced files)
    -r remove decomposed files to .decompose folder
    '''
    print(help_message)
