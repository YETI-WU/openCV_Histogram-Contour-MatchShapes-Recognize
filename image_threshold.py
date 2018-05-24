# Threshold to Remove other colors, set value = 0, only leave the color of target_graycolor_idex
def image_threshold(img, target_graycolor_idex):
    ret, img_threshold = cv2.threshold(img, target_graycolor_idex, 255, cv2.THRESH_TOZERO_INV)
    ret, img_threshold = cv2.threshold(img_threshold, target_graycolor_idex-1, 255, cv2.THRESH_TOZERO)  
    return img_threshold
