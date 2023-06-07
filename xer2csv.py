import os
import csv

# Define the path to the .xer file
xer_file = '<XER file path>.xer'
xer_file_name = os.path.splitext(os.path.basename(xer_file))[0]
folder_name = xer_file_name

if not os.path.exists(folder_name):
    os.makedirs(folder_name)

with open(xer_file, 'r', encoding='latin-1') as f:
    lines = f.readlines()

table_name = None
fields = None
rows = []

for line in lines:
    if line.startswith('%T'):
        if table_name:
            with open(os.path.join(folder_name, table_name + '.csv'), 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
                for row in rows:
                    writer.writerow(row)
            fields = None
            rows = []
        table_name = line.strip().split('\t')[1]
    elif line.startswith('%F'):
        fields = line.strip().split('\t')[1:]
    elif line.startswith('%R'):
        rows.append(line.strip().split('\t')[1:])
    else:
        continue