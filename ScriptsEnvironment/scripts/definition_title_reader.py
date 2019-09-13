import os
import re
import xml.etree.ElementTree as ET

def read_title( path ):
    title = None

    tree = ET.parse(path)
    root = tree.getroot()
    # title = root[0][0].text
    for child in root:
        for subchild in child:
            if re.search('title', str(subchild.tag), re.IGNORECASE):
                title = subchild.text
                break
        if title:
            break

    return title
