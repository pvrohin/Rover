#!/usr/bin/env python
from __future__ import print_function

import roslib
# roslib.load_manifest('my_package')
import sys
import rospy
import cv2
from std_msgs.msg import String
from std_msgs.msg import Bool
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from collections import deque
import numpy as np
import argparse
import imutils

pub = rospy.Publisher('ball', Bool, queue_size=10)

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())


greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
pts = deque(maxlen=args["buffer"])

class image_converter:

  def __init__(self):
    # self.image_pub = rospy.Publisher("image_topic_2",Image)

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/usb_cam/image_raw",Image,self.callback)

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    while True:
    	# resize the frame, blur it, and convert it to the HSV
    	# color space
    	frame = imutils.resize(cv_image, width=600)
    	# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    	# construct a mask for the color "green", then perform
    	# a series of dilations and erosions to remove any small
    	# blobs left in the mask
    	mask = cv2.inRange(hsv, greenLower, greenUpper)
    	mask = cv2.erode(mask, None, iterations=2)
    	mask = cv2.dilate(mask, None, iterations=2)

    	# find contours in the mask and initialize the current
    	# (x, y) center of the ball
    	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
    		cv2.CHAIN_APPROX_SIMPLE)[-2]
    	center = None

    	# only proceed if at least one contour was found
    	if len(cnts) > 0:
    		# find the largest contour in the mask, then use
    		# it to compute the minimum enclosing circle and
    		# centroid
    		c = max(cnts, key=cv2.contourArea)
    		((x, y), radius) = cv2.minEnclosingCircle(c)
    		M = cv2.moments(c)
    		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

    		# only proceed if the radius meets a minimum size
    		if radius > 15:
    			# draw the circle and centroid on the frame,
    			# then update the list of tracked points
    			cv2.circle(frame, (int(x), int(y)), int(radius),
    				(0, 255, 255), 2)
    			cv2.circle(frame, center, 5, (0, 0, 255), -1)
    			pub.publish(True)
    		else:
				pub.publish(False)
    			
    			

    	# update the points queue
    	pts.appendleft(center)

    	# loop over the set of tracked points
    	for i in range(1, len(pts)):
    		# if either of the tracked points are None, ignore
    		# them
    		if pts[i - 1] is None or pts[i] is None:
    			continue

    		# otherwise, compute the thickness of the line and
    		# draw the connecting lines
    		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
    		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    	# show the frame to our screen
    	cv2.imshow("Frame", frame)
    	key = cv2.waitKey(1) & 0xFF
    	# if the 'q' key is pressed, stop the loop
    	if key!= ord("q"):
    		break


    # try:
    #   self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
    # except CvBridgeError as e:
    #   print(e)

def main(args):
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
