# openCV_Histogram-Contour-Template.py
"""
BGR2GRAY --> thresholdBackground --> Histogram --> 
Resize --> bilateralFilter --> CannyEdge --> 
findContour --> matchShapes --> 
boundingRect --> rectangle --> putText
@author: Yen 
"""


import numpy as np
import cv2
import os
from matplotlib import pyplot as plt



# Image Resize
def image_resize(image, set_value_Width = 375):
    set_value_W = set_value_Width
    height, width = image.shape[0:2]
    ratio_H_div_W = height / width
    calc_value_H = round(set_value_W * ratio_H_div_W)
    img_resize = cv2.resize(image, ( set_value_W,calc_value_H ), interpolation = cv2.INTER_AREA ) #(Withd,Height); (fx horizontal, fy vertical)
    return img_resize


# Plot Image with Histogram 
def showImageHistogram_inRange_Gray(image, lower=0, upper=255): # Gray Value 0 and 255 will be Omitted
    print('working on showImageHistogram_inRange_Gray....................')
    hist = cv2.calcHist([image], channels=[0], mask=None, histSize=[256], ranges=[0,256]) 
    # print Image & Histogram
    plt.subplot(211), plt.imshow(image, 'gray')
    plt.subplot(212), plt.plot(hist[lower+1:upper])
    plt.show()
    # target graycolor Index & Intensity for next step analysis
    target_graycolor_histogram = []
    threshold_5pct = image.shape[0]*0.05 * image.shape[1]*0.05 # 0.03 will work for small triangle image
    print('threshold_5%_intensity = ' +str(threshold_5pct))
    for graycolor_Index, graycolor_Intensity in enumerate(hist):
        if lower < graycolor_Index < upper and graycolor_Intensity > threshold_5pct:
            target_graycolor_histogram.append((graycolor_Index,int(graycolor_Intensity)))
            print('graycolor_Index = ' +str(graycolor_Index)+ ', graycolor_Intensity = ' +str(graycolor_Intensity))
    return target_graycolor_histogram


# Contours : curve joining all the continuous points (along the boundary), having same color
def image_Contour(image, graycolor_value):
    print('working on image_Contour ....................')
    contour_output = []
    area_image = image.shape[0] * image.shape[1]
    print('Area_whole_image = '+str(area_image))
    image_to_find_contour = image.copy()
    im2, contours, hierarchy = cv2.findContours(image_to_find_contour, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_TC89_L1)
    # https://docs.opencv.org/3.4/d4/d73/tutorial_py_contours_begin.html
    for i, contour in enumerate(contours):
        area_contour = cv2.contourArea(contour)
        print('contour_'+str(i)+' Area_contour = '+str(area_contour))
        if 0.0025 < area_contour/area_image < 0.80 :
            x,y,w,h = cv2.boundingRect(contour) # x == row, y == colomn
            print('contour_'+str(i)+' gray_value = ' + str(graycolor_value)+' ; x,y,w,h = '+str(x)+' '+str(y)+' '+str(w)+' '+str(h))
            img_contour = image[y : y+h, x : x+w] # Attension!!!!! Python Matrix editing is [row,column] or [height,width], reversed order to CV2
            #cv2.imshow('contour '+str(i), img_contour)
            contour_output.append((img_contour,graycolor_value,contour))
        else:
            print('contour_'+str(i)+' does not count.')
    return contour_output


# Store Contour to Templates
def contours_to_templates(contours, templates):
    for i, contour in enumerate(contours):
        templates.append(contour)
    return templates


# Threshold to Remove other colors, set value = 0, only leave the color of target_graycolor_idex
def image_threshold(img, target_graycolor_idex):
    ret, img_threshold = cv2.threshold(img, target_graycolor_idex, 255, cv2.THRESH_TOZERO_INV)
    ret, img_threshold = cv2.threshold(img_threshold, target_graycolor_idex-1, 255, cv2.THRESH_TOZERO)  
    return img_threshold


# Draw Rectangle and Put Text
def draw_Rect_Text(image, x,y,w,h, index_template):
    image = cv2.rectangle(image, (x,y), (x+w, y+h), color[index_template], 2)
    image = cv2.putText(image, text='Class['+ str(index_template) +']', org=(x,y), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=color[index_template], thickness=1, lineType=cv2.LINE_AA) 
    return image





