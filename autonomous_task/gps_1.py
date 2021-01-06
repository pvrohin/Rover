#!/usr/bin/env python
from sensor_msgs.msg import NavSatFix
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int32
from sensor_msgs.msg import Joy
import math
import sys

forward = [0.0, 0.0, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0]
left = [-0.5, 0.0, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0]
right = [0.5, 0.0, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0]
stop = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
buttons= [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

gotFix = 0
headingGPS = 0
heading_value = 0
pub = rospy.Publisher("/turn_direction", String, queue_size = 10)

def compCallback(headingValue):
    global heading_value
    heading_value = headingValue.data
    print("In compCallback:",heading_value)
    rospy.spin()   

def distance(current_lat, current_long):
    global lat,lon,heading_value,headingGPS
    dist_calc1 = 0
    dist_calc2 = 0

    diff_lat = 0
    diff_long = 0

    dest_lat = lat
    dest_long = lon

    diff_lat = math.radians(dest_lat - current_lat)
    current_lat = math.radians(current_lat)
    dest_lat = math.radians(dest_lat)

    diff_long = math.radians(dest_long - current_long)
    current_long = math.radians(current_long)
    dest_long = math.radians(dest_long)

    dist_calc1 = (math.sin(diff_lat/2))**2
    dist_calc2 = math.cos(current_lat) * math.cos(dest_lat) * (math.sin(diff_long/2)**2)

    dist_calc = dist_calc1 + dist_calc2
    dist_calc = (2 * math.atan2(math.sqrt(dist_calc),math.sqrt(1 - dist_calc)))
    dist_calc = dist_calc * 6371000

    print("Distance:",dist_calc)

    heading = math.atan2(math.sin(dest_long - current_long) * math.cos(dest_lat), math.cos(current_lat) * math.sin(dest_lat) - math.sin    	(current_lat) * math.cos(dest_lat) * math.cos(dest_long - current_long))
    heading = heading * (180/math.pi)

    head = int(heading)


    if head < 0:
        heading = heading + 360
    print("Heading:",heading)
    rospy.sleep(3.)
    print("Heading value:",heading_value)
    while (heading_value+10 > heading or heading_value-10 < heading):
        headingPrac = heading_value / 10
        if headingPrac > 0:
            headingGPS = headingPrac
        print("Current heading:",headingGPS)
        theta = headingGPS - heading
        theta = math.fabs(theta)
        if theta > 180:
            theta = theta - 180

        print("Theta:",theta)
        if theta >= -180:
            if theta <= 0:
                pub.publish("right")

            if theta < -180:
                pub.publish("left")

        if theta >= 0:
            if theta < 180:
                pub.publish("left")
            if theta >= 180:
                pub.publish("right")

        hd = headingGPS
        if(hd == heading):
            pub.publish("forward")
        rospy.Subscriber("/compass_value",Int32,compCallback)

def callback(gps_fix):
    global gotFix

    print(gps_fix.latitude)
    print(gps_fix.longitude)

    if(gotFix == 0):
        rospy.Subscriber("/compass_value",Int32,compCallback)
        distance(gps_fix.latitude,gps_fix.longitude)
        gotFix = 1


def listener():


    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("/gps/fix",NavSatFix, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    global lat,lon
    lat = float(sys.argv[1])
    lon = float(sys.argv[2])
    listener()
