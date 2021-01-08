#!/usr/bin/python
import pyrealsense2 as rs
import rospy
from std_msgs.msg import String
import time
from sensor_msgs.msg import Joy
from std_msgs.msg import Bool


try:
	# Create a context object. This object owns the handles to all connected realsense devices
	pipeline = rs.pipeline()
	pipeline.start()
	pub = rospy.Publisher('obstacle_dist', Bool, queue_size=10)
	rospy.init_node('obstacleDetect', anonymous=True)
	rate = rospy.Rate(10) 
	while not rospy.is_shutdown():
		frames = pipeline.wait_for_frames(5000)
		depth = frames.get_depth_frame()
		if not depth: continue
		
		dist = depth.get_distance(340, 240)
		if dist < 5:
			#str="Obstacle detected"
			pub.publish(True)
		else:
			#str="Obstacle not detected"
			pub.publish(False)
		rate.sleep()

except Exception as e:
	print(e)
	pass
