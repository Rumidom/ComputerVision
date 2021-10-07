import cv2
import numpy as np

img = cv2.imread('Images/VW_Van.png')

Upper_Limit = np.array([109, 255, 255])
Lower_Limit = np.array([70, 121, 99])

hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_img,Lower_Limit,Upper_Limit)
masked_img = cv2.bitwise_and(img, img, mask=mask)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
mask_inv = cv2.bitwise_not(mask)
background = cv2.bitwise_and(gray,gray, mask=mask_inv)
background = np.stack((background,)*3,axis=-1)
added_img = cv2.add(masked_img,background)

cv2.imshow('Result',added_img)
cv2.imwrite('Images/Result.png',added_img)
cv2.waitKey(0)
cv2.destroyAllWindows()