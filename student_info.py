import pandas as pd
import os
import re


path = '/home/harry/VNUK/Introduction to CS and Programming/Challenge2/Mark Recognition/student/'
data = os.listdir(path)

sheet_list = []
for file in data:
    data_name = os.path.splitext(file)
    sheet_list.append(data_name[0])

sheet_data = {'Student_ID': [], 'Surname': [], 'Firstname': [], 'Code': []}


for filename in sheet_list:
    filename_parts = filename.split('_')
    
    sheet_data['Student_ID'].append(filename_parts[0])

    filename_parts[1] = re.sub(r"(\w)([A-Z])", r"\1 \2", filename_parts[1])
    *sur, first = filename_parts[1].split()
    sur = ' '.join(sur)
    sheet_data['Surname'].append(sur)
    sheet_data['Firstname'].append(first)

    sheet_data['Code'].append(filename_parts[2])


df = pd.DataFrame(sheet_data, columns= ['Student_ID', 'Surname', 'Firstname', 'Code'])
df = df.reset_index(drop=True)

# Generate student.csv
# df.to_csv('/home/harry/VNUK/Introduction to CS and Programming/Challenge2/Mark Recognition/student.csv')

