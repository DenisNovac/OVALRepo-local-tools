import os
import modules.submodules.read_title as read_title

def list_repository( args ):
    # this path is relative to function start path (where local_repo_mgmt.py file called)
    repository_path = os.path.relpath('./ScriptsEnvironment/repository/')
    modes = {
        'a': repository_path,
        'd': repository_path+os.sep+'definitions',
        't': repository_path+os.sep+'tests',
        'o': repository_path+os.sep+'objects',
        's': repository_path+os.sep+'states',
        'v': repository_path+os.sep+'variables'
    }
    mode = vars(args)['m']
    rootdir = modes[mode]

    isDefInfo = True
    isFull=False
    isLocalTotal=False

    format_option = vars(args)['f']
    if format_option == 'f': isFull=True
    if format_option == 'l': isLocalTotal=True
    if format_option == 'h': isDefInfo=False
    #try:
    #    if args[2] == '-f': isFull=True
    #    if args[2] == '-l': isLocalTotal=True
    #except: pass

    calc=0
    local_calc=0
    lastflag=""
    flag=""
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            path=os.path.join(subdir, file)
            if not isFull:
                short_path=path.split(os.path.relpath("ScriptsEnvironment/repository/"))[1]
                flag=short_path.split(os.sep)[1]
                nc_path=short_path.replace(flag+os.sep,"")
                local_calc=local_calc+1
                if not lastflag==flag:
                    if not lastflag=="" and isLocalTotal:
                        print("\tTotal in category: "+str(local_calc))
                    local_calc=0
                    print(flag+": ")
                    lastflag=flag
                # вывод укороченной версии имени
                title = ''
                if flag=='definitions' and isDefInfo:
                    title = read_title.read_title(path)
                
                # замена _ на : в id
                spl = nc_path.split(os.sep)
                spl[len(spl)-1] = spl[len(spl)-1].replace('_',':')
                nc_path = os.sep.join(spl).replace('.xml','')
                print('\t'+nc_path + '\t ' + title)
                
            else:
                # вывод полной версии имени
                print(path)
            calc=calc+1
    if not isFull and isLocalTotal:
        local_calc=local_calc+1
        print("\tTotal in category: "+str(local_calc))
    print("Total: "+str(calc))
        