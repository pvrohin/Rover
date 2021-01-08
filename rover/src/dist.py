#!/usr/bin/python
import pyrealsense2 as rs
import rospy
from std_msgs.msg import String
import time


try:
	# Create a context object. This object owns the handles to all connected realsense devices
	pipeline = rs.pipeline()
	pipeline.start()
	pub = rospy.Publisher('obstacle_dist', String, queue_size=10)
	rospy.init_node('obstacleDetect', anonymous=True)
	rate = rospy.Rate(10)
	while not rospy.is_shutdown():
		frames = pipeline.wait_for_frames(5000)
		depth = frames.get_depth_frame()
		width = depth.get_width()
		height = depth.get_height()
		if not depth: continue
		dist = depth.get_distance(width//2, height//2)
		res = ""
		if dist < 5:
			res = "stop "
			pub.publish(res + "\t" + str(dist))
			now = time.time()
			res = "left"
			while (int(time.time()) <= now + 10):
				pub.publish(res + "\t" + str(dist))
				time.sleep(2)
			pub.publish(res)
			now = time.time()
			speed = 30
			dif = speed/(dist + 0.5)
			res = "forward"
			dist = depth.get_distance(width//2, height//2)
			while (dist >= 5 and int(time.time()) <= now + dif):
				pub.publish(res + "\t" + str(dist))
				dist = depth.get_distance(width//2, height//2)
				time.sleep(2)
		else:
			res = "ok"
			pub.publish(res)
		rate.sleep()

except Exception as e:
    print(e)
    pass
