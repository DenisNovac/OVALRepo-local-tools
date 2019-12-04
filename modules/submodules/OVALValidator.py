import os
import re
import logging
import xml.etree.ElementTree as ET

from lxml import etree

from modules.submodules.RecursiveXMLSearcher import RecursiveXMLSearcher


class OVALValidator:
    """
    OVAL Validator - is a module that validates OVAL XML content through OVAL Schemes. It uses "wrapper" method to
    validate through OVAL Schemas: most of the time it is necessary to validate OVAL-content through several schemas.
    Module will "Wrap" them in one file - create file with imports of needed files and then validate OVAL content
    through this wrapper.
    """

    WRAPPER_NAME = '__generated_wrapper.xsd'
    WRAPPER_PATH = ''
    DEFAULT_ENCODING = 'UTF-8'

    def __init__(self, error_file=None):
        """
        Initialize loggers
        """
        self.e_log = logging.getLogger('Validator_info')
        self.e_log.setLevel(logging.ERROR)
        self.i_log = logging.getLogger('Validator_error')
        self.i_log.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        format_str = '%(asctime)s\t%(levelname)s [%(processName)s %(filename)s:%(lineno)s] %(message)s'
        formatter = logging.Formatter(format_str)
        handler.setFormatter(formatter)
        self.e_log.addHandler(handler)
        self.i_log.addHandler(handler)
        if error_file:
            fh = logging.FileHandler(error_file)
            fh.setFormatter(formatter)
            self.e_log.addHandler(fh)

    def validate(self, xml_path, xsd_path) -> bool:
        """
        Main validation method. It will try to validate OVAL definition xml file through schema files in specified
        folder. Used schemas (such as specific for Windows) will be concatenated to one "Wrapper" file wich will be
        used for validation.

        :param xml_path: OVAL definition file for validation
        :param xsd_path: Folder with XML schemas for validation
        :return: result of validation
        """
        if not os.path.isdir(xsd_path):
            err_message = f'xsd_path must refer to FOLDER with OVAL schemas but {xsd_path} provided.'
            self.e_log.error(err_message)
            raise Exception(err_message)

        self.check_schema_version(xsd_path)
        self.check_content_version(xml_path)

        # getting one schema from importing needed in one file
        wrapper_path = self.wrap_schema(xml_path, xsd_path)
        self.i_log.info(f'Wrapper path acquired: {wrapper_path}')

        # this variable is needed to delete wrapper afterwards
        self.WRAPPER_PATH = wrapper_path

        # parsing definition and schema
        try:
            xsd_parsed = etree.parse(wrapper_path)
            xsd = etree.XMLSchema(xsd_parsed)
            xml_doc = etree.parse(xml_path)
        except OSError as e:
            err_message = f'Error reading file {e}'
            self.e_log.error(err_message)
            raise Exception(err_message)

        # validation and error processing
        try:
            self.i_log.info('Validation starting...')
            xsd.assertValid(xml_doc)
        except etree.DocumentInvalid as e:
            err_message = f'Validation failure for {xml_path}: {e}'

            if re.search('No match found for key-sequence', str(e)):
                element = re.split('No match found for key-sequence', str(e))[1]
                element = re.split('of keyref', element)[0]
                element = element.replace('[\'', '').replace('\']', '')
                err_message += f'  (Perhaps, element refers to ID that is not exists. Check existence of element ' \
                               f'with ID  {element.strip()})'

            elif re.search('This element is not expected', str(e)):
                err_message += f'  (Perhaps, given element is not defined in schema of your version or you ' \
                               f'misplaced some elements. The right order: definitions, tests, objects, states, ' \
                               f'variables. Check new version of schemas on CISecurity: ' \
                               f'https://github.com/CISecurity/OVAL)'

            elif re.search('not an element of the set', str(e)):
                attr = re.search(r'attribute \'(\w*)', str(e)).group(1)
                elem = re.search(r'The value \'(\w*)\' is not an element of the set', str(e)).group(1)
                err_message += f'  (There is no {attr} = {elem}  in your schema. Perhaps, given element is not ' \
                               'defined in schema of your version. Check new version of schemas on CISecurity: ' \
                               'https://github.com/CISecurity/OVAL)'
            else:
                err_message += '  (There is no additional info on this error.)'

            self.e_log.error(err_message)
            # warning for WONTFIX bug:
            # https://bugzilla.gnome.org/show_bug.cgi?id=325533
            # https://bugs.launchpad.net/lxml/+bug/674775
            # https://stackoverflow.com/questions/19826050/is-it-possible-to-show-line-numbers-more-than-65535-when-you-validate-an-xml-fil
            if '65535' in str(e):
                self.e_log.error('Be cautious: line number 65535 is incorrect - usually it is > 65535. See bug of libxml2: https://bugzilla.gnome.org/show_bug.cgi?id=325533')
            return False
        self.i_log.info('Validation successful')
        return True

    def wrap_schema(self, xml_path, xsd_path) -> os.path:
        """
        This method will check used OVAL xml namespaces in definition and then concatenate appropriate schema
        files in one "Wrapper" file.

        :param xml_path: OVAL definition file for validation
        :param xsd_path: Folder with XML schemas for validation
        :return: path to wrapper
        """

        # checking namespaces used in OVAL xml config
        schema_namespaces = self.check_namespaces(xml_path)
        self.i_log.info('Imported namespaces: ' + str(schema_namespaces))

        # generate wrapper with those namespaces
        wrapper_path = self.generate_wrapper(xsd_path, schema_namespaces)
        self.i_log.info('Generated wrapper for imported namespaces.')
        return wrapper_path

    def check_namespaces(self, xml_path) -> list:
        """
        Check used namespaces in OVAL definition.

        :param xml_path: OVAL definition with some namespaces.
        :return: namespaces used in definition
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
                    # namespaces such as windows/independent/linux may be only in definitions, results or syschar files
                    regex = re.compile(r'xmlns.*="http://oval.mitre.org/XMLSchema/oval-'
                                       r'(definitions|results|system-characteristics)-5#')
                    if re.search(regex, word):
                        split = word.split('#')
                        try:
                            # cut last part (something like ">)
                            ns_name = split[-1].split('"')[0]
                            schema_namespaces.append(ns_name)
                        except IndexError as e:
                            self.e_log.error(e)
                            # there will be A LOT of exceptions for IndexError
                            pass
                        except Exception as e:
                            err_message = 'Exception occurred while checking imported namespaces: ' + str(e)
                            self.e_log.error(err_message)
                            raise Exception(err_message)

        schema_namespaces = list(set(schema_namespaces))
        return schema_namespaces

    def generate_wrapper(self, xsd_path, schema_namespaces) -> os.path:
        """
        Method for actually creating the "Wrapper" file. It takes path to schema folder and list of namespaces to
        create one file with all those namespaces which will be used for validation afterwars.

        :param xsd_path: Schema folder
        :param schema_namespaces: List of namespaces
        :return: path to the wrapper
        """
        # check if path specified without / at the end
        regex = re.compile(os.sep + r'$')
        if re.search(regex, xsd_path):
            wrapper_path = os.path.relpath(xsd_path + self.WRAPPER_NAME)
        else:
            wrapper_path = os.path.relpath(xsd_path + os.sep + self.WRAPPER_NAME)

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
                err_message = f"ERROR COLLECTING SCHEMAS: Schema for namespace {needed_schema} does not exists. " \
                              f"Perhaps, given element is not defined in schema of your version. Check new " \
                              f"version of OVAL schemas on CISecurity: https://github.com/CISecurity/OVAL "
                self.e_log.error(err_message)
                raise Exception(err_message)

        # wrapping all needed schemas in one XSD file with multiple imports
        with open(wrapper_path, 'w') as file:
            # header
            file.write(
                '<?xml version="1.0" encoding="UTF-8"?>\n<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema">\n')
            

            for schema in schemas:
                # don't let wrapper to import itself
                if schema == self.WRAPPER_NAME:
                    continue
                if 'xsl' in schema:  # do not take schematrons in imports
                    continue
                # xmldsig originally was placed in OpenSCAP outside of folder with OVAL schemas 5.10.1
                if 'xmldsig' in schema:  
                    file.write(
                        '<xsd:import namespace="http://www.w3.org/2000/09/xmldsig#" schemaLocation="xmldsig-core-schema.xsd"/>'
                    )
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

                # types of oval schemas are specified in names
                oval_type = re.search(
                    r'(?P<type>(definitions|results|system-characteristics|common|directives|variables))', schema)

                oval_type = oval_type.group('type')
                namespace = f'http://oval.mitre.org/XMLSchema/oval-{oval_type}-5'
                import_line = f'<xsd:import namespace="{namespace + family}" schemaLocation="{schema}"/>\n'
                file.write(import_line)
            # header closed
            file.write('</xsd:schema>')

        return wrapper_path

    def clear_wrapper(self) -> None:
        """
        Delete wrapper file used for validation.
        """
        try:
            os.remove(os.path.relpath(self.WRAPPER_PATH))
            self.i_log.info('Removed wrapper file ' + self.WRAPPER_PATH)
        except Exception as e:
            self.e_log.error('Error occurred while removing wrapper file: ' + str(e))

    """
    This is "decorative"-only methods. Outputs from them should never be used to stop validations.
    """

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
            self.i_log.info("Found OVAL schema version " + v.text)
        except Exception as e:
            self.e_log.error('Unable to check schema version: ' + str(e))

    def check_content_version(self, xml_path) -> None:
        """
        Check OVAL definition's schema version. It will check version specified in generator tag.
        It will print version in logs.

        :param xml_path: OVAL definition file
        """
        try:
            rs = RecursiveXMLSearcher()
            tree = ET.parse(xml_path)
            root = tree.getroot()

            content = 'OVAL content'
            content_name = re.search(r'(?P<content>(definitions|results|system-characteristics))', str(root))
            if content_name:
                content = 'OVAL '+content_name.group('content')

            v = rs.search_one(root, 'generator')
            v = rs.search_one(v, 'schema_version')
            self.i_log.info(f"Found {content} version " + v.text)
        except Exception as e:
            self.e_log.error('Unable to check definition version: ' + str(e))
