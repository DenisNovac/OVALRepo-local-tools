import os
import xml.etree.ElementTree as ET
import sys
import datetime
from RecursiveXMLSearcher import RecursiveXMLSearcher


def check_for_timestamps( path, contributor, organization ):
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
                print(d[0][0].text+' dates:FALSE')
            
        else:
            print(d[0][0].text+' oval_repository:FALSE')


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
            today = datetime.date.today()
            timestamp = today.strftime('%Y-%m-%dT%H:%M:%S.000+00:00')
            subm.set('date',timestamp)
        if not is_cont:
            cont = ET.SubElement(subm,'ns0:contributor')
            cont.set('organization',organization)
            cont.text=contributor+' with autoformat'
            is_changed=True

    if is_changed:
        print('Writing changes to disk...')
        data = ET.tostring(root)
        with open(path.split('.xml')[0]+'-formatted.xml','wb') as file:
            file.write(data)
            
    return


check_for_timestamps(sys.argv[1], 'Denis Yablochkin', 'USSC')