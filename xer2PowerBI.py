import os
import csv
import pandas as pd

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

# Iterate through all the .csv files in the folder_name directory
# and assign the resulting dataframe to a variable named after the table.
for f in os.listdir(folder_name):
    if f.endswith('.csv'):
        table_name = os.path.splitext(f)[0]
        vars()[table_name] = pd.read_csv(os.path.join(folder_name, f))