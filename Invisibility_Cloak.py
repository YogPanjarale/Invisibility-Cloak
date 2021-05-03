import cv2
import numpy as np
import time



output = cv2.VideoWriter_fourcc(*'XVID')# converting to 4cc format
#output
video = cv2.VideoWriter('output2.avi',output,20.0,(640,480))
capture  = cv2.VideoCapture(1)# first camera
# print(type(capture))
# print()
time.sleep(2)#waiting for camera

background = 0
for i in range(60):
  ret,background=capture.read()
# print(background)
background=np.flip(background,axis=1)#inverting camera input

while(capture.isOpened()):
  ret,img = capture.read()
  # print(ret)
  if not ret:
    break
  img= np.flip(img,axis=1)
  hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
  #mask 1
  lowerRed1 = np.array([0,120,50])
  upperRed1 = np.array([10,255,255])
  mask1 = cv2.inRange(hsv,lowerRed1,upperRed1)
  upperRed2 = np.array([170,120,70])
  lowerRed2 = np.array([180,255,255])
  mask2 = cv2.inRange(hsv,lowerRed2,upperRed2)

  mask1= mask1+ mask2
  mask1= cv2.morphologyEx(mask1,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
  mask1= cv2.morphologyEx(mask1,cv2.MORPH_DILATE,np.ones((3,3),np.uint8))

  mask2 = cv2.bitwise_not(mask1)
  #image without red
  res1 = cv2.bitwise_and(img,img,mask=mask2)
  #image with red
  res2 = cv2.bitwise_and(background,background,mask=mask1)

  result = cv2.addWeighted(res1,1,res2,1,0)
  video.write(result)
  cv2.imshow("Invisible!!",result)
  cv2.waitKey(10)
  # isClose =input("Y/N")
  # if isClose.lower() == 'n':
    # break

capture.release()
cv2.destroyAllWindows()


