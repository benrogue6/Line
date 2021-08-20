#!/usr/bin/env python
from __future__ import print_function


import sys
import numpy as np
#import rospy
#import cv2
import rospy, cv2, cv_bridge, numpy
from std_msgs.msg import String
#from sensor_msgs.msg import Image
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
import time

class image_converter:

  def __init__(self):
    self.cmd_vel_pub = rospy.Publisher("/cmd_vel",Twist, queue_size=2)

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/camera/color/image_raw",Image, self.callback)
    self.twist = Twist()

   
  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
     
      #converting bgr to hsv in order to identify the green color
      hsv_cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
   
    except CvBridgeError as e:
      print(e)

  
    lower_green = np.array([45, 100, 50])
    upper_green = np.array([70, 255, 255]) 

    masking = cv2.inRange(hsv_cv_image, lower_green, upper_green)
   #M = cv2.moments(masking)
    
   #cv2.imshow("Green_detection", masking)

    cv2.waitKey(3)

 
     
   
def main(args):
  ic = image_converter()

  rospy.init_node('traffic', anonymous = True)

  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()




if __name__ == '__main__':
    main(sys.argv)
    
