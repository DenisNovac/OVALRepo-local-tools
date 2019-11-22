import argparse
import sys

import modules.build_definition as build_definition
import modules.clear_repository as clear_repository
import modules.decompose_definition as decompose_definition
# custom modules
import modules.list_repository as list_repository
import modules.timestamp_definition as timestamp_definition
import modules.validate_definition as validate_definition


class ArgumentsParser:
    """
    Custom parser for arguments.
    Internal modules such as build_definition have their own standard argument parsers so i've decided to
    write my own. I do not see a good way to wrap other argument parsers without writing my own and
    loosing command-line autocomplete.
    """

    @staticmethod
    def parse_arguments():

        # Second argument is always a function name, so it will decide if i use argparse or custom parser.
        # There is no need to use argparse for wrapped modules - they have their own argparse.
        wrapped_modules = ['b', 'd']
        try:
            if sys.argv[1] in wrapped_modules:
                # call wrapped modules directly
                ArgumentsParser.__call_wrapped_modules()
            else:
                # call own parsers first
                ArgumentsParser.__call_argparse()
        except IndexError as e:
            print(e)
            ArgumentsParser.__call_argparse()

        pass

    @staticmethod
    def __call_wrapped_modules():
        """
        This method will be called if user DOES want to use some OVAL Repo modules. These modules already have
        argparse library inside, so we only want to run modules.
        """
        if sys.argv[1] == 'b':
            build_definition.build_definition_cli()
        elif sys.argv[1] == 'd':
            decompose_definition.decompose_definition()
        pass

    @staticmethod
    def __call_argparse():
        """
        This method will be called if user does not tries to use wrapper for decomposition or build.
        We'll need our own argument parsers for this.

        """

        """Main parser with subparsers"""
        main_parser = argparse.ArgumentParser(description='Local OVAL Repository Managment tool.')
        # main_parser.add_argument('-e', '--environment',
        #                         help='Default Script Environment (folder with scripts and repository folder).')
        subparsers = main_parser.add_subparsers(title='Main options',
                                                help='Choose one of this options. Help available for each one.')

        """Parser for Clear module"""
        parser_clear = subparsers.add_parser('c',
                                             help='Clear script environment. Use it if some troubles with building '
                                                  'occurs.')
        parser_clear.add_argument('-d', '--decomposed', action='store_true', help='Also clear .decomposed folder')
        parser_clear.set_defaults(func=clear_repository.clear_repository)

        """ Parser for List module"""
        parser_list = subparsers.add_parser('l', help='List entries in repository.')
        parser_list.add_argument('-m', '--mode', choices='adtosv', default='d',
                                 help='Output mode: all, definitions, tests, objects, states or variables. Default: '
                                      'only definitions.')
        parser_list.add_argument('-f', '--format', choices='flh',
                                 help='Format options: full paths, count files in every category, hide definitions name')
        parser_list.set_defaults(func=list_repository.list_repository)

        """ Parser for Build module"""
        parser_build = subparsers.add_parser('b', help='Build OVAL definitions from repository.')
        parser_build.add_argument('-o', '--options', default='-h',
                                  help='Options for build module. Use "" for options. Pass only \'b\' to see full '
                                       'help from original module.')
        parser_build.set_defaults(func=build_definition.build_definition_cli)

        """ Parser for Decomposition module"""
        parser_decompose = subparsers.add_parser('d',
                                                 help='Decompose OVAL definitions to repository. It will replace '
                                                      'entries with equal IDs. Use LIST to check IDs. You may specify '
                                                      'path to directory and all xmls inside will be decomposed.')
        parser_decompose.add_argument('-r', '--remove_decomposed', action='store_true',
                                      help='Replaces decomposed files to .decomposed folder.')
        parser_decompose.add_argument('-o', '--options',
                                      help='Options for build module. Use "" for options. Pass only \'b\' to see full '
                                           'help from original module.')
        parser_decompose.set_defaults(func=decompose_definition.decompose_definition)

        """ Parser for Validation module"""
        parser_validate = subparsers.add_parser('v', help='Validate OVAL definition with schema.')
        parser_validate.add_argument('xml', help='Path to OVAL definition')
        parser_validate.add_argument('xsd', help='Path to schema FOLDER. Default: version 5.10.1.')
        parser_validate.set_defaults(func=validate_definition.validate_definition)

        """Parser for timestamp_definition module"""
        parser = argparse.ArgumentParser(description='This tool will automatically check the oval_repository field '
                                                     'in all definitions. If there is no such field - the tool will '
                                                     'add it. New file will be saved in '
                                                     '*original-name*-formatted.xml.')
        parser_ts = subparsers.add_parser('t',
                                          help='Insert valid <oval_repository> tag with timestamp in OVAL definitions '
                                               'file.')
        parser_ts.add_argument('path', help='Path to XML with definition')
        parser_ts.add_argument('contributor', help='Name of the contributor')
        parser_ts.add_argument('organization', help='Name of the contributor\'s organization')
        parser_ts.set_defaults(func=timestamp_definition.timestamp_definition)
        args = main_parser.parse_args()
        try:
            args.func(args)
        except AttributeError:
            main_parser.print_help()
