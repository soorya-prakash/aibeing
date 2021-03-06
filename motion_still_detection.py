import cv2
import sys
import threading
import numpy as np
import datetime
import pandas as pd
import time
df=pd.DataFrame(columns=["Start","End"]) 
baseline_image=None
status_list=[None,None] 
times=[] 
checker=True
video=cv2.VideoCapture(0)
print('no motion detected duration starts at: ',datetime.datetime.now())
endTime = datetime.datetime.now() + datetime.timedelta(minutes=2)
baseimage_change= datetime.datetime.now() + datetime.timedelta(minutes=.5)
print('starting endtime: ',endTime)
while checker:
    status=0 
    check, frame = video.read()
    gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray_frame=cv2.GaussianBlur(gray_frame,(25,25),0)

    if baseline_image is None or datetime.datetime.now() >=baseimage_change :
        baseline_image=gray_frame
        baseimage_change= datetime.datetime.now() + datetime.timedelta(minutes=.5)
        print('baseline_frame_changed')
        continue

    delta=cv2.absdiff(baseline_image,gray_frame)
    threshold=cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
    (contours,_)=cv2.findContours(threshold,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    font = cv2.FONT_HERSHEY_SIMPLEX
    if not contours:
        cv2.putText(frame,'no motion detected!',(0,50), font, 1, (200,255,155), 2, cv2.LINE_AA)
        if datetime.datetime.now() >= endTime:
            print('No motion detected for last one minute: ',datetime.datetime.now())
            print('[info]:storing in database')
            if status==1: 
                times.append(datetime.datetime.now()) 
            checker=False
            break
    else:
        for contour in contours:
            if cv2.contourArea(contour) < 10000:
                continue
            else:
                status=1 
                (x, y, w, h)=cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 1)
                cv2.putText(frame,'motion detected!',(0,20), font, 1, (200,255,155), 2, cv2.LINE_AA)
                faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
                faces = faceCascade.detectMultiScale(gray_frame,scaleFactor=1.3, minNeighbors=3,minSize=(20, 20))
                print("[INFO] Found {0} Faces!".format(len(faces)))
                endTime = datetime.datetime.now() + datetime.timedelta(minutes=1)
                # print("new endtime:",endTime)
                for (x1, y1, w1, h1) in faces:
                    cv2.rectangle(frame, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
                    if (x,y,w,h) == (x1,y1,w1,h1):
                        print('human standing still ')
    status_list.append(status) 
    status_list=status_list[-2:] 
    if status_list[-1]==1 and status_list[-2]==0: 
        times.append(datetime.datetime.now()) 

    if status_list[-1]==0 and status_list[-2]==1: 
        times.append(datetime.datetime.now())

    cv2.imshow("gray_frame Frame",gray_frame)
    cv2.imshow("Delta Frame",delta)
    cv2.imshow("Threshold Frame",threshold)
    cv2.imshow("Color Frame",frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        if status==1: 
            times.append(datetime.datetime.now()) 
        for (x, y, w, h) in faces:
            roi_color= frame[y:y + h, x:x + w] 
            cv2.imwrite(str(x) + '_faces.jpg', roi_color)
            print("[INFO] detected face stored successfully")
        break
print(len(times))
for i in range(0,len(times),2): 
    df=df.append({"Start":times[i],"End":times[i+1]},ignore_index=True)
d=datetime.datetime.now()
df.to_csv("{}-{}-{}-{}.csv".format(d.strftime("%Y"),d.strftime("%b"),d.strftime("%d"),d.strftime("%S")))
video.release()
cv2.destroyAllWindows