import cv2
import numpy as np


############
# FUNCTION #
############

def cells(img):
    rows = np.vsplit(img, 36) 
    cells = []
    for c in rows:
        cols = np.hsplit(c, 5)
        for cell in cols:
            cells.append(cell) 
    return cells


def boxes(cells, count_col, count_row, pixel_array):
    for box in cells:
        pixels = cv2.countNonZero(box) 
        pixel_array[count_row][count_col] = pixels
        count_col += 1
        if count_col == 5:
            count_row += 1
            count_col = 0


def handle_image(img):
    # resize answer image
    img_width = 850
    img_height = 850
    img = cv2.resize(img, (img_width, img_height))

    # region of interest
    roi1 = img[132:816, 150:365]
    roi2 = img[132:816, 532:747]


    ##############
    # ROI HANDLE #
    ##############

    roi1 = cv2.cvtColor(roi1, cv2.COLOR_BGR2GRAY)
    roi2 = cv2.cvtColor(roi2, cv2.COLOR_BGR2GRAY)
    roi1_thresh = cv2.threshold(roi1, 150, 255, cv2.THRESH_BINARY_INV)[1]
    roi2_thresh = cv2.threshold(roi2, 150, 255, cv2.THRESH_BINARY_INV)[1]

    # split image into cells
    cells1 = cells(roi1_thresh)
    cells2 = cells(roi2_thresh)

    # handle cells
    pixel_array1 = np.zeros((72,5))
    boxes(cells1, 0, 0, pixel_array1)
    boxes(cells2, 0, 36, pixel_array1)

    return pixel_array1
    ##

def find_correct_choices(pixel_array, lst):
    
    for x in range(0, 72):
        array = pixel_array[x]
        list_value = np.where(array == np.amax(array)) # finding the correct choices
        lst.append(list_value[0][0]) # adding the choices' position into answer list

    return lst
##