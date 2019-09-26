import sys
import Validator
import argparse



def main( args ):
    v = Validator.Validator()

    if v.isValid(args['xml'], args['xsd']):
        print('Validation successful.')
    v.clear_wrap()
    return


parser = argparse.ArgumentParser(description='XML Validator')
parser.add_argument('xml', help='Path to your xml')
parser.add_argument('xsd', help='Path to your schema FOLDER')
main( vars(parser.parse_args()) )
