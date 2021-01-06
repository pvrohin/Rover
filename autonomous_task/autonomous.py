#!/usr/bin/env python
import rospy
import time
from std_msgs.msg import String
from std_msgs.msg import Bool
from sensor_msgs.msg import Joy

forward = [0.0, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
left = [-0.5, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
right = [0.5, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
stop = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

pub = rospy.Publisher('/joy', Joy, queue_size = 10)
j = Joy()

class auto:

    def ballCallback(self,data):
        self.ball = data.data

    def obstacleCallback(self,data):
        self.obstacle = data.data

    def gpsCallback(self,data):
        if data.data == "forward":
            j.axes = forward
        elif data.data == "left":
            j.axes = left
        elif data.data == "right":
            j.axes = right

    def obstacleSequence(self):
        j.axes = stop
        pub.publish(j)
        now = time.time()
        j.axes = left
        while (int(time.time()) <= now + 5):
            pub.publish(j)
            time.sleep(2)
        j.axes = stop
        pub.publish(j)
        j.axes = forward
        while (int(time.time()) <= now + 5):
            pub.publish(j)
            time.sleep(2)
        j.axes = stop
        pub.publish(j)

    def __init__(self):
        self.ball = False
        self.obstacle = False
        rospy.Subscriber("/ball", Bool, self.ballCallback)
        rospy.Subscriber("/obstacle_dist", Bool, self.obstacleCallback)
        rospy.Subscriber("/turn_direction", String, self.gpsCallback)
        r = rospy.Rate(5)
        while not rospy.is_shutdown():
            if self.ball == True:
                j.axes = stop
                pub.publish(j)
                break
            elif self.obstacle == True:
                self.obstacleSequence()
            else:
                pub.publish(j)
            r.sleep()

if __name__ == "__main__":
    rospy.init_node('autonomous')

    try:
        drive = auto()
    except rospy.ROSInterruptException:
        pass

    rospy.spin()
