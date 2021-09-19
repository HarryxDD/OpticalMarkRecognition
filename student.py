import cv2
import numpy as np
import answer
import pandas as pd
import student_info

# path = f'student/*.png'
path_array = []
for sheet in range(len(student_info.sheet_list)):
    path_array.append(f'student/{student_info.sheet_list[sheet]}.png')

student_id = []
grading = []
status = []
ans_dict = {}
new_ans_dict = {}
for ques in range(0,72):
    ans_dict[f'{ques}'] = 0
for ques in range(60):
    new_ans_dict[f'{ques}'] = 0

for sheet in range(len(path_array)):

    ##### HANDLE IMAGE #####
    img_width = 850
    img_height = 850
    answer_array = answer.my_answer_list


    img = cv2.imread(path_array[sheet])

    img = cv2.resize(img, (img_width, img_height))


    roi1 = img[132:816, 150:365]
    roi2 = img[132:816, 532:747]

    ###### ROI ######
    roi1 = cv2.cvtColor(roi1, cv2.COLOR_BGR2GRAY)
    roi2 = cv2.cvtColor(roi2, cv2.COLOR_BGR2GRAY)
    roi1_thresh = cv2.threshold(roi1, 150, 255, cv2.THRESH_BINARY_INV)[1]
    roi2_thresh = cv2.threshold(roi2, 150, 255, cv2.THRESH_BINARY_INV)[1]

    cells1 = answer.cells(roi1_thresh)
    cells2 = answer.cells(roi2_thresh)

    pixel_array2 = np.zeros((72,5))
        
    answer.boxes(cells1, 0, 0, pixel_array2)
    answer.boxes(cells2, 0, 36, pixel_array2)
    #################

    ########################


    ##### STUDENT INFO #####
    id = student_info.df.loc[sheet, ['Student_ID']].tolist()
    id = ' '.join(id)
    student_id.append(id)
    ########################

    ##### STUDENT ANSWER #####
    answer_dict = {'0': 'A', '1': 'B', '2':'C', '3':'D', '4':'E'}
    student_answer = []
    answer_letter = []
    for x in range(0, 72):
        array = pixel_array2[x]
        list_value = np.where(array == np.amax(array))
        student_answer.append(list_value[0][0]) 
        
    for x in student_answer:
        answer_letter.append(answer_dict[f'{x}'])
    ###################

    ##### GRADING #####
    count = 0
    check = []
    for x in range(0, 72):
        if answer_array[x] == student_answer[x]:
            check.append(1)
            count += 1
        else: 
            check.append(0)
            ans_dict[f'{x}'] += 1
    count -= 12
    grading.append(count)
    

    # pass/fail
    if count >= 30:
        status.append('Pass')
    else:
        status.append('Fail')

    surname = student_info.df.loc[sheet, ['Surname']].values
    surname = ' '.join(surname)
    firstname = student_info.df.loc[sheet, ['Firstname']].values
    firstname = ' '.join(firstname)

    print(f'So diem cua {surname} {firstname} la {count}/60')
    print(f'Nam cau dau tien la {answer_letter[0:5]}')
    print(f'Toan bo dap an la {answer_letter}')
    
    ###################

##### 3 MOST DIFFICULT #####

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

############################


##### DATAFRAME #####
# grading_data = {'Student_ID': [], 'Grading': [], 'Result': []}
# grading_data['Student_ID'] = student_id
# grading_data['Grading'] = grading
# grading_data['Result'] = status
# grading_df = pd.DataFrame(grading_data, columns=['Student_ID', 'Grading', 'Result'])
# grading_df = grading_df.sort_values(by=['Student_ID'])
# grading_df = grading_df.reset_index(drop=True)
# print(grading_df)

# # Generate grading.csv
# grading_df.to_csv('/home/harry/VNUK/Introduction to CS and Programming/Challenge2/Mark Recognition/grading.csv')
#####################

