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
import logging

def main():
    """
    Initializing root logger and start ArgumentParser
    """
    handler = logging.StreamHandler()
    # Readable format for all loggers in app
    format_str = '%(asctime)s\t%(levelname)s [%(processName)s %(filename)s:%(lineno)s] %(message)s'
    handler.setFormatter(logging.Formatter(format_str))

    e_log = logging.getLogger()
    e_log.setLevel(logging.ERROR)
    e_log.addHandler(handler)

    i_log = logging.getLogger()
    i_log.setLevel(logging.INFO)
    i_log.addHandler(handler)

    ArgumentsParser.parse_arguments()


# always need this to make sure that module was not called from return of submodules
if __name__ == '__main__':
    main()
