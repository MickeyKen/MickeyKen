#!/usr/bin/env python
import sys
import rospy
import cv2
import datetime
import numpy as np
from std_msgs.msg import Int16
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import rospkg

import message_filters


class Subscribe():
    def __init__(self):

        self.bridge = CvBridge()
        self.path = rospkg.RosPack().get_path('cv_neuroud') + '/picture/'
        # print (self.path)

        # Declaration Subscriber
        self.img_sub = message_filters.Subscriber('/fixed_camera_rgb/rgb/image_raw', Image)
        self.int_sub = message_filters.Subscriber('/take_picture/flag', Int16)

        ts = message_filters.ApproximateTimeSynchronizer([self.img_sub, self.int_sub], 10, 5, allow_headerless=True)
        ts.registerCallback(self.callback)


    ### callback function for /people_tracker_measurements ###
    def callback(self, img, data):
        print (data)
        try:
            cv_image = self.bridge.imgmsg_to_cv2(img, "bgr8")
        except CvBridgeError as e:
            print(e)

        dt_now = datetime.datetime.now()
        cv2.imwrite(str(dt_now) + '.png', cv_image)
        print ("saved!", self.path + str(dt_now) + '.png')

if __name__ == '__main__':
    rospy.init_node('take_picture')

    Subscribe = Subscribe()

    rospy.spin()
