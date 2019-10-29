from lxml import etree
import xml.etree.ElementTree as ET
import re, os
from modules.submodules.RecursiveXMLSearcher import RecursiveXMLSearcher
class Validator:
    
    WRAPPER_NAME = '__generated_wrapper.xsd'

    WRAPPER_PATH = ''

    # validation method
    def isValid(self, xml_path, xsd_path) :
        if not os.path.isdir(xsd_path):
            print('ERROR:')
            print('xsd_path must refer to FOLDER with xsd schemas')
            print('Schemas from CISecurity: https://github.com/CISecurity/OVAL')
            return False
        
        
        print('Getting version of schema...')
        version = self.check_version(xsd_path)
        if version:
            print('Version '+version+' found.')

        # getting one schema from importing needed in one file
        wrapper_path = self.__wrap(xml_path, xsd_path)
        if not wrapper_path:
            return False

        xsd = None
        xml_doc = None
        try:
            xsd_parsed = etree.parse(wrapper_path)
            xsd = etree.XMLSchema(xsd_parsed)
            xml_doc = etree.parse(xml_path)
        except OSError as e:
            if re.search('Error reading file', str(e)):
                print('Error reading file. File may not exist.')
            else:
                print(str(e))
            return
        
        # validation and error processing
        try:
            print('Validation starting...')
            xsd.assertValid(xml_doc)
        except etree.DocumentInvalid as e:
            print('\nVALIDATION ERROR')
            print(str(e)+'\n')
            print('Additional info:')
            if re.search('No match found for key-sequence', str(e)):
                print('Perhaps, element refers to ID that is not exists.')
                element = re.split('No match found for key-sequence', str(e))[1]
                element = re.split('of keyref', element)[0]
                element = element.replace('[\'','').replace('\']','')
                print('Check existence of element with ID '+element.strip()+'.')

            elif re.search('This element is not expected', str(e)):
                print('Perhaps, given element is not defined in schema of your version or you misplaced some elements. The right order: definitions, tests, objects, states, variables.')
                print('Check new version of schemas on CISecurity: https://github.com/CISecurity/OVAL')

            elif re.search('not an element of the set', str(e)):
                attr = re.search('attribute \'(\w*)',str(e)).group(1)
                elem = re.search('The value \'(\w*)\' is not an element of the set',str(e)).group(1)
                
                print('There is no '+attr+' = '+elem +' in your schema.')
                print('Perhaps, given element is not defined in schema of your version.')
                print('Check new version of schemas on CISecurity: https://github.com/CISecurity/OVAL')

            else:
                print('There is no additional info for this error.')
            print()
            return False
        
        return True



    # this method will create file with imports of needed schemas
    def __wrap ( self, xml_path, xsd_path ):
        namespace='http://oval.mitre.org/XMLSchema/oval-definitions-5'

        
        wrapper_path = None
        if re.search(os.sep+'$', xsd_path):
            wrapper_path = os.path.abspath(xsd_path+self.WRAPPER_NAME)
        else:
            wrapper_path = os.path.abspath(xsd_path+os.sep+self.WRAPPER_NAME)
        self.WRAPPER_PATH=wrapper_path


        # checking namespaces used in OVAL xml config
        needed_schemas = [ ]
        print('Checking for imported namespaces in definition...')
        # sometimes you have to change encoding here
        with open(xml_path, 'r', encoding='utf-8') as file:
            for line in file:
                # do not process line without namespace
                if not re.search('xmlns',line):
                    continue
                
                # one line can contain more than one namepsace
                words = line.split(' ')
                for word in words:
                    # cut namespace name from line (excluding oval-namespaces)
                    split = re.split('xmlns.*="'+namespace+'#', word)
                    # if that was not oval namespace, process it
                    if split:
                        try:
                            # cut last part (something like ">)
                            ns_name = split[1].split('"')[0]
                            needed_schemas.append(ns_name)    
                        except Exception:
                            pass

        needed_schemas = list(set(needed_schemas))
        print('Imported namespaces: '+str(needed_schemas))
    
        # schemas in directory
        schemas = os.listdir(xsd_path)

        # checking if we have all needed schemas in folder
        for needed_schema in needed_schemas:
            isNamespaceExists=False
            for schema in schemas:
                ns = re.split('-', schema)[0]
                if needed_schema == ns:
                    isNamespaceExists=True
            if not isNamespaceExists:
                print('\nERROR COLLECTING SCHEMAS')
                print('Schema for namespace '+needed_schema+' not exists.')
                print('Perhaps, given element is not defined in schema of your version.')
                print('Check new version of OVAL schemas on CISecurity: https://github.com/CISecurity/OVAL')
                return None

        # wrapping all needed schemas in one XSD file with multiple imports
        with open(wrapper_path,'w') as file:
            # header
            file.write('<?xml version="1.0" encoding="UTF-8"?>\n<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema">\n')
            
            for schema in schemas:
                # dont import wrapper in wrapper
                if schema == self.WRAPPER_NAME:
                    continue
                # import all common oval schemas
                if re.match('oval-', schema):
                    pass
                # check if this schema needed for import
                else:
                    isNeeded = False
                    for needed_schema in needed_schemas:
                        if re.match(needed_schema+'-', schema):
                           isNeeded = True
                    if not isNeeded:
                        continue
                
                
                # if this is not common oval namespace then change namespace
                family=''
                if not re.match('^oval-', schema):
                    family = '#'+re.split('-', schema)[0]
                file.write('<xsd:import namespace="'+namespace+family+'" schemaLocation="'+schema+'"/>\n')

            # header closed
            file.write('</xsd:schema>')
        return wrapper_path


    # deletes file from schemas folder
    def clear_wrapper( self ):
        try:
            os.remove(os.path.relpath(self.WRAPPER_PATH))
            print('Removed ' + self.WRAPPER_PATH)
        except Exception as e:
            print(str(e))
        return

    
    def check_version( self, xsd_path ):
        path = xsd_path
        if re.search('.*'+os.sep+os.sep+'$', path):
            path = path+'oval-definitions-schema.xsd'
        else:
            path = path+os.sep+'oval-definitions-schema.xsd'
        try:
            rs = RecursiveXMLSearcher()
            tree = ET.parse(path)
            root = tree.getroot()
            v = rs.search_one(root,'version')
            return v.text
        except Exception as e:
            print('Unable to check version! Folder with schema may be corrupted. Error: '+str(e))
            return None        