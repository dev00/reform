import os
import csv
from optparse import OptionParser
from xml.etree import cElementTree as ElementTree

file_ending = 'wsd'
relevant_machines = [
        'Schweissen_FOKO_1',
        'Schweissen_FOKO_2',
        'Schweissen_FOKO_3',
        'Schweissen_FOKO_4']

fieldnames = ['Dateiname', 'Maschine', 'Einsinkweg', 'Spannungsspitzenwert', 'EffekitvSpannungswert', 'Stromwert', 'Schweisszeit', 'Fehler-Code', 'Schweissstation-Nr', 'Schweissprogramm-Nr', 'fortlaufender Schweisszaehler']


parser = OptionParser()
parser.add_option("-s", "--sourcedir", help="folder where the wsd files are stored", default=os.getcwd())
parser.add_option("-o", "--output", help="Where the output should be written to", default=os.path.join(os.getcwd()))

(options, args) = parser.parse_args()

work_path = options.sourcedir
report_file = options.output

# generates a list of all files with a certain ending
# ending is described in file_ending
def file_list(work_path, file_ending):
    wsd_file_list= []
    for file in os.listdir(work_path):
        if file.lower().endswith(file_ending):
            wsd_file_list.append(os.path.join(work_path, file))
    return wsd_file_list

# returns a list of dicts
# each dict represents a line in the csv file
def extract_datasets(xml_file):
    tree = ElementTree.parse(xml_file)
    root = tree.getroot()
    dataset_list = [] 
    for child in root[1]:
        if child.attrib['Maschine'] in relevant_machines:
            dataset = {
                    'Dateiname': os.path.basename(xml_file),
                    'Maschine': child.attrib['Maschine']
                    }

            for value in child[0]:
                if value.get('Value'):
                    dataset.update({ value.get('Name'): value.get('Value')})
               # dataset = {
               #         'Path': os.path.basename(xml_file),
               #         'Maschine': child.attrib['Maschine'],
               #         'Name': value.get('Name', ''),
               #         'Value': value.get('Value', ''),
               #         'bValue': value.get('bValue', ''),
               #         'diValue': value.get('diValue', ''),
               #         'Min': value.get('Min', ''),
               #         'Max': value.get('Max', ''),
               #         }
               # dataset_list.append(dataset)
            dataset_list.append(dataset)
    return dataset_list

records = []

for file in file_list(work_path, file_ending):
    # append new records to the old ones
    records += extract_datasets(file)

# write all


#fieldnames = records[0].keys()

print(records[0])
print(records[1])
print(fieldnames)

with open(os.path.join(report_file, 'report.csv'), 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for record in records:
        writer.writerow(record)

for machine in relevant_machines:
    with open(os.path.join(report_file, (machine+'.csv')), 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            if record.get('Maschine') == machine:
                writer.writerow(record)


        
