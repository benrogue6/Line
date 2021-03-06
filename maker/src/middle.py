#!/usr/bin/env python

import rospy, cv2, cv_bridge, numpy
from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import Twist


class black:
  def __init__(self):
    self.bridge = cv_bridge.CvBridge()
    
    self.image_sub = rospy.Subscriber('/camera/color/image_raw',Image, self.image_callback)

    self.cmd_vel_pub = rospy.Publisher('/cmd_vel',Twist, queue_size=1)
    self.twist = Twist()

  def image_callback(self, msg):
    image = self.bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

   #lower_yellow = numpy.array([ 10,  10,  10])
   #upper_yellow = numpy.array([255, 255, 250])

    lower_black = numpy.array([ 0, 0, 0])
    upper_black = numpy.array([180, 255, 30])

   #lower_white = numpy.array([0,0,180]) 0,0, 200
   #higher_white = numpy.array([255,255,255]) 180,255,255

    mask = cv2.inRange(hsv, lower_black, upper_black)
  # mask = cv2.inRange(hsv, lower_white, higher_white)
    
    h, w, d = image.shape
    search_top = 3*h/4
    search_bot = 3*h/4 + 20
   #image[0:search_top, 0:w] = 0
   #image[0:search_top, 0:w] = 0
    mask[0:search_top, 0:w] = 0
    mask[search_bot:h, 0:w] = 0
    M = cv2.moments(mask)
   #M = cv2.moments(image)

    if M['m00'] > 0:
      cx = int(M['m10']/M['m00'])
      cy = int(M['m01']/M['m00'])
      #cv2.circle(image, (cx, cy), 20, (0,0,255), -1)
      
      err = cx - w/2
      self.twist.linear.x = 0.2
      self.twist.angular.z = -float(err) / 100
      self.cmd_vel_pub.publish(self.twist)
      
    cv2.imshow("mask",mask)
    cv2.imshow("output", image)
    cv2.waitKey(3)

rospy.init_node('black')
black = black()
rospy.spin()
