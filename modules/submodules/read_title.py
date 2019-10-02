import re
import xml.etree.ElementTree as ET
from modules.submodules.RecursiveXMLSearcher import RecursiveXMLSearcher

def read_title( path, add_reference=False ):
    title = None
    reference = None
 
    tree = ET.parse(path)
    root = tree.getroot()

    rs = RecursiveXMLSearcher()

    result = rs.search_all(root, 'reference|title')
    for r in result:
        if re.search('title', r.tag):
            title=r.text
        if re.search('reference', r.tag):
            reference=r.attrib['ref_id']
    if add_reference and reference and title:
        title = title+'\t'+reference

    return title