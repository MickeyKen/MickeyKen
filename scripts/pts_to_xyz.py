#!/usr/bin/env python

import sys
import rospy
import numpy as np
from std_msgs.msg import String, Int32MultiArray
import cv2
import math

class Homograpy:

    def __init__(self):

        self.sub = rospy.Subscriber("/human_point_xy",Int32MultiArray,self.callback)

        pts_src = np.array([[10,460], [600,460], [600,20],[10,20]],np.float32)
        pts_org = np.array([[3, -4],[3, 4],[-3, 4],[-3, -4]],np.float32)
        self.h, self.status = cv2.findHomography(pts_src, pts_org)
        self.h = np.linalg.inv(self.h)

    def callback(self,data):
        if data.data:
            print ("human number :", len(data.data)/4)



def main(args):
    ic = Homograpy()
    rospy.init_node('pts_to_xyz_node', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")


if __name__ == '__main__':
    main(sys.argv)
