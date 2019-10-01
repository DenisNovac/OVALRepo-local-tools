"""
    Local OVAL Repository Managment tool.
    It is a wrapper for several OVALRepo modules:
    oval_decomposition.py
    build_oval_definitions_file.py

    And some OVALRepo libs (see ScriptsEnvironment/scripts).

    Allows to run local OVAL repository by creating false git environment for it.

    Author: Denis Yablochkin <denis-yablochkin.ib@yandex.ru>
    
    Copyright: https://github.com/CISecurity/OVALRepo
    Copyright© 2010 United States Government. All Rights Reserved.
"""
import argparse

# import my custom modules
import modules.list_repository as list_repository
import modules.clear_repository as clear_repository
import modules.build_definition as build_definition
import modules.decompose_definition as decompose_definition
import modules.validate_definition as validate_definition
import modules.timestamp_definition as timestamp_definition

def main():
    ''' Main parser with subparsers '''
    main_parser = argparse.ArgumentParser(description='Local OVAL Repository Managment tool.')
    subparsers = main_parser.add_subparsers(title='Main options', help ='Choose one of this options. Help available for each one.')


    ''' Parser for Clear module '''
    parser_clear = subparsers.add_parser('c', help='Clear script environment. Use it if some troubles with building occurs.')
    parser_clear.add_argument('--d', '--decomposed', action='store_true' ,help='Also clear .decomposed folder')
    parser_clear.set_defaults(func=clear_repository.clear_repository)


    ''' Parser for List module'''
    parser_list = subparsers.add_parser('l', help='List entries in repository.')
    parser_list.add_argument('--m', '--mode', choices='adtosv', default='d', help='Output mode: all, definitions, tests, objects, states or variables. Default: only definitions.')
    parser_list.add_argument('--f', '--format', choices='flh', help='Format options: full paths, count files in every category, hide definitions name')
    parser_list.set_defaults(func=list_repository.list_repository)

    ''' Parser for Build module'''
    parser_build = subparsers.add_parser('b', help='Build OVAL definitions from repository.')
    parser_build.add_argument('--o', '--options', default='-h', help='Options for build module. Use "" for options. Pass only \'b\' to see full help from original module.')
    parser_build.set_defaults(func=build_definition.build_definition)


    ''' Parser for Decomposition module'''
    parser_decompose = subparsers.add_parser('d', help='Decompose OVAL definitions to repository. It will replace entries with equal IDs. Use LIST to check IDs. You may specify path to directory and all xmls inside will be decomposed.')
    parser_decompose.add_argument('--r', '--replaces_decomposed', action='store_true', help='Replaces decomposed files to .decomposed folder.')
    parser_decompose.add_argument('--o', '--options', help='Options for build module. Use "" for options. Pass only \'b\' to see full help from original module.')
    parser_decompose.set_defaults(func=decompose_definition.decompose_definition)


    ''' Parser for Validation module'''
    parser_validate = subparsers.add_parser('v', help='Validate OVAL definition with schema.')
    parser_validate.add_argument('xml', help='Path to OVAL definition')
    parser_validate.add_argument('xsd', help='Path to schema FOLDER')
    parser_validate.set_defaults(func=validate_definition.validate_definition)

    '''Parser for timestamp_definition module'''
    #parser = argparse.ArgumentParser(description='This tool will authomatically check the oval_repository field in all definitions. If there is no such field - the tool will add it. New file will be saved in *original-name*-formatted.xml.')
    parser_ts = subparsers.add_parser('t', help='Insert valid <oval_repository> tag with timestamp in OVAL definitions file.')
    parser_ts.add_argument('path', help='Path to XML with definition')
    parser_ts.add_argument('contributor', help='Name of the contributor')
    parser_ts.add_argument('organization', help='Name of the contributor\'s organization')
    parser_ts.set_defaults(func=timestamp_definition.timestamp_definition)

    args = main_parser.parse_args()
    args.func(args)


# always need this to make sure that module was not called from return of submodules
if __name__ == '__main__':
    main()
