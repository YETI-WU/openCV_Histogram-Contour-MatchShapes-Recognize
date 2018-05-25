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
            cv2.drawContours(imgage, contours, i, color=(255,0,0), thickness=2)
            #img_contour = image[y : y+h, x : x+w] # Attension!!!!! Python Matrix editing is [row,column] or [height,width], reversed order to CV2
            cv2.imshow('contour '+str(i), img_contour)
            contour_output.append((img_contour,graycolor_value,contour))
        else:
            print('contour_'+str(i)+' does not count.')
    return contour_output
