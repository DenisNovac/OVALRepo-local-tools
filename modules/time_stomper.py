import os
import xml.etree.ElementTree as ET
import sys
import datetime
import argparse
from RecursiveXMLSearcher import RecursiveXMLSearcher

parser = argparse.ArgumentParser(description='This tool will authomatically check the oval_repository field in all definitions. If there is no such field - the tool will add it. New file will be saved in *original-name*-formatted.xml.')
parser.add_argument('path', help='Path to XML with definition')
parser.add_argument('contributor', help='Name of the contributor')
parser.add_argument('organization', help='Name of the contributor\'s organization')

def check_for_timestamps( args ):
    path = args['path']
    contributor = args['contributor']
    organization = args['organization']

    rs = RecursiveXMLSearcher()
    tree = ET.parse(path)
    root = tree.getroot()

    definitions = rs.search_all(root,'definition$')

    print(len(definitions))
    
    is_changed = False
    for d in definitions:
        #print(d[0][0].text)

        is_ov_rep=False
        is_dates=False
        is_subm=False
        is_cont=False

        ov_rep = None
        dates = None
        sumb = None
        cont = None

        ov_rep = rs.search_one(d,'oval_repository$')
        
        if not ov_rep==None:
            is_ov_rep=True
            dates = rs.search_one(ov_rep,'dates$')
            if not dates==None:
                is_dates=True
                subm = rs.search_one(dates,'submitted$')
                if not subm==None:
                    is_subm=True
                    cont = rs.search_one(subm,'contributor$')
                    if not cont==None:
                        is_cont=True
                        #print(d[0][0].text+' is good.')
                    else:
                        print(d[0][0].text+' contributor: FALSE')
                else:
                    print(d[0][0].text+' submitted: FALSE')
            else:
                print(d[0][0].text+' dates: FALSE')
            
        else:
            print(d[0][0].text+' oval_repository: FALSE')


        # now writing changes
        # you need to use ns0: to make sure that output files will be
        # able to get decomposed and composed backwards
        if not is_ov_rep:
            # oval_repository must be in <metadata> tag!
            meta = rs.search_one(d,'metadata$')
            ov_rep = ET.SubElement(meta,'ns0:oval_repository')
        if not is_dates:
            dates = ET.SubElement(ov_rep,'ns0:dates')
        if not is_subm:
            subm = ET.SubElement(dates, 'ns0:submitted')
            today = datetime.datetime.today()
            timestamp = today.strftime('%Y-%m-%dT%H:%M:%S.000+00:00')
            subm.set('date',timestamp)
        if not is_cont:
            cont = ET.SubElement(subm,'ns0:contributor')
            cont.set('organization',organization)
            cont.text=contributor
            is_changed=True

    if is_changed:
        new_name = path.split('.xml')[0]+'-formatted.xml'
        print('Writing changes to '+new_name)
        data = ET.tostring(root)
        with open(new_name,'wb') as file:
            file.write(data)
    else:
        print('All definitions is good. Exiting.')        
    return

check_for_timestamps(vars(parser.parse_args()))