# Draw Rectangle and Put Text
def draw_Rect_Text(image, x,y,w,h, index_template):
    image = cv2.rectangle(image, (x,y), (x+w, y+h), color[index_template], 2)
    image = cv2.putText(image, text='Class['+ str(index_template) +']', org=(x,y), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=color[index_template], thickness=1, lineType=cv2.LINE_AA) 
    return image
