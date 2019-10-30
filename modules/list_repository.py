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
                for title in repo[oval_type]:
                    show_title=title if not isHidingDefinitions else ''
                    print('\t'+repo[oval_type][title]+'\t'+show_title)
            else: 
                for entity in repo[oval_type]:
                    print('\t'+entity)
            
            if isLocalTotal:
                print('\tType total: '+str(len(repo[oval_type])))
            
    
    print('Total: '+str(length))
    



def get_repository_dir( rootdir ):
    """Function for smart dictionary creating"""

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
                lastflag=flag
                # only definitions has the title which can be used as key
                if flag=='definitions':
                    repository_dict[flag]={ }
                else:
                    repository_dict[flag]=[ ]
                
            title = None
            if flag=='definitions':
                title_get = read_title.read_title(path, False)
                if title_get:
                    title=title_get

            # make name of the entity useful for copying/finding in
            # OVAL xml sources
            spl = short_path.split(os.sep)
            spl[len(spl)-1] = spl[len(spl)-1].replace('_',':')
            short_path = os.sep.join(spl).replace('.xml','')

            if title:
                repository_dict[flag][title]=short_path
            else:
                repository_dict[flag].append(short_path)
    return repository_dict



def get_simple_repository_content( rootdir ):
    """This function will return an simple array of paths"""
    repository_array = [ ]
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            path=os.path.join(subdir, file)
            repository_array.append(path)
    return repository_array
