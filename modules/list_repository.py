import os
import modules.submodules.read_title as read_title

def list_repository( args ):
    """Function for arguments processing and repository printing"""

    # this path is relative to function start path (where lrm.py file called)
    repository_path = os.path.relpath('./ScriptsEnvironment/repository/')
    # modes is similar to command line options, so we'll map them to each other
    # so command line option 'd' will make repository_path+os.sep+'definitions'
    modes = {
        'a': repository_path,
        'd': repository_path+os.sep+'definitions',
        't': repository_path+os.sep+'tests',
        'o': repository_path+os.sep+'objects',
        's': repository_path+os.sep+'states',
        'v': repository_path+os.sep+'variables'
    }
    mode = vars(args)['mode']
    rootdir = modes[mode]

    isFull = True if vars(args)['format']=='f' else False
    isLocalTotal = True if vars(args)['format']=='l' else False
    isHidingDefinitions = True if vars(args)['format']=='h' else False

    # Printing repository content
    repo = None
    length = 0
    if isFull:
        repo = get_simple_repository_content(rootdir)
        for e in repo:
            print(e)
        length=len(repo)
        
    else:
        repo= get_repository_dir(rootdir)
        for oval_type in repo:
            length+=len(repo[oval_type])
            print(oval_type+':')
            if oval_type=='definitions':
                for id in repo[oval_type]:
                    show_title = repo[oval_type][id] if not isHidingDefinitions else ''
                    print('\t'+id+'\t'+show_title)
            else: 
                for entity in repo[oval_type]:
                    print('\t'+entity)
            
            if isLocalTotal:
                print('\tType total: '+str(len(repo[oval_type])))

    print('Total: '+str(length))
    



def get_repository_dir( rootdir ):
    """
    Function for smart dictionary creating. Will create
    dictionaries

    """

    repository_dict = { }

    lastflag=''
    flag=''
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            path=os.path.join(subdir, file)
            # generating short path (cutting out the beginning)
            short_path=path.split(os.path.relpath('ScriptsEnvironment/repository/'))[1]
            # generating flag (class of oval entity)
            flag=short_path.split(os.sep)[1]
            # cutting out the flag from path
            short_path=short_path.replace(flag+os.sep,'')

            if not lastflag==flag:
                # this called once for each category of OVAL files
                lastflag=flag
                # only definitions has the title which can be used as key
                if flag=='definitions':
                    repository_dict[flag]={ }
                else:
                    repository_dict[flag]=[ ]

            # make name of the entity useful for copying/finding in
            # OVAL xml sources
            spl = short_path.split(os.sep)
            spl[len(spl)-1] = spl[len(spl)-1].replace('_',':')
            short_path = os.sep.join(spl).replace('.xml','')

            if flag=='definitions':
                id = short_path.split(os.sep)[-1]
                title = read_title.read_title(path)
                # not every definition may have the title, so we use ID instead
                if title:
                    """
                    There is a lot of equal titles even in OVAL Repo from CISecurity,
                    so we can not use title as a key by itself.
                    """
                    repository_dict[flag][short_path]=title
                else:
                    repository_dict[flag][short_path.split(os.sep)[-1]]=id
            else:
                repository_dict[flag].append(short_path)
    return repository_dict



def get_simple_repository_content( rootdir ):
    """
    This function will return an simple array of paths
    """
    repository_array = [ ]
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            path=os.path.join(subdir, file)
            repository_array.append(path)
    return repository_array
