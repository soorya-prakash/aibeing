import cv2
import sys
import threading
import numpy as np
from face_detector import  face_detecter
# capturing first frame without any motion
baseline_image=None
status_list=[None,None]
video=cv2.VideoCapture(0)
x1 = 10 #position of text
y1 = 20 #position of text
def mse(imageA, imageB):

	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

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
    if not contours:
        cv2.putText(frame,'no motion detected!',(0,50), font, 1, (200,255,155), 2, cv2.LINE_AA)
    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue
        else:
            (x, y, w, h)=cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 1)
            cv2.putText(frame,'motion detected!',(0,20), font, 1, (200,255,155), 2, cv2.LINE_AA)
            faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            faces = faceCascade.detectMultiScale(gray_frame,scaleFactor=1.3, minNeighbors=3,minSize=(30, 30))
            print("[INFO] Found {0} Faces!".format(len(faces)))
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow("gray_frame Frame",gray_frame)
    cv2.imshow("Delta Frame",delta)
    cv2.imshow("Threshold Frame",threshold)
    cv2.imshow("Color Frame",frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


video.release()
cv2.destroyAllWindows