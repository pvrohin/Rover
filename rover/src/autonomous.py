#!/usr/bin/python
import pyrealsense2 as rs
import rospy
from std_msgs.msg import String
import time
from sensor_msgs.msg import Joy


forward = [0.0, 0.0, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0]
left = [-0.5, 0.0, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0]
right = [0.5, 0.0, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0]
stop = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


try:
	# Create a context object. This object owns the handles to all connected realsense devices
	pipeline = rs.pipeline()
	pipeline.start()
	pub = rospy.Publisher('obstacle_dist', Joy, queue_size=10)
	rospy.init_node('obstacleDetect', anonymous=True)
	rate = rospy.Rate(10) 
	j = Joy()
	while not rospy.is_shutdown():
		frames = pipeline.wait_for_frames(5000)
		depth = frames.get_depth_frame()
		if not depth: continue
		
		dist = depth.get_distance(340, 240)
		if dist < 5:
			j.axes = stop
			pub.publish(j)
			now = time.time()
			j.axes = left
			while (int(time.time()) <= now + 10):
				pub.publish(j)
				time.sleep(2)
			pub.publish(j)
			now = time.time()
			speed = 30
			dif = speed/(dist + 0.5)
			j.axes = forward
			dist = depth.get_distance(340, 240)
			while (dist >= 5 and int(time.time()) <= now + dif):
				pub.publish(j)
				dist = depth.get_distance(340, 240)
				time.sleep(2)
		else:
			j.axes = forward
			pub.publish(j)
		rate.sleep()

except Exception as e:	
    print(e)
    pass
