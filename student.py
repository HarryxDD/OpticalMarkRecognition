import cv2
import numpy as np
from answer import my_answer_list
import my_function
import pandas as pd
import student_info


path_array = []
for sheet in range(len(student_info.sheet_list)):
    path_array.append(f'student/{student_info.sheet_list[sheet]}.png') # adding paths into an array


# lists and dicts
student_id = []
grading = []
status = []
ans_dict = {}
answer_array = my_answer_list
new_ans_dict = {}
for ques in range(0,72):
    ans_dict[f'{ques}'] = 0
for ques in range(60):
    new_ans_dict[f'{ques}'] = 0

# input 1 student id to get his/her answer
input_id = int(input("Input student ID: "))

for sheet in range(len(path_array)):
    img = cv2.imread(path_array[sheet]) # read image
    pixel_array2 = my_function.handle_image(img) # handle image


    # getting student id
    id = student_info.df.loc[sheet, ['Student_ID']].tolist()
    id = ' '.join(id)
    student_id.append(id) # adding IDs into a list


    # handle students' answer
    answer_dict = {'0': 'A', '1': 'B', '2':'C', '3':'D', '4':'E'}
    student_answer = []
    answer_letter = []
    my_function.find_correct_choices(pixel_array2, student_answer)

    for x in student_answer: 
        answer_letter.append(answer_dict[f'{x}']) # convert number to letter


    # grading
    count = 0
    check = []
    for x in range(0, 72):
        if answer_array[x] == student_answer[x]:
            check.append(1)
            count += 1
        else: 
            check.append(0)
            ans_dict[f'{x}'] += 1 # the number of students choosing the wrong answer
    count -= 12
    grading.append(count)


    # pass/fail
    if count >= 30:
        status.append('Pass')
    else:
        status.append('Fail')


    # print first 5 and all answers of students
    surname = ' '.join(student_info.df.loc[sheet, ['Surname']].values) 
    firstname = ' '.join(student_info.df.loc[sheet, ['Firstname']].values)

    if id == f'{input_id}':
        print(f'So diem cua {surname} {firstname} la {count}/60')
        print(f'Nam cau dau tien la {answer_letter[0:5]}')
        print(f'Toan bo dap an la {answer_letter}')


# finding 3 most difficult ques
count_ques = 0
for ques in list(ans_dict):
    count_ques += 1
    if count_ques == 6: 
        ans_dict.pop(f'{ques}', None) 
        count_ques -= 6

num = 0
for ques in list(ans_dict):
    new_ans_dict[f'{num}'] = ans_dict[f'{ques}']
    num += 1

sort_ans_dict = sorted(new_ans_dict.items(), key=lambda x:x[1], reverse=True)
print(f'3 cau kho nhat la: {int(sort_ans_dict[0][0]) + 1}, {int(sort_ans_dict[1][0]) + 1}, {int(sort_ans_dict[2][0]) + 1}')



#############
# DATAFRAME #
#############
grading_data = {'Student_ID': [], 'Grading': [], 'Result': []}
grading_data['Student_ID'] = student_id
grading_data['Grading'] = grading
grading_data['Result'] = status
grading_df = pd.DataFrame(grading_data, columns=['Student_ID', 'Grading', 'Result'])
grading_df = grading_df.sort_values(by=['Student_ID'])
grading_df = grading_df.reset_index(drop=True)

grading_df.to_csv('csv_files/grading.csv') # generating grading.csv


##
