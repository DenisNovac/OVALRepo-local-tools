# coding: utf-8
"""
    Local OVAL repository managment tool.
    It is a wrapper for several OVALRepo modules:
    oval_decomposition.py
    build_oval_definitions_file.py

    Allows to run local OVAL repository by creating false git environment for it.

    Author: Denis Yablochkin <denis-yablochkin.ib@yandex.ru>
    Copyright: https://github.com/CISecurity/OVALRepo
"""
import os, shutil, sys
from git import Repo
# import modules from OVALRepo-scripts
sys.path.insert(1,'./ScriptsEnvironment/scripts')
import oval_decomposition
import build_oval_definitions_file


def decomposition():
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
    oval_decomposition.main()



def build():
    try:
        shutil.rmtree(os.path.abspath('./ScriptsEnvironment/.git'))
    except:
        pass
    
    open(os.path.abspath('./ScriptsEnvironment/.init'), 'w').close()
    repo = Repo.init(os.path.abspath('./ScriptsEnvironment'))
    index = repo.index
    index.add( [ '.init' ] )
    index.commit("init")
    try:
        build_oval_definitions_file.main()
    except Exception as e:
        print("ee")

    try:
        shutil.rmtree(os.path.abspath('./ScriptsEnvironment/.git'))
        os.remove(os.path.abspath('./ScriptsEnvironment/.init'))
    except:
        pass


def clear(args):
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
        shutil.rmtree(os.path.abspath('./ScriptsEnvironment/.git'))
    except Exception as e:
        print(str(e))
    try:
        os.remove(os.path.abspath('./ScriptsEnvironment/.init'))
    except Exception as e:
        print(str(e))



def list(args):
    """
        Lists files in repository:
        -d definitions
        -t tests
        -o objects
        -s states
        -v variables
        -a all
    """
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
        
        for subdir, dirs, files in os.walk(rootdir):
            for file in files:
                print(os.path.join(subdir, file))

    except IndexError as e:
        help(list)



def main(args):
    """
        Local OVAL repository managment tool.

        USAGE
        Decompose xml-config to it's parts:
        local_repo_mgmt.py -d [-h]

        Build xml-config:
        local_repo_mgmt.py -b [-h]

        Clear scripts false git environment:
        local_repo_mgmt.py -c [-h]

        List files in repository:
        local_repo_mgmt.py -l [-adtosvh]

    """
    try:
        if args[1]=='-d':
            args.pop(1) 
            decomposition()

        elif args[1]=='-b':
            args.pop(1)
            build()

        elif args[1] == '-c':
            args.pop(1)
            clear(args)
        
        elif args[1] == '-l':
            args.pop(1)
            list(args)
        else:
            help(main)

    except IndexError:
        help(main)


if __name__ == '__main__':
    main(sys.argv)


