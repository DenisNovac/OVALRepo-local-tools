import os
import re
import logging
import xml.etree.ElementTree as ET

from lxml import etree

from modules.submodules.RecursiveXMLSearcher import RecursiveXMLSearcher


class Validator:
    WRAPPER_NAME = '__generated_wrapper.xsd'
    WRAPPER_PATH = ''
    DEFAULT_NAMESPACE = 'http://oval.mitre.org/XMLSchema/oval-definitions-5'
    DEFAULT_ENCODING = 'UTF-8'
    ERR_MESSAGE = ""

    def __init__(self):
        """
        Initialize loggers
        """
        self.e_log = logging.getLogger()
        self.e_log.setLevel(logging.ERROR)
        self.i_log = logging.getLogger()
        self.i_log.setLevel(logging.INFO)

    def validate(self, xml_path, xsd_path) -> tuple:
        """
        Main validation method. It will try to validate OVAL definition xml file through schema files in specified
        folder. Used schemas (such as specific for Windows) will be concatenated to one "Wrapper" file wich will be
        used for validation.

        :param xml_path: OVAL definition file for validation
        :param xsd_path: Folder with XML schemas for validation
        :return: tuple CODE, RESULT (if code is -1 the result is error message)
        """
        if not os.path.isdir(xsd_path):
            self.ERR_MESSAGE = f'xsd_path must refer to FOLDER with OVAL schemas but {xsd_path} provided.'
            self.e_log.error(self.ERR_MESSAGE)
            return -1, self.ERR_MESSAGE

        self.check_schema_version(xsd_path)
        self.check_definition_version(xml_path)

        # getting one schema from importing needed in one file
        wrapper_path = self.wrap_schema(xml_path, xsd_path)
        if not wrapper_path[0] == 0:
            self.ERR_MESSAGE = 'Unable to get wrapper for schema.'
            return -1, self.ERR_MESSAGE

        # this variable is needed to delete wrapper afterwards
        wrapper_path = wrapper_path[1]
        self.WRAPPER_PATH = wrapper_path

        # parsing xmls
        try:
            xsd_parsed = etree.parse(wrapper_path)
            xsd = etree.XMLSchema(xsd_parsed)
            xml_doc = etree.parse(xml_path)
        except OSError as e:
            self.ERR_MESSAGE = f'Error reading file {e}'
            self.e_log.error(self.ERR_MESSAGE)
            return -1, self.ERR_MESSAGE

        # validation and error processing
        try:
            self.i_log.info('Validation starting...')
            xsd.assertValid(xml_doc)
        except etree.DocumentInvalid as e:
            self.ERR_MESSAGE = f'Validation error: {e}'

            if re.search('No match found for key-sequence', str(e)):
                element = re.split('No match found for key-sequence', str(e))[1]
                element = re.split('of keyref', element)[0]
                element = element.replace('[\'', '').replace('\']', '')

                self.ERR_MESSAGE += f'\n Perhaps, element refers to ID that is not exists. Check existence of element '\
                                    f'with ID  {element.strip()} '

            elif re.search('This element is not expected', str(e)):

                self.ERR_MESSAGE += f'\nPerhaps, given element is not defined in schema of your version or you ' \
                                    f'misplaced some elements. The right order: definitions, tests, objects, states, '\
                                    f'variables. Check new version of schemas on CISecurity: ' \
                                    f'https://github.com/CISecurity/OVAL '

            elif re.search('not an element of the set', str(e)):
                attr = re.search(r'attribute \'(\w*)', str(e)).group(1)
                elem = re.search(r'The value \'(\w*)\' is not an element of the set', str(e)).group(1)
                self.ERR_MESSAGE += f'\nThere is no {attr} = {elem}  in your schema. Perhaps, given element is not ' \
                                    'defined in schema of your version. Check new version of schemas on CISecurity: ' \
                                    'https://github.com/CISecurity/OVAL '

            else:
                self.ERR_MESSAGE += '\nThere is no additional info on this error.'

            for m in self.ERR_MESSAGE.split('\n'):
                self.e_log.error(m)
            return -1, self.ERR_MESSAGE

        self.i_log.info('Validation successful')
        return 0, ''

    def wrap_schema(self, xml_path, xsd_path) -> tuple:
        """
        This method will check used OVAL xml namespaces in definition and then concatenate appropriate schema
        files in one "Wrapper" file.

        :param xml_path: OVAL definition file for validation
        :param xsd_path: Folder with XML schemas for validation
        :return: tuple CODE, RESULT (if code is -1 the result is error message)
        """

        # checking namespaces used in OVAL xml config
        schema_namespaces = self.check_namespaces(xml_path)

        if not schema_namespaces[0] == 0:
            self.e_log.error('Error occurred while checking schema namespaces')
            return -1, self.ERR_MESSAGE
        schema_namespaces = schema_namespaces[1]
        self.i_log.info('Imported namespaces: ' + str(schema_namespaces))

        # generate wrapper with those namespaces
        wrapper_path = self.generate_wrapper(xsd_path, schema_namespaces)
        if not wrapper_path[0] == 0:
            self.e_log.error('Unable to get wrapper path, cancelling creation of wrapper file')
            return -1, self.ERR_MESSAGE

        wrapper_path = wrapper_path[1]
        self.i_log.info('Generated wrapper for imported namespaces.')

        return 0, wrapper_path

    def check_namespaces(self, xml_path) -> tuple:
        """
        Check used namespaces in OVAL definition.

        :param xml_path: OVAL definition with some namespaces.
        :return: tuple CODE, RESULT (if code is -1 the result is error message)
        """
        schema_namespaces = []
        self.i_log.info('Checking for imported namespaces in definition...')

        with open(xml_path, 'r', encoding=self.DEFAULT_ENCODING) as file:
            for line in file:
                # do not process line without namespace
                if 'xmlns' not in line:
                    continue

                # one line can contain more than one namespace
                words = line.split(' ')
                for word in words:
                    # cut namespace name from line (excluding oval-namespaces)
                    regex = re.compile(r'xmlns.*="' + self.DEFAULT_NAMESPACE + r'#')
                    split = re.split(regex, word)
                    # if that was not oval namespace, process it
                    if split:
                        try:
                            # cut last part (something like ">)
                            ns_name = split[1].split('"')[0]
                            schema_namespaces.append(ns_name)
                        except IndexError:
                            # there will be A LOT of exceptions for IndexError
                            pass
                        except Exception as e:
                            self.ERR_MESSAGE = 'Exception occurred while checking imported namespaces: ' + str(e)
                            self.e_log.error(self.ERR_MESSAGE)
                            return -1, self.ERR_MESSAGE

        schema_namespaces = list(set(schema_namespaces))
        return 0, schema_namespaces

    def generate_wrapper(self, xsd_path, schema_namespaces) -> tuple:
        """
        Method for actually creating the "Wrapper" file. It takes path to schema folder and list of namespaces to
        create one file with all those namespaces which will be used for validation afterwars.

        :param xsd_path: Schema folder
        :param schema_namespaces: List of namespaces
        :return: tuple CODE, RESULT (if code is -1 the result is error message)
        """
        # check if path specified without / at the end
        regex = re.compile(os.sep + r'$')
        if re.search(regex, xsd_path):
            wrapper_path = os.path.abspath(xsd_path + self.WRAPPER_NAME)
        else:
            wrapper_path = os.path.abspath(xsd_path + os.sep + self.WRAPPER_NAME)

        # list of schemas file in directory
        schemas = os.listdir(xsd_path)

        # checking if we have all needed schemas in folder
        for needed_schema in schema_namespaces:
            namespace_exists = False
            for schema in schemas:
                ns = schema.split('-')[0]
                if needed_schema == ns:
                    namespace_exists = True
            if not namespace_exists:
                self.ERR_MESSAGE = f"ERROR COLLECTING SCHEMAS: Schema for namespace {needed_schema} does not exists. " \
                                   f"Perhaps, given element is not defined in schema of your version. Check new " \
                                   f"version of OVAL schemas on CISecurity: https://github.com/CISecurity/OVAL "
                self.e_log.error(self.ERR_MESSAGE)
                return -1, self.ERR_MESSAGE

        # wrapping all needed schemas in one XSD file with multiple imports
        with open(wrapper_path, 'w') as file:
            # header
            file.write(
                '<?xml version="1.0" encoding="UTF-8"?>\n<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema">\n')

            for schema in schemas:
                # don't let wrapper to import itself
                if schema == self.WRAPPER_NAME:
                    continue
                # import all common oval schemas (starts with oval-)
                if re.match(r'oval-', schema):
                    pass
                # check if this namespace was used in definition
                else:
                    to_import = False
                    for used_schema in schema_namespaces:
                        if re.match(used_schema + '-', schema):
                            to_import = True
                            break
                    if not to_import:
                        continue  # this will continue outer FOR (schema in schemas)
                family = ''
                if not re.match(r'^oval-', schema):  # if this is not common oval namespace then change namespace
                    family = '#' + str(schema.split('-')[0])

                import_line = f'<xsd:import namespace="{self.DEFAULT_NAMESPACE + family}" schemaLocation="{schema}"/>\n'
                file.write(import_line)
            # header closed
            file.write('</xsd:schema>')

        return 0, wrapper_path

    def clear_wrapper(self) -> None:
        """
        Delete wrapper file used for validation.
        """
        try:
            os.remove(os.path.relpath(self.WRAPPER_PATH))
            self.i_log.info('Removed wrapper file ' + self.WRAPPER_PATH)
        except Exception as e:
            self.e_log.error('Error deleting wrapper file: '+str(e))

    def check_schema_version(self, xsd_path) -> None:
        """
        Check OVAL schema's version. It will find the file oval-definitions-schema and search it
        for version line. Apparently, this version is a version for all schemas files in
        specified schema folder.
        It will print version in logs.

        :param xsd_path: schema folder
        """
        path = xsd_path
        regex = re.compile(r'.*' + os.sep + os.sep + '$')
        if re.search(regex, path):
            path = path + 'oval-definitions-schema.xsd'
        else:
            path = path + os.sep + 'oval-definitions-schema.xsd'
        try:
            rs = RecursiveXMLSearcher()
            tree = ET.parse(path)
            root = tree.getroot()
            v = rs.search_one(root, 'version')
            self.i_log.info("Found schema version " + v.text)
        except Exception as e:
            self.e_log.error('Unable to check schema version: ' + str(e))

    def check_definition_version(self, xml_path) -> None:
        """
        Check OVAL definition's schema version. It will check version specified in generator tag.
        It will print version in logs.

        :param xml_path: OVAL definition file
        """
        try:
            rs = RecursiveXMLSearcher()
            tree = ET.parse(xml_path)
            root = tree.getroot()
            v = rs.search_one(root, 'generator')
            v = rs.search_one(v, 'schema_version')
            self.i_log.info("Found definition version " + v.text)
        except Exception as e:
            self.e_log.error('Unable to check definition version: ' + str(e))
