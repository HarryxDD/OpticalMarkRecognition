import pandas as pd
import os
import re


path = 'student/'
data = os.listdir(path)

##### ADD DATA INTO DF #####
sheet_list = []
sheet_data = {'Student_ID': [], 'Surname': [], 'Firstname': [], 'Code': []}

for file in data:
    data_name = os.path.splitext(file) # split extension

    sheet_list.append(data_name[0]) # add id_name_code into a list

    filename_parts = data_name[0].split('_') # split id, name, and code
    
    
    # split surname and firstname
    filename_parts[1] = re.sub(r"(\w)([A-Z])", r"\1 \2", filename_parts[1])
    *sur, first = filename_parts[1].split()
    #

    sheet_data['Student_ID'].append(filename_parts[0]) 
    sheet_data['Surname'].append(' '.join(sur))
    sheet_data['Firstname'].append(first)
    sheet_data['Code'].append(filename_parts[2])


df = pd.DataFrame(sheet_data, columns= ['Student_ID', 'Surname', 'Firstname', 'Code'])
df = df.reset_index(drop=True)

# Generate student.csv
df.to_csv('csv_files/student.csv')
