import os, shutil, sys, random
from git import Repo
from git.exc import InvalidGitRepositoryError

sys.path.insert(1, os.path.relpath('./ScriptsEnvironment/scripts'))
import ScriptsEnvironment.scripts.build_oval_definitions_file as build_oval_definitions_file

def build_definition_cli(args):
    """
    Removing 1, 2 and 3 arguments of command line because
    build_oval_definitions_file will process command line arguments
    with own parser. In GUI we won't need this since we'll operate with
    build_definition directly and do not use arguments.
    """

    if len(sys.argv)>2:
        try:
            for i in range(0,3):
                sys.argv.pop(1)
        except IndexError:
            pass
    build_definition(args)



def build_definition(args):
    """
    This function will create fake GIT environment. There is no visible speed
    growth when indexing OVAL repository with git all the time. It is faster
    to just commit one little file and make build.
    """

    for a in vars(args)['options'].split(' '):
        sys.argv.append(a)
  
    # creating fake environment for scripts
    try:
        shutil.rmtree(os.path.relpath('./ScriptsEnvironment/.git'))
        os.remove(os.path.relpath('./ScriptsEnvironment/.init'))
    except:
        pass

    with open(os.path.relpath('./ScriptsEnvironment/.init'), 'w') as file:
        file.write('init')
        
    try:
        repo = Repo(os.path.relpath('./ScriptsEnvironment'))
    except InvalidGitRepositoryError:
        repo = Repo.init(os.path.relpath('./ScriptsEnvironment'))
    
    index = repo.index
    index.add( [ '.init' ] )
    index.commit("env")

    build_oval_definitions_file.main()

    # removing fake environment for next use
    try:
        shutil.rmtree(os.path.relpath('./ScriptsEnvironment/.git'))
        os.remove(os.path.relpath('./ScriptsEnvironment/.init'))
    except:
        pass