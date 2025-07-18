import rclpy
from rclpy.node import Node

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            LaserScan,
            'scan',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

        self.get_logger().info("sub created")

        self.publisher_ = self.create_publisher(Twist, 'diff_cont/cmd_vel_unstamped', 10)

        self.get_logger().info("pub created")

        self.last_val = 1.0


    def listener_callback(self, msg):
        dist = msg.ranges[90]
        self.get_logger().info('Distance: "%s"' % dist)

        out = Twist()

        if str(dist) != "inf": self.last_val = dist
        
        if str(dist) != "inf" or (str(dist) == "inf" and self.last_val > 0.2):


            if dist > 0.50:
                out.linear.x = 0.1
                self.get_logger().info('Going forward')
            else: 
                out.linear.x = 0.0
                out.angular.z = 0.5
                self.get_logger().warning('Stopped!')
        else:
            self.get_logger().debug('Discarting value')



        self.publisher_.publish(out)

def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()
    minimal_subscriber.get_logger().info("sub defined")

    rclpy.spin(minimal_subscriber)
    minimal_subscriber.get_logger().info("sub running")

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
