try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from urllib import urlopen
import csv
import argparse

def ask_ripe(network,xml_dict):
    # type: (object) -> object
    ripe_net = {}
    url_base='http://rest.db.ripe.net/search?query-string='
    ripe_query= url_base + network
    print('Asking for ',network)
    rep = urlopen(ripe_query)
    data= str(rep.read().decode(encoding='UTF-8'))
    rep.close()
    tree = ET.fromstring(data)
    for l1 in xml_dict:
        for l2 in xml_dict[l1]:
            for elem in tree.iterfind('objects/object[@type="{}"]/attributes/attribute[@name="{}"]'.format(l1,l2)):
                if l1 not in ripe_net.keys():
                    ripe_net.update({l1: {l2: elem.attrib[xml_dict[l1][l2]]}})
                else:
                    if l2 not in ripe_net[l1].keys():
                        ripe_net[l1].update({l2: elem.attrib[xml_dict[l1][l2]]})
                    else:
                        ripe_net[l1][l2] = ripe_net[l1][l2]+','+elem.attrib[xml_dict[l1][l2]]
    return ripe_net


xml_dict = {'inetnum': {'inetnum':'value','status': 'value', 'netname': 'value', 'descr': 'value'},
            'route': {'route': 'value', 'descr': 'value', 'origin': 'value'}}

ripe_db = {}
top_row = ['Network','inetnum','status','netname','descr','route-obj','route-descr','route-origin']

parser = argparse.ArgumentParser()
parser.add_argument("input_file")
parser.add_argument("output_file")
args = parser.parse_args()

with open(args.input_file,'r') as f_in:
    for line in f_in:
        line_str = line.strip()
        ripe_reply = ask_ripe(line_str,xml_dict)
        if ripe_reply is not None:
            ripe_db[line_str] = ripe_reply


with open(args.output_file, 'wb') as csvfile:
    spamwriter = csv.writer(csvfile,delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(top_row)

    for net in ripe_db:
        new_row = [net]
        if 'inetnum' in ripe_db[net].keys():
            if 'inetnum' in ripe_db[net]['inetnum'].keys():
                new_row.append(ripe_db[net]['inetnum']['inetnum'])
            else:
                new_row.append('')
            if 'status' in ripe_db[net]['inetnum'].keys():
                new_row.append(ripe_db[net]['inetnum']['status'])
            else:
                new_row.append('')
            if 'netname' in ripe_db[net]['inetnum'].keys():
                new_row.append(ripe_db[net]['inetnum']['netname'])
            else:
                new_row.append('')
            if 'descr' in ripe_db[net]['inetnum'].keys():
                new_row.append(ripe_db[net]['inetnum']['descr'])
            else:
                new_row.append('')
        else:
            for i in range(2):
                new_row.append('')

        if 'route' in ripe_db[net].keys():
            if 'route' in ripe_db[net]['route'].keys():
                new_row.append(ripe_db[net]['route']['route'])
            else:
                new_row.append('')
            if 'descr' in ripe_db[net]['route'].keys():
                new_row.append(ripe_db[net]['route']['descr'])
            else:
                new_row.append('')
            if 'origin' in ripe_db[net]['route'].keys():
                new_row.append(ripe_db[net]['route']['origin'])
            else:
                new_row.append('')
        else:
            for i in range(2):
                new_row.append('')
        spamwriter.writerow(new_row)



