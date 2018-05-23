# Plot Image with Histogram in Gray Color
def showImageHistogram_inRange_Gray(image, lower=0, upper=255): # Gray Value 0 and 255 will be Omitted
    print('working on showImageHistogram_inRange_Gray....................')
    hist = cv2.calcHist([image], channels=[0], mask=None, histSize=[256], ranges=[0,256]) 
    # print Image & Histogram
    plt.subplot(211), plt.imshow(image, 'gray')
    plt.subplot(212), plt.plot(hist[lower+1:upper])
    plt.show()
    # target graycolor Index & Intensity for next step analysis
    target_graycolor_histogram = []
    threshold_5pct = image.shape[0]*0.05 * image.shape[1]*0.05 #
    print('threshold_5%_intensity = ' +str(threshold_5pct))
    for graycolor_Index, graycolor_Intensity in enumerate(hist):
        if lower < graycolor_Index < upper and graycolor_Intensity > threshold_5pct:
            target_graycolor_histogram.append((graycolor_Index,int(graycolor_Intensity)))
            print('graycolor_Index = ' +str(graycolor_Index)+ ', graycolor_Intensity = ' +str(graycolor_Intensity))
    return target_graycolor_histogram
    
