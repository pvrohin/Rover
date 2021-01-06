#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Bool
from sensor_msgs.msg import Joy

forward = [0.0, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
left = [-0.5, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
right = [0.5, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
stop = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

pub = rospy.Publisher('joy', Joy, queue_size=10)
#rate = rospy.Rate(10) 
j = Joy()

gotBall = 1
gotObst = 1

def ball_callback(data):
    global gotBall
    print(data.data)
    if data.data==True:
        j.axes=stop
        pub.publish(j)
        gotBall = 0
    else:
        gotBall = 1
		
def obstacle_callback(data):
    global gotObst
    print(data.data)
    if(data.data == True):
        j.axes = stop
        pub.publish(j)
        now = time.time()
        j.axes = left
        while (int(time.time()) <= now + 10):
            pub.publish(j)
            time.sleep(2)
        pub.publish(j)
        rospy.Subscriber("obstacle_dist", Bool, obstacle_callback)
    else:
        now = time.time()
        speed = 30
        dif = speed/(dist + 0.5)
        j.axes = forward
        pub.publish(j)
        time.sleep(2)
    gotObst = 0

def gps_callback(data):
    global gotObst
    print("Inside gps callback")
    if data.data == "forward":
        j.axes = forward
        pub.publish(j)
    elif data.data == "left":
        j.axes = left
        pub.publish(j)
    elif data.data == "right":
        j.axes = right
        pub.publish(j)


def listener():
    global gotBall
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("ball", Bool, ball_callback)   
    while(gotBall):
        print("In side turn direction calling loop")
        rospy.Subscriber("obstacle_dist", Bool, obstacle_callback)
        rospy.Subscriber("/turn_direction", String, gps_callback)
		
    j.axes=stop
    pub.publish(j)	
	
	# spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':

    listener()







