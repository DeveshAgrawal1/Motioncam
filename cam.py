from cv2 import imshow, waitKey, threshold, findContours
import cv2
import datetime

def detect(img,feed):
    motiondetect=False
    temp=img.copy()
    contours,hierarchy=findContours(temp,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    if(len(contours)>0):
        motiondetect=True
    else:
        motiondetect=False
        
    return motiondetect


cap=cv2.VideoCapture(0)
pr=False
font=cv2.FONT_HERSHEY_SIMPLEX
recording=False
startr=True
count=0
out=cv2.VideoWriter()
while True:
    ret,img=cap.read()
    if startr==True:
        out = cv2.VideoWriter("E:/vid"+str(count)+".avi",-1, 10, (640,480),1)
        startr=False
    img=cv2.resize(img,(640,480))
    grayimg=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,img2=cap.read()
    grayimg2=cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    diffimg=cv2.absdiff(grayimg,grayimg2)
    m,thresimg=cv2.threshold(diffimg,20,255,cv2.THRESH_BINARY)
    thresimg=cv2.blur(thresimg,(10,10))
    n,thresimg=threshold(thresimg,20,255,cv2.THRESH_BINARY)
    motionn=detect(thresimg, img)
    now=datetime.datetime.now()
    mm = str(now.month)
    dd = str(now.day)
    yy = str(now.year)
    hour = str(now.hour)
    if(int(hour)<10):
        hour="0"+str(hour)
    mi = str(now.minute)
    if(int(mi)<10):
        mi="0"+str(mi)
    ss = str(now.second)
    if(int(ss)<10):
        ss="0"+str(ss)
    pdt=dd+"-"+mm+"-"+yy+" "+hour+":"+mi+":"+ss
    cv2.rectangle(img,(0,460),(200,480),(255,255,255),-1)
    cv2.putText(img,str(pdt),(10,473), font, 0.5,(0,0,0),2)
    if(motionn==True):
        recording=True
         
    else:
        recording=False
    if(recording==True):
        out.write(img)
        cv2.putText(img,"Motion Detected",(0,420),cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2)
    
    
    imshow("Window",img)
    
    k=waitKey(20)
    if k==27:
        break
    elif k==110:
        count=count+1
        startr=True
    elif k==114:
        if(startr==False):
            startr=True

cap.release()
cv2.destroyAllWindows()
