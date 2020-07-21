import cv2
import sys
def face_detecter():
    vid = cv2.VideoCapture(0) 
    
    while(True): 
        ret, frame = vid.read()   
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=3,
        minSize=(30, 30))

        print("[INFO] Found {0} Faces!".format(len(faces)))
        for (x, y, w, h) in faces:
            print('helo')
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow('frame', frame) 
        # the 'q' button is set as the 
        # quitting button you may use any 
        # desired button of your choice 

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi_color = frame[y:y + h, x:x + w] 

    # After the loop release the cap object 
    vid.release() 
    # Destroy all the windows 
    cv2.destroyAllWindows() 
    return roi_color

# image = cv2.imread('img2.jpg')
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
# faces = faceCascade.detectMultiScale(
#     gray,
#     scaleFactor=1.3,
#     minNeighbors=3,
#     minSize=(30, 30)
# )

# print("[INFO] Found {0} Faces!".format(len(faces)))
# for (x, y, w, h) in faces:
#     cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
#     roi_color = image[y:y + h, x:x + w] 
#     print("[INFO] Object found. Saving locally.") 
#     cv2.imwrite(str(w) + str(h) + '_faces.jpg', roi_color)


