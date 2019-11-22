import os
import shutil
import sys

from git import Repo
from git.exc import InvalidGitRepositoryError

sys.path.insert(1, os.path.relpath('./ScriptsEnvironment/scripts'))
import ScriptsEnvironment.scripts.build_oval_definitions_file as build_oval_definitions_file


def build_definition_cli():
    """
    Removing 1  argument of command line because build_oval_definitions_file
    will process command line arguments with own parser (but it want optional
    arguments to start from index '1').

    In GUI we won't need this since we'll operate with build_definition directly and do not use arguments.
    """
    sys.argv.pop(0)
    build_definition()


def build_definition():
    """
    This function will create fake GIT environment. There is no visible speed
    growth when indexing OVAL repository with git all the time. It is faster
    to just commit one little file and start build the definition.
    """

    # creating fake environment for scripts
    try:
        shutil.rmtree(os.path.relpath('./ScriptsEnvironment/.git'))
        os.remove(os.path.relpath('./ScriptsEnvironment/.init'))
    except FileNotFoundError:
        pass

    with open(os.path.relpath('./ScriptsEnvironment/.init'), 'w') as file:
        file.write('init')

    try:
        repo = Repo(os.path.relpath('./ScriptsEnvironment'))
    except InvalidGitRepositoryError:
        repo = Repo.init(os.path.relpath('./ScriptsEnvironment'))

    index = repo.index
    index.add(['.init'])
    index.commit("env")

    build_oval_definitions_file.main()

    # removing fake environment for next use
    try:
        shutil.rmtree(os.path.relpath('./ScriptsEnvironment/.git'))
        os.remove(os.path.relpath('./ScriptsEnvironment/.init'))
    except FileNotFoundError:
        pass