# Paramter Initial
templates = []
color_matrix = np.random.randint(low=0,high=255,size=(100,3))# (low, high=None, size=None, dtype='l') # Matrix to List
color = color_matrix.tolist()
threshold_matchShape = 0.5
set_value_Width = 1500

path_sample = os.path.abspath('.\\sample\\')

# Load Image
for filename in os.listdir(path_sample):    
    print('\n########## Read File = ' + filename + ' ##########')
    img_color = cv2.imread(path_sample +'\\' + str(filename), 1) # read image in color BGR
    #cv2.imshow('read', img)
    
    ########## Pre-Processing Image ##########
    # Re-Size Image
    img_resize = image_resize(img_color, set_value_Width)
    
    # Plot Image 
    # cv2.imshow('img_resize_BGR', img_resize)
    
    # Convert to Gray
    img_gray = cv2.cvtColor(img_resize, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('BGR2GRAY', img_gray)
    
    # Show Image Histogram in Gray Color
    target_graycolor_histogram = showImageHistogram_inRange_Gray(img_gray)
        
    # Below here, all image will be call as "img", no matter how many pre-processing we select
    img = img_gray.copy()
    img_output = img_resize.copy()
    
    # Bilateral Filter : reduce noise & keep edges sharp.
    img = cv2.bilateralFilter(img, d=2, sigmaColor=4, sigmaSpace=4)
    #cv2.imshow('bilateral_filter', img)
    
    # Canny Edge Detection
    img = cv2.Canny(img, 30, 200) # (input_image, min_Val, max_Val)
    #cv2.imshow('Canny', img_gray_filter_thresh_canny)
    # http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_canny/py_canny.html
    # https://docs.opencv.org/3.1.0/da/d22/tutorial_py_canny.html
    
    
    # Loop through every Targeted GrayColor Index, use Thresold to select Sepecific Color for Image Shape Analysis
    for i, (target_graycolor_idex, target_graycolor_intensity) in enumerate(target_graycolor_histogram):
        print('\nColor_Iter = '+str(i)+' : Target_GrayColor = ' + str(target_graycolor_idex))
        img_next = img.copy()
        img_next = image_threshold(img_next, target_graycolor_idex)
        #cv2.imshow('img_next_iter_'+str(i)+'_filter_process_img', img_next)
        
        # Contour Image to get Shape
        img_to_findContour = img_next.copy() # function findContours will change the imput image
        contour_output = image_Contour(img_to_findContour, target_graycolor_idex)
        
        # Add Un-Seen Color Contours to Templates
        if target_graycolor_idex not in [ template[1] for template in templates ] :
            templates = contours_to_templates(contour_output, templates)
            print('-> Add Un-Seen Color Contours to Templates .......... GrayColor_Value = '+str(target_graycolor_idex))
            #img_next_output=drwa_Rect_Text(img_next_output, x,y,w,h, index_template)
            
        # Loop Over all Detected Contour in Specific Color
        for index_contour,[img_contour,graycolor_value_contour,contour] in enumerate(contour_output):
            x,y,w,h = cv2.boundingRect(contour)
            print('Image_Contour_Index = '+str(index_contour)+' , GrayColor_Value = ' + str(graycolor_value_contour)+' ; x,y,w,h = '+str(x)+' '+str(y)+' '+str(w)+' '+str(h))
        
            # For every Detected Contour, Loop Over every Template to Match Shape
            match_result = []
            for index_template, [template,graycolor_value_template, template_contour] in enumerate(templates): 
                if graycolor_value_template == target_graycolor_idex:
                    match_value = cv2.matchShapes(contour, template_contour, method=1, parameter=0.0)
                    if match_value < threshold_matchShape:
                        print('Template '+str(index_template)+' , Shape match = '+str(match_value))
                        match_result.append((match_value, index_template))
            #print('match_result = '+str(match_result))
            best_MatchClass = min(match_result, key=lambda item:item[0])[1]
            print('best_MatchClass = '+str(best_MatchClass))
            img_output=draw_Rect_Text(img_output, x,y,w,h, best_MatchClass)

    # Show Output Image
    #cv2.imshow('img_output'+str(filename), img_output)
    
    # Write Output 
    output_filename = 'output/'+str(filename[:-4])+'_TxtRect.png'
    print('\n########## Write File = ' + filename + ' ##########')
    cv2.imwrite(filename = output_filename, img = img_output )
  
cv2.waitKey(0)
cv2.destroyAllWindows()



