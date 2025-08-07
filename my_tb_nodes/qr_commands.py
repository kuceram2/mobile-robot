import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np
from geometry_msgs.msg import Twist
import sys
import time

from my_turtlebot4_navigator import TurtleBot4Directions, TurtleBot4Navigator

class QRCodeCommands(Node):
    def __init__(self):
        super().__init__('qr_commands')
        namespace = sys.argv[1]
        self.subscription = self.create_subscription(
            Image,
            f'/{namespace}/oakd/rgb/preview/image_raw',
            self.listener_callback,
            10)
        self.bridge = CvBridge()

        self.publisher = self.create_publisher(Twist, f'/{namespace}/cmd_vel', 10)

        self.detector = cv2.QRCodeDetector()

        self.navigator = TurtleBot4Navigator(namespace)

        self.timer = self.create_timer(0.2, self.timer_callback)

        #cv2.startWindowThread()

        self.qr_data = "stop"
        self.go_forward = False
        

    def listener_callback(self, msg):
        self.get_qr_data(msg)

       # print("callback")
        if self.qr_data == "left":
            self.go_forward = False
            self.navigator.rotate_angle_deg(90)
            self.go_forward = True

        elif self.qr_data == "right":
            self.go_forward = False
            self.navigator.rotate_angle_deg(-90)
            self.go_forward = True

        elif self.qr_data == "forward":
            self.go_forward = True
        
        elif self.qr_data == "position 1":
            self.go_forward = False
            
    def timer_callback(self):
        #print("callback")
        if self.go_forward:
            msg = Twist()
            msg.linear.x = 0.1
            self.publisher.publish(msg)


    def get_qr_data(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        data, bbox, _ = self.detector.detectAndDecode(frame)

        if bbox is not None:
            # Draw bounding box
            for i in range(len(bbox)):
                cv2.circle(frame, (int(bbox[0][0][0]), int(bbox[0][0][1])), 5, (0,255,0), 5)
                cv2.circle(frame, (int(bbox[0][2][0]), int(bbox[0][2][1])), 5, (255,0,0), 5)
                pts = np.array(bbox[0], np.int32)
                cv2.polylines(frame, [pts], True, (0,255,0), 5 )
            if data:
                print("Decoded Data:", data)
                cv2.putText(frame, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                self.qr_data = data
                time.sleep(1)
            else: 
                #self.qr_data = ""
                print("Old data: ", self.qr_data)
        # Display
        #cv2.imshow("Camera Feed with Blobs", frame)
        #print("frame")
        #cv2.waitKey(1)

        self.qr_data = data

        



def main(args=None):

    # rclpy.init(args=args)
    # node = QRCodeCommands()
    # rclpy.spin(node)

    # node.destroy_node()
    # rclpy.shutdown()
    # cv2.destroyAllWindows()
    rclpy.init(args=args)
    node = QRCodeCommands()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()


    node.destroy_node()
    rclpy.shutdown()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
