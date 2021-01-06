#!/usr/bin/env python
from sensor_msgs.msg import NavSatFix
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int32
from sensor_msgs.msg import Joy
import math
import sys

forward = [0.0, 0.0, 0.8, 0.0, 0.0, 0.0, 0.0, 0.0]
left = [-0.8, 0.0, 0.8, 0.0, 0.0, 0.0, 0.0, 0.0]
right = [0.8, 0.0, 0.8, 0.0, 0.0, 0.0, 0.0, 0.0]
stop = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

pub = rospy.Publisher("/turn_direction", String, queue_size = 10)

class GPS:

    def gpsCallback(self,pos):
        self.currentLat = pos.latitude
        self.currentLon = pos.longitude
        print("Latitude:",self.currentLat)
        print("Longitude:",self.currentLon)

    def compassCallback(self,angle):
        self.heading = angle.data

    def move(self):

        dist_calc1 = 0
        dist_calc2 = 0

        diff_lat = 0
        diff_lon = 0

        #difference between latitudes
        diff_lat = math.radians(self.destLat - self.currentLat)

        #converting latitudes to radians
        self.currentLat = math.radians(self.currentLat)
        self.destLat = math.radians(self.destLat)

        #difference between longitudes
        diff_lon = math.radians(self.destLon - self.currentLon)

        #converting longitudes to radians
        self.currentLon = math.radians(self.currentLon)
        self.destLon = math.radians(self.destLon)

        #calculating distances
        dist_calc1 = (math.sin(diff_lat/2)) ** 2
        dist_calc2 = math.cos(self.currentLat) * math.cos(self.destLat) * (math.sin(diff_lon/2) ** 2)

        #combining the individual distances
        self.distance = dist_calc1 + dist_calc2
        self.distance = (2 * math.atan2( math.sqrt(self.distance), math.sqrt(1 - self.distance) ))

        #converting to meters
        self.distance = self.distance * 6371000

        print("Distance:",self.distance)

        #calculating the angle of bearing
        self.bearing = math.atan2(math.sin(self.destLon - self.currentLon) * math.cos(self.destLat) , math.cos(self.currentLat) * math.sin(self.destLat) - math.sin(self.currentLat) * math.cos(self.destLat) * math.cos(self.destLon - self.currentLon))

        #converting the angle of bearing to degrees
        self.bearing = self.bearing * (180/math.pi)

        #converting the negative angles to positive
        self.bearing = (self.bearing + 360) % 360

        print("Bearing:", self.bearing)
        print("Heading:", self.heading)

        turnAngle = self.heading - int(self.bearing)

        print(turnAngle)
        if turnAngle >= 180:
            if turnAngle <= 0:
                self.moveDirection = "right"

        if turnAngle < -180:
            self.moveDirection = "left"

        if turnAngle >= 0:
            if turnAngle < 180:
                self.moveDirection = "left"

        if turnAngle >= 180:
            self.moveDirection = "right"

        if self.heading + 2 > self.bearing:
            if self.heading - 2 < self.bearing:
                self.moveDirection = "straight"


    def __init__(self):
        self.destLat = float(sys.argv[1])
        self.destLon = float(sys.argv[2])
        self.currentLat = 0
        self.currentLon = 0
        self.bearing = 0
        self.heading = 0
        self.moveDirection = "stop"
        rospy.Subscriber("/gps/fix",NavSatFix, self.gpsCallback)
        rospy.Subscriber("/compass_value",Int32,self.compassCallback)

        r = rospy.Rate(10)
        while not rospy.is_shutdown():
            self.move()
            pub.publish(self.moveDirection)
            r.sleep()

if __name__ == '__main__':
    rospy.init_node('gps')

    try:
        run = GPS()
    except rospy.ROSInterruptException:
        pass

    rospy.spin()
