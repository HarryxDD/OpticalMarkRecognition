import cv2
import numpy as np
import my_function

# read answer
path = 'answer/3A.png'
img = cv2.imread(path)

###############
# ANSWER LIST #
###############

my_answer_list = []
pixel_array1 = my_function.handle_image(img)
my_function.find_correct_choices(pixel_array1, my_answer_list)

##
