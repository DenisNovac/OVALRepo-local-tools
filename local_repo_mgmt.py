# coding: utf-8
"""
    Local OVAL repository managment tool.
    It is a wrapper for several OVALRepo modules:
    oval_decomposition.py
    build_oval_definitions_file.py

    Allows to run local OVAL repository by creating false git environment for it.

    Author: Denis Yablochkin <denis-yablochkin.ib@yandex.ru>
    
    
    Copyright: https://github.com/CISecurity/OVALRepo
    Copyright© 2010 United States Government. All Rights Reserved.
"""
import os, shutil, sys, datetime
from git import Repo
# import modules from OVALRepo-scripts
sys.path.insert(1,'./ScriptsEnvironment/scripts')
import ScriptsEnvironment.scripts.oval_decomposition as oval_decomposition
import ScriptsEnvironment.scripts.build_oval_definitions_file as build_oval_definitions_file

import ScriptsEnvironment.scripts.definition_title_reader as definition_title_reader


def decomposition( auto_remove_decomposed=False ):
    """
        Every module MUST have this part in <definition>:
        <oval_repository>
            <dates>
                <submitted date="YYYY-MM-DDTHH:MM:SS.000+00:00">
                    <contributor organization="ORGANISATION">JOHN WICK</contributor>
                </submitted>
            </dates>
        </oval_repository>
        
    """
    # need to call decompose module help if there is no more arguments
    input_path = ''
    try:
        input_path=os.sys.argv[2]
    except IndexError:
        oval_decomposition.main()
        return

    configs = [ ]
    if input_path[len(input_path)-1] == os.sep:
        configs_root = os.path.abspath(input_path)
        file_list=os.listdir(os.path.relpath(input_path))
        for file in file_list:
            configs.append(configs_root+os.sep+file)
    else:
        configs.append(os.path.abspath(os.sys.argv[2]))
    
    for config in configs:
        sys.stdout.write("Decomposing "+config+" ...")
        sys.argv[2]=config
    
        oval_decomposition.main()

        if auto_remove_decomposed:
            config_name=config.split(os.sep)[len(config.split(os.sep))-1]
            path = os.path.abspath(sys.argv[2])
            try:
                os.mkdir(os.path.abspath('./.decomposed'))
                os.system("attrib +h " + os.path.abspath('./.decomposed'))
            except:
                pass
            time=datetime.datetime.now()
            ts=str(datetime.datetime.timestamp(time))
            shutil.move(path,os.path.abspath('./.decomposed/'+ts+' '+config_name))

        sys.stdout.write(" Success\n")

def build():
    try:
        shutil.rmtree(os.path.relpath('./ScriptsEnvironment/.git'))
    except:
        pass
    
    open(os.path.relpath('./ScriptsEnvironment/.init'), 'w').close()
    repo = Repo.init(os.path.relpath('./ScriptsEnvironment'))
    index = repo.index
    index.add( [ '.init' ] )
    index.commit("init")
    try:
        build_oval_definitions_file.main()
    except Exception as e:
        print(str(e))

    try:
        shutil.rmtree(os.path.relpath('./ScriptsEnvironment/.git'))
        os.remove(os.path.relpath('./ScriptsEnvironment/.init'))
    except:
        pass


def clear( args, clear_decomposed_folder=False ):
    """
        Clears files and folders:
        ./ScriptsEnvironment/.git/
        ./ScriptsEnvironment/.init
        ./ScriptsEnvironment/scripts/__pycache__/
        ./ScriptsEnvironment/scripts/__index__/

        If specified like -cd will also remove folder:
        ./.decomposed
    """

    if len(args)>1:
        help(clear)
        return

    try:
        shutil.rmtree(os.path.relpath('./ScriptsEnvironment/.git'))
        print('removed ./ScriptsEnvironment/.git')
    except Exception as e:
        print(str(e))
    try:
        os.remove(os.path.relpath('./ScriptsEnvironment/.init'))
        print('removed ./ScriptsEnvironment/.init')
    except Exception as e:
        print(str(e))
    try:
        shutil.rmtree(os.path.relpath('./ScriptsEnvironment/scripts/__pycache__'))
        print('removed __pycache__')
    except Exception as e:
        print(str(e))
    try:
        shutil.rmtree(os.path.relpath('./ScriptsEnvironment/scripts/__index__'))
        print('removed __index__')
    except Exception as e:
        print(str(e))
    if clear_decomposed_folder:
        try:
            shutil.rmtree(os.path.relpath('./.decomposed'))
            print('removed ./.decomposed')
        except Exception as e:
            print(str(e))



def list(args):
    """
        Lists files in repository.
        Category (second arg):
        -a all
        -d definitions
        -t tests
        -o objects
        -s states
        -v variables

        Formatting (third arg):
        -f for full paths without categories
        -l for local total files calculation
    """
    isDefInfo = True

    isFull=False
    isLocalTotal=False
    try:
        if args[2] == '-f': isFull=True
        if args[2] == '-l': isLocalTotal=True
    except: pass

    try:
        rootdir=''
        if args[1] == '-t':
            rootdir=os.path.relpath('./ScriptsEnvironment/repository/tests')
        elif args[1] == '-v':
            rootdir=os.path.relpath('./ScriptsEnvironment/repository/variables')
        elif args[1] == '-s':
            rootdir=os.path.relpath('./ScriptsEnvironment/repository/states')
        elif args[1] == '-o':
            rootdir=os.path.relpath('./ScriptsEnvironment/repository/objects')
        elif args[1] == '-d':
            rootdir=os.path.relpath('./ScriptsEnvironment/repository/definitions')
        elif args[1] == '-a':
            rootdir=os.path.relpath('./ScriptsEnvironment/repository/')
        else:
            help(list)

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
                        title = definition_title_reader.read_title(path)
                    print('\t'+nc_path + '\t ' + title)
                    
                else:
                    # вывод полной версии имени
                    print(path)
                calc=calc+1
        if not isFull and isLocalTotal:
            local_calc=local_calc+1
            print("\tTotal in category: "+str(local_calc))
        print("Total: "+str(calc))
        
    except IndexError as e:
        print(str(e))
        help(list)



def main(args):
    """
        Local OVAL repository managment tool

        USAGE
        Building and decomposing work with ./ScriptsEnvironment/repository folder.

        * DECOMPOSE xml-config to parts (definitions, objects etc):
        local_repo_mgmt.py -d[r] [-h]
        -dr will move decomposed file to .decomposed folder.
        if PATH to decompose file (-d -f <PATH>) is folder - it will decompose every file in it (without subfolders).
        NOTE: Decomposing will ALWAYS replace files with equals ID. Use -l -a to check IDs in your repository.


        * BUILD xml-config from repository:
        local_repo_mgmt.py -b [-h]


        * CLEAR scripts false git environment:
        local_repo_mgmt.py -c[d] [-h]
        -cd will also remove .decomposed folder.


        * LIST files in repository:
        local_repo_mgmt.py -l [-adtosvh] [-fl]
    """

    try:
        if args[1]=='-d':
            args.pop(1) 
            decomposition()

        elif args[1]=='-dr':
            args.pop(1)
            decomposition( auto_remove_decomposed=True )

        elif args[1]=='-b':
            args.pop(1)
            build()

        elif args[1] == '-c':
            args.pop(1)
            clear( args )

        elif args[1] == '-cd':
            args.pop(1)
            clear( args, clear_decomposed_folder=True )
        
        elif args[1] == '-l':
            args.pop(1)
            list(args)
        else:
            help(main)

    except IndexError:
        help(main)


if __name__ == '__main__':
    main(sys.argv)


