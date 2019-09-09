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
import oval_decomposition
import build_oval_definitions_file


def decomposition( removeAfter=False ):
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
    # folder check
    input_path=os.sys.argv[2]

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

        if removeAfter:
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
        print("ee")

    try:
        shutil.rmtree(os.path.relpath('./ScriptsEnvironment/.git'))
        os.remove(os.path.relpath('./ScriptsEnvironment/.init'))
    except:
        pass


def clear( args, removeDecomposed=False ):
    """
        Clears false git envrionment ScriptsEnvironment.
    """
    try:
        if args[1] == '-h':
            help(clear)
            return
    except:
        pass

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
    
    if removeDecomposed:
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
                        

                    print("\t"+nc_path)
                else:
                    print(path)
                calc=calc+1
        if not isFull and isLocalTotal:
            local_calc=local_calc+1
            print("\tTotal in category: "+str(local_calc))
        print("Total: "+str(calc))
        
    except IndexError as e:
        help(list)



def main(args):
    """
        Local OVAL repository managment tool.

        USAGE
        Decompose xml-config to it's parts:
        local_repo_mgmt.py -d[r] [-h]
        -dr will move decomposed file to .decomposed folder
        if -f argument after -d is FOLDER, it will attempt to decompose all files in folder

        Build xml-config:
        local_repo_mgmt.py -b [-h]

        Clear scripts false git environment:
        local_repo_mgmt.py -c[r] [-h]
        -cr will remove .decomposed folder

        List files in repository:
        local_repo_mgmt.py -l [-adtosvh] [-fl]

    """
    try:
        if args[1]=='-d':
            args.pop(1) 
            decomposition()

        elif args[1]=='-dr':
            args.pop(1)
            decomposition( True )

        elif args[1]=='-b':
            args.pop(1)
            build()

        elif args[1] == '-c':
            args.pop(1)
            clear( args )

        elif args[1] == '-cr':
            args.pop(1)
            clear( args, True )
        
        elif args[1] == '-l':
            args.pop(1)
            list(args)
        else:
            help(main)

    except IndexError:
        help(main)


if __name__ == '__main__':
    main(sys.argv)


