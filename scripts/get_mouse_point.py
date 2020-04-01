#!/usr/bin/env python
from __future__ import print_function

import roslib
# roslib.load_manifest('my_package')
import sys
import rospy
import cv2
from std_msgs.msg import String, Empty
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import message_filters

class mouseParam:
    def __init__(self, input_img_name):

        self.mouseEvent = {"x":None, "y":None, "event":None, "flags":None}

        cv2.setMouseCallback(input_img_name, self.__CallBackFunc, None)

    def __CallBackFunc(self, eventType, x, y, flags, userdata):

        self.mouseEvent["x"] = x
        self.mouseEvent["y"] = y
        self.mouseEvent["event"] = eventType
        self.mouseEvent["flags"] = flags

    def getData(self):
        return self.mouseEvent

    def getEvent(self):
        return self.mouseEvent["event"]

    def getFlags(self):
        return self.mouseEvent["flags"]

    def getX(self):
        return self.mouseEvent["x"]

    def getY(self):
        return self.mouseEvent["y"]

    def getPos(self):
        return (self.mouseEvent["x"], self.mouseEvent["y"])

class image_converter:

    def __init__(self):

        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/fixed_camera_rgb/rgb/image_raw",Image,self.callback)

    def callback(self, data):
        # print (flag)
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        cv2.imshow("Image window", cv_image)
        mouseData = mouseParam("Image window")
        while 1:
            cv2.waitKey(20)

            if mouseData.getEvent() == cv2.EVENT_LBUTTONDOWN:
                print(mouseData.getPos())

            elif mouseData.getEvent() == cv2.EVENT_RBUTTONDOWN:
                break;


def main(args):
    ic = image_converter()
    rospy.init_node('get_mousepoint_server', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
