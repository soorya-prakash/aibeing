import cv2
import sys
import threading
# capturing first frame without any motion
baseline_image=None
status_list=[None,None]
video=cv2.VideoCapture(0)
x = 10 #position of text
y = 20 #position of text


while True:
    check, frame = video.read()
    gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray_frame=cv2.GaussianBlur(gray_frame,(25,25),0)

    if baseline_image is None:
        baseline_image=gray_frame
        continue

    delta=cv2.absdiff(baseline_image,gray_frame)
    threshold=cv2.threshold(delta, 30, 255, cv2.THRESH_BINARY)[1]
    (contours,_)=cv2.findContours(threshold,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    font = cv2.FONT_HERSHEY_SIMPLEX
    for contour in contours:
        cv2.putText(frame,'no motion detected!',(0,130), font, 1, (200,255,155), 2, cv2.LINE_AA)
        #cv2.PutText(frame,"status: NO MOTION DETECTED", (x,y),cv2.FONT_HERSHEY_SIMPLEX, 255) #Draw the text
        if cv2.contourArea(contour) < 10000:
            continue
        (x, y, w, h)=cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 1)
        cv2.putText(frame,'motion detected!',(0,130), font, 1, (200,255,155), 2, cv2.LINE_AA) 
        print('motion detected')


    cv2.imshow("gray_frame Frame",gray_frame)
    cv2.imshow("Delta Frame",delta)
    cv2.imshow("Threshold Frame",threshold)
    cv2.imshow("Color Frame",frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


video.release()
cv2.destroyAllWindows