import os, shutil, sys
from git import Repo
sys.path.insert(1, os.path.relpath('./ScriptsEnvironment/scripts'))
import ScriptsEnvironment.scripts.build_oval_definitions_file as build_oval_definitions_file

def build_definition_cli(args):
    # removing 1, 2 and 3 arguments of command line because
    # build_oval_definitions_file will use them with own parser
    # in GUI we won't need this since we'll operate with 
    # build_definition directly

    if len(sys.argv)>2:
        try:
            for i in range(0,3):
                sys.argv.pop(1)
        except IndexError:
            pass
    build_definition(args)



def build_definition(args):
    
    for a in vars(args)['options'].split(' '):
        sys.argv.append(a)
  
    # creating fake environment for scripts
    try:
        shutil.rmtree(os.path.relpath('./ScriptsEnvironment/.git'))
        os.remove(os.path.relpath('./ScriptsEnvironment/.init'))
    except:
        pass

    open(os.path.relpath('./ScriptsEnvironment/.init'), 'w').close()
    repo = Repo.init(os.path.relpath('./ScriptsEnvironment'))
    index = repo.index
    index.add( [ '.init' ] )
    index.commit("init")

    build_oval_definitions_file.main()

    # removing fake environment for next use
    try:
        shutil.rmtree(os.path.relpath('./ScriptsEnvironment/.git'))
        os.remove(os.path.relpath('./ScriptsEnvironment/.init'))
    except:
        pass