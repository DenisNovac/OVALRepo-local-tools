"""Local OVAL Repository Managment tool.

It is a wrapper for several OVALRepo modules:
oval_decomposition.py
build_oval_definitions_file.py

And some OVALRepo libs (see ScriptsEnvironment/scripts).

Allows to run local OVAL repository by creating false git environment for it.

Author: Denis Yablochkin <denis-yablochkin.ib@yandex.ru>

Copyright: https://github.com/CISecurity/OVALRepo
Copyright© 2010 United States Government. All Rights Reserved.
"""
from modules.ArgumentsParser import ArgumentsParser


def main():
    ArgumentsParser.parse_arguments()

# always need this to make sure that module was not called from return of submodules
if __name__ == '__main__':
    main()
