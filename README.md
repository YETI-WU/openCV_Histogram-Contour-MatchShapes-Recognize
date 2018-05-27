# openCV_Histogram-Contour-Template

##Pipeline (draft)
(still working on it. will be finished soon............................................)  
Read a Image from Figure or Video Capture  
Turn into Gray Color Scale  
Plot the Histogram of Image  
Threshold to remove Background   
Ommit 0 and 255 for Black and White Bacground  
Store the major Color from Histogram Analysis:  
  Select the Gray Color Index Range  
  Select the Threshold of Minimum Intensity to render as Background  
  Store the Major Gray Color Index & Intensity for further Propose  
Bilateral Filter : reduce noise & keep edges sharp  
Canny Edge Detection 
Find Contour: mode & method & hierachy 
  mode  
  method  
  hierachy  
 cv2.findContours  
 cv2.arcLength  
 cv2.approxPolyDP  
 area_contour = cv2.contourArea(contour)  
 0.0025 < area_contour/area_image < 0.81  
 x,y,w,h = cv2.boundingRect(contour)  

Save un-Seen Contour to Template  
Use Template to Recognize Item in next Image  
  cv2.matchShapes  
    CONTOURS_MATCH_I1  
    CONTOURS_MATCH_I2  
    CV_CONTOURS_MATCH_I3  
  cv2.matchTemplate  
    square difference  
    cross correlation  
    correlated coefficient  
Draw Rectangle and Put Text  
  cv2.rectangle  
  cv2.putText 
  
