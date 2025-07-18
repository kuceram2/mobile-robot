import rclpy
from rclpy.node import Node

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Vector3

from tf_transformations import euler_from_quaternion
import math

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        # self.subscription = self.create_subscription(
        #     String,
        #     'topic',
        #     self.listener_callback,
        #     10)
        self.subscription = self.create_subscription(Odometry, 'diff_cont/odom', self.listener_callback, 10)
        self.subscription  # prevent unused variable warning

        self.publisher_ = self.create_publisher(Vector3, 'orientation_euler', 10)

    def listener_callback(self, msg):
        quaternion = [msg.pose.pose.orientation.x, msg.pose.pose.orientation.y, msg.pose.pose.orientation.z, msg.pose.pose.orientation.w]
        roll_rad, pitch_rad, yaw_rad = euler_from_quaternion(quaternion)

        roll_deg = math.degrees(roll_rad)
        pitch_deg = math.degrees(pitch_rad)
        yaw_deg = math.degrees(yaw_rad)

        euler_msg = Vector3()
        euler_msg.x = roll_deg
        euler_msg.y = pitch_deg
        euler_msg.z = yaw_deg
        self.publisher_.publish(euler_msg)
        self.get_logger().info(f"Converted to Euler: roll={roll_deg:.3f}, pitch={pitch_deg:.3f}, yaw={yaw_deg:.3f}")     

def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
