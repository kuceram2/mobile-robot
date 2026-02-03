import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist

import math

import time

#from action_tutorials_interfaces.action import Fibonacci
from tutorial_interfaces.action import Translate

class TranslationActionServer(Node):

    def __init__(self):
        super().__init__('translation_action_server')
        self._action_server = ActionServer(
            self,
            Translate, #interface name
            'translate', # action name (both must match with action client)
            self.execute_callback)
        
        # subscriber for getting current rotation
        self.subscription = self.create_subscription(Odometry, 'diff_cont/odom', self.listener_callback, 10)
        self.subscription  # prevent unused variable warning


        # publisher for commanding the robot
        self.publisher_ = self.create_publisher(Twist, 'diff_cont/cmd_vel_unstamped', 10)
        self.get_logger().info("Translation action ready")


    def listener_callback(self, msg):
        self.x_current_pos = msg.pose.pose.position.x
        self.y_current_pos = msg.pose.pose.position.y
    

    def execute_callback(self, goal_handle):
        cmd_msg = Twist()
        x_start_pos = self.x_current_pos
        y_start_pos = self.y_current_pos
        desired_dist = goal_handle.request.goal

        while True:
            x_delta = abs(self.x_current_pos - x_start_pos)
            y_delta = abs(self.y_current_pos - y_start_pos)
            
            direction = 1 if desired_dist > 0 else -1


            cmd_msg.linear.x = 0.2 * direction
            self.publisher_.publish(cmd_msg)

            if(math.sqrt((x_delta * x_delta) + (y_delta * y_delta)) >= abs(desired_dist)):
                break
 
        goal_handle.succeed()
        result = Translate.Result()
        result.result = "Done!"
        self.get_logger().info(f'Result: {result.result}')
        return result


def main(args=None):
    rclpy.init(args=args)

    translation_action_server = TranslationActionServer()

    executor = MultiThreadedExecutor()
    executor.add_node(translation_action_server)
    executor.spin()

    translation_action_server.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()