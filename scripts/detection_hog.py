#!/usr/bin/env python
from __future__ import print_function

import roslib
# roslib.load_manifest('my_package')
import sys
import rospy
import cv2
from std_msgs.msg import String, Int32MultiArray
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import dlib

class image_converter:

    def __init__(self):
        # self.image_pub = rospy.Publisher("image_topic_2",Image)
        self.pnt_pub = rospy.Publisher("human_point_xy", Int32MultiArray, queue_size=100)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/fixed_camera_rgb/rgb/image_raw",Image,self.callback)

        self.SvmFile = "../human/detector.svm"
        self.detector = dlib.simple_object_detector(self.SvmFile)
        self.win_det = dlib.image_window()
        self.win_det.set_image(self.detector)

    def callback(self,data):
        try:
            self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        dets = self.detector(self.cv_image)

        array=[]

        for d in dets:
            # array.append([int(d.left()), int(d.top()), int(d.right()), int(d.bottom())])
            # array.append(int(d.left()))
            array[len(array):len(array)] = [int(d.left()), int(d.top()), int(d.right()), int(d.bottom())]
            self.write_rec(d)
        print (array)

        cv2.imshow("Image window", self.cv_image)
        cv2.waitKey(3)

        array_forPublish = Int32MultiArray(data=array)
        self.pnt_pub.publish(array_forPublish)
        # try:
        #     self.image_pub.publish(self.bridge.cv2_to_imgmsg(self.cv_image, "bgr8"))
        # except CvBridgeError as e:
        #     print(e)


    def write_rec(self, d):
        cv2.rectangle(self.cv_image, (d.left(), d.top()), (d.right(), d.bottom()), (0, 0, 255), 2)

def main(args):
    ic = image_converter()
    rospy.init_node('detection_hog', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
