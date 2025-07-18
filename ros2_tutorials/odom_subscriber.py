import rclpy
from rclpy.node import Node

from nav_msgs.msg import Odometry

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

    def listener_callback(self, msg):
        self.get_logger().info('Z orientation: "%s"' % msg.pose.pose.orientation.z)
        self.get_logger().info('Z angular twist: "%s"' % msg.twist.twist.angular.z)

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
