import shutil, os

def clear_repository( args ):
    # temp folders and fake environment folders
    clear_path = [
        './ScriptsEnvironment/.git',
        './ScriptsEnvironment/.init',
        './ScriptsEnvironment/scripts/__pycache__',
        './ScriptsEnvironment/scripts/__index__',

        './modules/__pycache__',
        './modules/submodules/__pycache__',
    ]

    if vars(args)['decomposed']:
        clear_path.append('./.decomposed')

    # clearing the pathes
    for path in clear_path:
        path = os.path.relpath(path)
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            print('Removed '+path)
        except FileNotFoundError as e:
            print(str(e))