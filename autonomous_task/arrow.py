import numpy as np
import cv2
import math
from math import degrees, atan2


cap = cv2.VideoCapture(1)

while True:
	ret, frame = cap.read()
	img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	img2 = cv2.imread('white.png', cv2.IMREAD_COLOR)


	_,threshold = cv2.threshold(img, 110, 255,
								cv2.THRESH_BINARY)

	_,contours,_=cv2.findContours(threshold, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	posible_arrow = None
	for cnt in contours :
		area = cv2.contourArea(cnt)
		# print(len(area))
		if area > 400:
			approx = cv2.approxPolyDP(cnt,
									0.01 * cv2.arcLength(cnt, True), True)
			if(len(approx) == 7):
				posible_arrow = approx.copy()

	if posible_arrow is not None:
		# cv2.drawContours(img2, [posible_arrow], 0, (0, 0, 255), 5)
		cv2.fillPoly(img2, [posible_arrow], (0,0,0))
	else:
		continue
	img2 = cv2.bitwise_not(img2)
	first_white_pixel, last_white_pixel = np.array(np.where(img2 == 255))[:,[0,-1]].T
	# print(first_white_pixel, last_white_pixel)
	mid = (first_white_pixel[0] + last_white_pixel[0])/2

	# Taking a matrix of size 5 as the kernel
	# kernel = np.ones((5,5), np.uint8)

	# # you want to erode/dilate a given image.
	# img2 = cv2.erode(img2, kernel, iterations=1)
	# img2 = cv2.dilate(img2, kernel, iterations=1)
	edges = cv2.Canny(img2,50,200,apertureSize = 3)
	corners = cv2.goodFeaturesToTrack(edges, maxCorners = 5, qualityLevel=0.01, minDistance = 10)
	corners = np.int0(corners)


	count = 0

	for i in corners:
		x,y = i.ravel()
		cv2.circle(img2,(x,y),3,255,-1)
		# print(x)
		if x > mid:
			count += 1
		else:
			count -= 1
	if count < 0:
		print("left")
	else:
		print("right")
	# cv2.imshow('image2', img2)
	# cv2.imwrite('answer.jpg', img2)

	# Exiting the window if 'q' is pressed on the keyboard.
	if cv2.waitKey(0) & 0xFF == ord('q'):
		cv2.destroyAllWindows()
